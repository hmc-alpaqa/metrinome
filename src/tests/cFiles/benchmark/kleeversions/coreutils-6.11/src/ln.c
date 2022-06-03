/* `ln' program to create links between files.
   Copyright (C) 1986, 1989-1991, 1995-2007 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* Written by Mike Parker and David MacKenzie. */

#include <config.h>
#include <stdio.h>
#include <sys/types.h>
#include <getopt.h>

#include "system.h"
#include "backupfile.h"
#include "error.h"
#include "filenamecat.h"
#include "file-set.h"
#include "hash.h"
#include "hash-triple.h"
#include "quote.h"
#include "same.h"
#include "yesno.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "ln"

#define AUTHORS "Mike Parker", "David MacKenzie"

#ifndef ENABLE_HARD_LINK_TO_SYMLINK_WARNING
# define ENABLE_HARD_LINK_TO_SYMLINK_WARNING 0
#endif

/* In being careful not even to try to make hard links to directories,
   we have to know whether link(2) follows symlinks.  If it does, then
   we have to *stat* the `source' to see if the resulting link would be
   to a directory.  Otherwise, we have to use *lstat* so that we allow
   users to make hard links to symlinks-that-point-to-directories.  */

#if LINK_FOLLOWS_SYMLINKS
# define STAT_LIKE_LINK(File, Stat_buf) \
  stat (File, Stat_buf)
#else
# define STAT_LIKE_LINK(File, Stat_buf) \
  lstat (File, Stat_buf)
#endif

/* The name by which the program was run, for error messages.  */
char *program_name;

/* FIXME: document */
static enum backup_type backup_type;

/* If true, make symbolic links; otherwise, make hard links.  */
static bool symbolic_link;

/* If true, ask the user before removing existing files.  */
static bool interactive;

/* If true, remove existing files unconditionally.  */
static bool remove_existing_files;

/* If true, list each file as it is moved. */
static bool verbose;

/* If true, allow the superuser to *attempt* to make hard links
   to directories.  However, it appears that this option is not useful
   in practice, since even the superuser is prohibited from hard-linking
   directories on most (all?) existing systems.  */
static bool hard_dir_link;

/* If nonzero, and the specified destination is a symbolic link to a
   directory, treat it just as if it were a directory.  Otherwise, the
   command `ln --force --no-dereference file symlink-to-dir' deletes
   symlink-to-dir before creating the new link.  */
static bool dereference_dest_dir_symlinks = true;

/* This is a set of destination name/inode/dev triples for hard links
   created by ln.  Use this data structure to avoid data loss via a
   sequence of commands like this:
   rm -rf a b c; mkdir a b c; touch a/f b/f; ln -f a/f b/f c && rm -r a b */
static Hash_table *dest_set;

/* Initial size of the dest_set hash table.  */
enum { DEST_INFO_INITIAL_CAPACITY = 61 };

static struct option const long_options[] =
{
  {"backup", optional_argument, NULL, 'b'},
  {"directory", no_argument, NULL, 'F'},
  {"no-dereference", no_argument, NULL, 'n'},
  {"no-target-directory", no_argument, NULL, 'T'},
  {"force", no_argument, NULL, 'f'},
  {"interactive", no_argument, NULL, 'i'},
  {"suffix", required_argument, NULL, 'S'},
  {"target-directory", required_argument, NULL, 't'},
  {"symbolic", no_argument, NULL, 's'},
  {"verbose", no_argument, NULL, 'v'},
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
  {NULL, 0, NULL, 0}
};

/* FILE is the last operand of this command.  Return true if FILE is a
   directory.  But report an error there is a problem accessing FILE,
   or if FILE does not exist but would have to refer to an existing
   directory if it referred to anything at all.  */

static bool
target_directory_operand (char const *file)
{
  char const *b = last_component (file);
  size_t blen = strlen (b);
  bool looks_like_a_dir = (blen == 0 || ISSLASH (b[blen - 1]));
  struct stat st;
  int stat_result =
    (dereference_dest_dir_symlinks ? stat (file, &st) : lstat (file, &st));
  int err = (stat_result == 0 ? 0 : errno);
  bool is_a_dir = !err && S_ISDIR (st.st_mode);
  if (err && err != ENOENT)
    error (EXIT_FAILURE, err, _("accessing %s"), quote (file));
  if (is_a_dir < looks_like_a_dir)
    error (EXIT_FAILURE, err, _("target %s is not a directory"), quote (file));
  return is_a_dir;
}

/* Make a link DEST to the (usually) existing file SOURCE.
   Symbolic links to nonexistent files are allowed.
   Return true if successful.  */

static bool
do_link (const char *source, const char *dest)
{
  struct stat source_stats;
  struct stat dest_stats;
  char *dest_backup = NULL;
  bool dest_lstat_ok = false;
  bool source_is_dir = false;
  bool ok;

  /* Use stat here instead of lstat.
     On SVR4, link does not follow symlinks, so this check disallows
     making hard links to symlinks that point to directories.  Big deal.
     On other systems, link follows symlinks, so this check is right.  */
  if (!symbolic_link)
    {
      if (STAT_LIKE_LINK (source, &source_stats) != 0)
	{
	  error (0, errno, _("accessing %s"), quote (source));
	  return false;
	}

      if (ENABLE_HARD_LINK_TO_SYMLINK_WARNING
	  && S_ISLNK (source_stats.st_mode))
	{
	  error (0, 0, _("%s: warning: making a hard link to a symbolic link\
 is not portable"),
		 quote (source));
	}

      if (S_ISDIR (source_stats.st_mode))
	{
	  source_is_dir = true;
	  if (! hard_dir_link)
	    {
	      error (0, 0, _("%s: hard link not allowed for directory"),
		     quote (source));
	      return false;
	    }
	}
    }

  if (remove_existing_files || interactive || backup_type != no_backups)
    {
      dest_lstat_ok = (lstat (dest, &dest_stats) == 0);
      if (!dest_lstat_ok && errno != ENOENT)
	{
	  error (0, errno, _("accessing %s"), quote (dest));
	  return false;
	}
    }

  /* If the current target was created as a hard link to another
     source file, then refuse to unlink it.  */
  if (dest_lstat_ok
      && dest_set != NULL
      && seen_file (dest_set, dest, &dest_stats))
    {
      error (0, 0,
	     _("will not overwrite just-created %s with %s"),
	     quote_n (0, dest), quote_n (1, source));
      return false;
    }

  /* If --force (-f) has been specified without --backup, then before
     making a link ln must remove the destination file if it exists.
     (with --backup, it just renames any existing destination file)
     But if the source and destination are the same, don't remove
     anything and fail right here.  */
  if ((remove_existing_files
       /* Ensure that "ln --backup f f" fails here, with the
	  "... same file" diagnostic, below.  Otherwise, subsequent
	  code would give a misleading "file not found" diagnostic.
	  This case is different than the others handled here, since
	  the command in question doesn't use --force.  */
       || (!symbolic_link && backup_type != no_backups))
      && dest_lstat_ok
      /* Allow `ln -sf --backup k k' to succeed in creating the
	 self-referential symlink, but don't allow the hard-linking
	 equivalent: `ln -f k k' (with or without --backup) to get
	 beyond this point, because the error message you'd get is
	 misleading.  */
      && (backup_type == no_backups || !symbolic_link)
      && (!symbolic_link || stat (source, &source_stats) == 0)
      && SAME_INODE (source_stats, dest_stats)
      /* The following detects whether removing DEST will also remove
	 SOURCE.  If the file has only one link then both are surely
	 the same link.  Otherwise check whether they point to the same
	 name in the same directory.  */
      && (source_stats.st_nlink == 1 || same_name (source, dest)))
    {
      error (0, 0, _("%s and %s are the same file"),
	     quote_n (0, source), quote_n (1, dest));
      return false;
    }

  if (dest_lstat_ok)
    {
      if (S_ISDIR (dest_stats.st_mode))
	{
	  error (0, 0, _("%s: cannot overwrite directory"), quote (dest));
	  return false;
	}
      if (interactive)
	{
	  fprintf (stderr, _("%s: replace %s? "), program_name, quote (dest));
	  if (!yesno ())
	    return true;
	  remove_existing_files = true;
	}

      if (backup_type != no_backups)
	{
	  dest_backup = find_backup_file_name (dest, backup_type);
	  if (rename (dest, dest_backup) != 0)
	    {
	      int rename_errno = errno;
	      free (dest_backup);
	      dest_backup = NULL;
	      if (rename_errno != ENOENT)
		{
		  error (0, rename_errno, _("cannot backup %s"), quote (dest));
		  return false;
		}
	    }
	}
    }

  ok = ((symbolic_link ? symlink (source, dest) : link (source, dest))
	== 0);

  /* If the attempt to create a link failed and we are removing or
     backing up destinations, unlink the destination and try again.

     POSIX 1003.1-2004 requires that ln -f A B must unlink B even on
     failure (e.g., when A does not exist).  This is counterintuitive,
     and we submitted a defect report
     <http://www.opengroup.org/austin/mailarchives/ag-review/msg01794.html>
     (2004-06-24).  If the committee does not fix the standard we'll
     have to change the behavior of ln -f, at least if POSIXLY_CORRECT
     is set.  In the meantime ln -f A B will not unlink B unless the
     attempt to link A to B failed because B already existed.

     Try to unlink DEST even if we may have backed it up successfully.
     In some unusual cases (when DEST and DEST_BACKUP are hard-links
     that refer to the same file), rename succeeds and DEST remains.
     If we didn't remove DEST in that case, the subsequent symlink or link
     call would fail.  */

  if (!ok && errno == EEXIST && (remove_existing_files || dest_backup))
    {
      if (unlink (dest) != 0)
	{
	  error (0, errno, _("cannot remove %s"), quote (dest));
	  free (dest_backup);
	  return false;
	}

      ok = ((symbolic_link ? symlink (source, dest) : link (source, dest))
	    == 0);
    }

  if (ok)
    {
      /* Right after creating a hard link, do this: (note dest name and
	 source_stats, which are also the just-linked-destinations stats) */
      record_file (dest_set, dest, &source_stats);

      if (verbose)
	{
	  if (dest_backup)
	    printf ("%s ~ ", quote (dest_backup));
	  printf ("%s %c> %s\n", quote_n (0, dest), (symbolic_link ? '-' : '='),
		  quote_n (1, source));
	}
    }
  else
    {
      error (0, errno,
	     (symbolic_link
	      ? (errno != ENAMETOOLONG && *source
		 ? _("creating symbolic link %s")
		 : _("creating symbolic link %s -> %s"))
	      : (errno == EMLINK && !source_is_dir
		 ? _("creating hard link to %.0s%s")
		 : (errno == EDQUOT || errno == EEXIST || errno == ENOSPC
		    || errno == EROFS)
		 ? _("creating hard link %s")
		 : _("creating hard link %s => %s"))),
	     quote_n (0, dest), quote_n (1, source));

      if (dest_backup)
	{
	  if (rename (dest_backup, dest) != 0)
	    error (0, errno, _("cannot un-backup %s"), quote (dest));
	}
    }

  free (dest_backup);
  return ok;
}

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, _("Try `%s --help' for more information.\n"),
	     program_name);
  else
    {
      printf (_("\
Usage: %s [OPTION]... [-T] TARGET LINK_NAME   (1st form)\n\
  or:  %s [OPTION]... TARGET                  (2nd form)\n\
  or:  %s [OPTION]... TARGET... DIRECTORY     (3rd form)\n\
  or:  %s [OPTION]... -t DIRECTORY TARGET...  (4th form)\n\
"),
	      program_name, program_name, program_name, program_name);
      fputs (_("\
In the 1st form, create a link to TARGET with the name LINK_NAME.\n\
In the 2nd form, create a link to TARGET in the current directory.\n\
In the 3rd and 4th forms, create links to each TARGET in DIRECTORY.\n\
Create hard links by default, symbolic links with --symbolic.\n\
When creating hard links, each TARGET must exist.\n\
\n\
"), stdout);
      fputs (_("\
Mandatory arguments to long options are mandatory for short options too.\n\
"), stdout);
      fputs (_("\
      --backup[=CONTROL]      make a backup of each existing destination file\n\
  -b                          like --backup but does not accept an argument\n\
  -d, -F, --directory         allow the superuser to attempt to hard link\n\
                                directories (note: will probably fail due to\n\
                                system restrictions, even for the superuser)\n\
  -f, --force                 remove existing destination files\n\
"), stdout);
      fputs (_("\
  -n, --no-dereference        treat destination that is a symlink to a\n\
                                directory as if it were a normal file\n\
  -i, --interactive           prompt whether to remove destinations\n\
  -s, --symbolic              make symbolic links instead of hard links\n\
"), stdout);
      fputs (_("\
  -S, --suffix=SUFFIX         override the usual backup suffix\n\
  -t, --target-directory=DIRECTORY  specify the DIRECTORY in which to create\n\
                                the links\n\
  -T, --no-target-directory   treat LINK_NAME as a normal file\n\
  -v, --verbose               print name of each linked file\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      fputs (_("\
\n\
The backup suffix is `~', unless set with --suffix or SIMPLE_BACKUP_SUFFIX.\n\
The version control method may be selected via the --backup option or through\n\
the VERSION_CONTROL environment variable.  Here are the values:\n\
\n\
"), stdout);
      fputs (_("\
  none, off       never make backups (even if --backup is given)\n\
  numbered, t     make numbered backups\n\
  existing, nil   numbered if numbered backups exist, simple otherwise\n\
  simple, never   always make simple backups\n\
"), stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

int
main (int argc, char **argv)
{
  int c;
  bool ok;
  bool make_backups = false;
  char *backup_suffix_string;
  char *version_control_string = NULL;
  char const *target_directory = NULL;
  bool no_target_directory = false;
  int n_files;
  char **file;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdin);

  /* FIXME: consider not calling getenv for SIMPLE_BACKUP_SUFFIX unless
     we'll actually use backup_suffix_string.  */
  backup_suffix_string = getenv ("SIMPLE_BACKUP_SUFFIX");

  symbolic_link = remove_existing_files = interactive = verbose
    = hard_dir_link = false;

  while ((c = getopt_long (argc, argv, "bdfinst:vFS:T", long_options, NULL))
	 != -1)
    {
      switch (c)
	{
	case 'b':
	  make_backups = true;
	  if (optarg)
	    version_control_string = optarg;
	  break;
	case 'd':
	case 'F':
	  hard_dir_link = true;
	  break;
	case 'f':
	  remove_existing_files = true;
	  interactive = false;
	  break;
	case 'i':
	  remove_existing_files = false;
	  interactive = true;
	  break;
	case 'n':
	  dereference_dest_dir_symlinks = false;
	  break;
	case 's':
	  symbolic_link = true;
	  break;
	case 't':
	  if (target_directory)
	    error (EXIT_FAILURE, 0, _("multiple target directories specified"));
	  else
	    {
	      struct stat st;
	      if (stat (optarg, &st) != 0)
		error (EXIT_FAILURE, errno, _("accessing %s"), quote (optarg));
	      if (! S_ISDIR (st.st_mode))
		error (EXIT_FAILURE, 0, _("target %s is not a directory"),
		       quote (optarg));
	    }
	  target_directory = optarg;
	  break;
	case 'T':
	  no_target_directory = true;
	  break;
	case 'v':
	  verbose = true;
	  break;
	case 'S':
	  make_backups = true;
	  backup_suffix_string = optarg;
	  break;
	case_GETOPT_HELP_CHAR;
	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);
	default:
	  usage (EXIT_FAILURE);
	  break;
	}
    }

  n_files = argc - optind;
  file = argv + optind;

  if (n_files <= 0)
    {
      error (0, 0, _("missing file operand"));
      usage (EXIT_FAILURE);
    }

  if (no_target_directory)
    {
      if (target_directory)
	error (EXIT_FAILURE, 0,
	       _("Cannot combine --target-directory "
		 "and --no-target-directory"));
      if (n_files != 2)
	{
	  if (n_files < 2)
	    error (0, 0,
		   _("missing destination file operand after %s"),
		   quote (file[0]));
	  else
	    error (0, 0, _("extra operand %s"), quote (file[2]));
	  usage (EXIT_FAILURE);
	}
    }
  else if (!target_directory)
    {
      if (n_files < 2)
	target_directory = ".";
      else if (2 <= n_files && target_directory_operand (file[n_files - 1]))
	target_directory = file[--n_files];
      else if (2 < n_files)
	error (EXIT_FAILURE, 0, _("target %s is not a directory"),
	       quote (file[n_files - 1]));
    }

  if (backup_suffix_string)
    simple_backup_suffix = xstrdup (backup_suffix_string);

  backup_type = (make_backups
		 ? xget_version (_("backup type"), version_control_string)
		 : no_backups);

  if (target_directory)
    {
      int i;

      /* Create the data structure we'll use to record which hard links we
	 create.  Used to ensure that ln detects an obscure corner case that
	 might result in user data loss.  Create it only if needed.  */
      if (2 <= n_files
	  && remove_existing_files
	  /* Don't bother trying to protect symlinks, since ln clobbering
	     a just-created symlink won't ever lead to real data loss.  */
	  && ! symbolic_link
	  /* No destination hard link can be clobbered when making
	     numbered backups.  */
	  && backup_type != numbered_backups)

	{
	  dest_set = hash_initialize (DEST_INFO_INITIAL_CAPACITY,
				      NULL,
				      triple_hash,
				      triple_compare,
				      triple_free);
	  if (dest_set == NULL)
	    xalloc_die ();
	}

      ok = true;
      for (i = 0; i < n_files; ++i)
	{
	  char *dest_base;
	  char *dest = file_name_concat (target_directory,
					 last_component (file[i]),
					 &dest_base);
	  strip_trailing_slashes (dest_base);
	  ok &= do_link (file[i], dest);
	  free (dest);
	}
    }
  else
    ok = do_link (file[0], file[1]);

  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}
