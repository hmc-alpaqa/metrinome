/* chcon -- change security context of files
   Copyright (C) 2005-2008 Free Software Foundation, Inc.

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

#include <config.h>
#include <stdio.h>
#include <sys/types.h>
#include <getopt.h>

#include "system.h"
#include "dev-ino.h"
#include "error.h"
#include "quote.h"
#include "quotearg.h"
#include "root-dev-ino.h"
#include "selinux-at.h"
#include "xfts.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "chcon"

#define AUTHORS "Russell Coker", "Jim Meyering"

enum Change_status
{
  CH_NOT_APPLIED,
  CH_SUCCEEDED,
  CH_FAILED,
  CH_NO_CHANGE_REQUESTED
};

enum Verbosity
{
  /* Print a message for each file that is processed.  */
  V_high,

  /* Print a message for each file whose attributes we change.  */
  V_changes_only,

  /* Do not be verbose.  This is the default. */
  V_off
};

/* The name the program was run with. */
char *program_name;

/* If nonzero, and the systems has support for it, change the context
   of symbolic links rather than any files they point to.  */
static bool affect_symlink_referent;

/* If true, change the modes of directories recursively. */
static bool recurse;

/* Level of verbosity. */
static bool verbose;

/* Pointer to the device and inode numbers of `/', when --recursive.
   Otherwise NULL.  */
static struct dev_ino *root_dev_ino;

/* The name of the context file is being given. */
static char const *specified_context;

/* Specific components of the context */
static char const *specified_user;
static char const *specified_role;
static char const *specified_range;
static char const *specified_type;

/* For long options that have no equivalent short option, use a
   non-character as a pseudo short option, starting with CHAR_MAX + 1.  */
enum
{
  DEREFERENCE_OPTION = CHAR_MAX + 1,
  NO_PRESERVE_ROOT,
  PRESERVE_ROOT,
  REFERENCE_FILE_OPTION
};

static struct option const long_options[] =
{
  {"recursive", no_argument, NULL, 'R'},
  {"dereference", no_argument, NULL, DEREFERENCE_OPTION},
  {"no-dereference", no_argument, NULL, 'h'},
  {"no-preserve-root", no_argument, NULL, NO_PRESERVE_ROOT},
  {"preserve-root", no_argument, NULL, PRESERVE_ROOT},
  {"reference", required_argument, NULL, REFERENCE_FILE_OPTION},
  {"user", required_argument, NULL, 'u'},
  {"role", required_argument, NULL, 'r'},
  {"type", required_argument, NULL, 't'},
  {"range", required_argument, NULL, 'l'},
  {"verbose", no_argument, NULL, 'v'},
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
  {NULL, 0, NULL, 0}
};

/* Given a security context, CONTEXT, derive a context_t (*RET),
   setting any portions selected via the global variables, specified_user,
   specified_role, etc.  */
static int
compute_context_from_mask (security_context_t context, context_t *ret)
{
  bool ok = true;
  context_t new_context = context_new (context);
  if (!new_context)
    {
      error (0, errno, _("failed to create security context: %s"),
	     quotearg_colon (context));
      return 1;
    }

#define SET_COMPONENT(C, comp)						\
   do									\
     {									\
       if (specified_ ## comp						\
	   && context_ ## comp ## _set ((C), specified_ ## comp))	\
         {								\
	    error (0, errno,						\
		   _("failed to set %s security context component to %s"), \
		   #comp, quote (specified_ ## comp));			\
           ok = false;							\
	 }								\
     }									\
   while (0)

  SET_COMPONENT (new_context, user);
  SET_COMPONENT (new_context, range);
  SET_COMPONENT (new_context, role);
  SET_COMPONENT (new_context, type);

  if (!ok)
    {
      int saved_errno = errno;
      context_free (new_context);
      errno = saved_errno;
      return 1;
    }

  *ret = new_context;
  return 0;
}

/* Change the context of FILE, using specified components.
   If it is a directory and -R is given, recurse.
   Return 0 if successful, 1 if errors occurred. */

static int
change_file_context (int fd, char const *file)
{
  security_context_t file_context = NULL;
  context_t context;
  security_context_t context_string;
  int errors = 0;

  if (specified_context == NULL)
    {
      int status = (affect_symlink_referent
		    ? getfileconat (fd, file, &file_context)
		    : lgetfileconat (fd, file, &file_context));

      if (status < 0 && errno != ENODATA)
	{
	  error (0, errno, _("failed to get security context of %s"),
		 quote (file));
	  return 1;
	}

      /* If the file doesn't have a context, and we're not setting all of
	 the context components, there isn't really an obvious default.
	 Thus, we just give up. */
      if (file_context == NULL)
	{
	  error (0, 0, _("can't apply partial context to unlabeled file %s"),
		 quote (file));
	  return 1;
	}

      if (compute_context_from_mask (file_context, &context))
	return 1;
    }
  else
    {
      /* FIXME: this should be done exactly once, in main.  */
      context = context_new (specified_context);
      if (!context)
	abort ();
    }

  context_string = context_str (context);

  if (file_context == NULL || ! STREQ (context_string, file_context))
    {
      int fail = (affect_symlink_referent
		  ?  setfileconat (fd, file, context_string)
		  : lsetfileconat (fd, file, context_string));

      if (fail)
	{
	  errors = 1;
	  error (0, errno, _("failed to change context of %s to %s"),
		 quote_n (0, file), quote_n (1, context_string));
	}
    }

  context_free (context);
  freecon (file_context);

  return errors;
}

/* Change the context of FILE.
   Return true if successful.  This function is called
   once for every file system object that fts encounters.  */

static bool
process_file (FTS *fts, FTSENT *ent)
{
  char const *file_full_name = ent->fts_path;
  char const *file = ent->fts_accpath;
  const struct stat *file_stats = ent->fts_statp;
  bool ok = true;

  switch (ent->fts_info)
    {
    case FTS_D:
      if (recurse)
	{
	  if (ROOT_DEV_INO_CHECK (root_dev_ino, ent->fts_statp))
	    {
	      /* This happens e.g., with "chcon -R --preserve-root ... /"
		 and with "chcon -RH --preserve-root ... symlink-to-root".  */
	      ROOT_DEV_INO_WARN (file_full_name);
	      /* Tell fts not to traverse into this hierarchy.  */
	      fts_set (fts, ent, FTS_SKIP);
	      /* Ensure that we do not process "/" on the second visit.  */
	      ent = fts_read (fts);
	      return false;
	    }
	  return true;
	}
      break;

    case FTS_DP:
      if (! recurse)
	return true;
      break;

    case FTS_NS:
      /* For a top-level file or directory, this FTS_NS (stat failed)
	 indicator is determined at the time of the initial fts_open call.
	 With programs like chmod, chown, and chgrp, that modify
	 permissions, it is possible that the file in question is
	 accessible when control reaches this point.  So, if this is
	 the first time we've seen the FTS_NS for this file, tell
	 fts_read to stat it "again".  */
      if (ent->fts_level == 0 && ent->fts_number == 0)
	{
	  ent->fts_number = 1;
	  fts_set (fts, ent, FTS_AGAIN);
	  return true;
	}
      error (0, ent->fts_errno, _("cannot access %s"), quote (file_full_name));
      ok = false;
      break;

    case FTS_ERR:
      error (0, ent->fts_errno, _("%s"), quote (file_full_name));
      ok = false;
      break;

    case FTS_DNR:
      error (0, ent->fts_errno, _("cannot read directory %s"),
	     quote (file_full_name));
      ok = false;
      break;

    default:
      break;
    }

  if (ent->fts_info == FTS_DP
      && ok && ROOT_DEV_INO_CHECK (root_dev_ino, file_stats))
    {
      ROOT_DEV_INO_WARN (file_full_name);
      ok = false;
    }

  if (ok)
    {
      if (verbose)
	printf (_("changing security context of %s"),
		quote (file_full_name));

      if (change_file_context (fts->fts_cwd_fd, file) != 0)
	ok = false;
    }

  if ( ! recurse)
    fts_set (fts, ent, FTS_SKIP);

  return ok;
}

/* Recursively operate on the specified FILES (the last entry
   of which is NULL).  BIT_FLAGS controls how fts works.
   Return true if successful.  */

static bool
process_files (char **files, int bit_flags)
{
  bool ok = true;

  FTS *fts = xfts_open (files, bit_flags, NULL);

  while (1)
    {
      FTSENT *ent;

      ent = fts_read (fts);
      if (ent == NULL)
	{
	  if (errno != 0)
	    {
	      /* FIXME: try to give a better message  */
	      error (0, errno, _("fts_read failed"));
	      ok = false;
	    }
	  break;
	}

      ok &= process_file (fts, ent);
    }

  /* Ignore failure, since the only way it can do so is in failing to
     return to the original directory, and since we're about to exit,
     that doesn't matter.  */
  fts_close (fts);

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
Usage: %s [OPTION]... CONTEXT FILE...\n\
  or:  %s [OPTION]... [-u USER] [-r ROLE] [-l RANGE] [-t TYPE] FILE...\n\
  or:  %s [OPTION]... --reference=RFILE FILE...\n\
"),
	program_name, program_name, program_name);
      fputs (_("\
Change the security context of each FILE to CONTEXT.\n\
With --reference, change the security context of each FILE to that of RFILE.\n\
\n\
  -c, --changes          like verbose but report only when a change is made\n\
  -h, --no-dereference   affect symbolic links instead of any referenced file\n\
"), stdout);
      fputs (_("\
      --reference=RFILE  use RFILE's security context rather than specifying\n\
                         a CONTEXT value\n\
  -R, --recursive        operate on files and directories recursively\n\
  -v, --verbose          output a diagnostic for every file processed\n\
"), stdout);
      fputs (_("\
  -u, --user=USER        set user USER in the target security context\n\
  -r, --role=ROLE        set role ROLE in the target security context\n\
  -t, --type=TYPE        set type TYPE in the target security context\n\
  -l, --range=RANGE      set range RANGE in the target security context\n\
\n\
"), stdout);
      fputs (_("\
The following options modify how a hierarchy is traversed when the -R\n\
option is also specified.  If more than one is specified, only the final\n\
one takes effect.\n\
\n\
  -H                     if a command line argument is a symbolic link\n\
                         to a directory, traverse it\n\
  -L                     traverse every symbolic link to a directory\n\
                         encountered\n\
  -P                     do not traverse any symbolic links (default)\n\
\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
    }
  exit (status);
}

int
main (int argc, char **argv)
{
  security_context_t ref_context = NULL;

  /* Bit flags that control how fts works.  */
  int bit_flags = FTS_PHYSICAL;

  /* 1 if --dereference, 0 if --no-dereference, -1 if neither has been
     specified.  */
  int dereference = -1;

  bool ok;
  bool preserve_root = false;
  bool component_specified = false;
  char *reference_file = NULL;
  int optc;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  while ((optc = getopt_long (argc, argv, "HLPRchvu:r:t:l:", long_options, NULL))
	 != -1)
    {
      switch (optc)
	{
	case 'H': /* Traverse command-line symlinks-to-directories.  */
	  bit_flags = FTS_COMFOLLOW | FTS_PHYSICAL;
	  break;

	case 'L': /* Traverse all symlinks-to-directories.  */
	  bit_flags = FTS_LOGICAL;
	  break;

	case 'P': /* Traverse no symlinks-to-directories.  */
	  bit_flags = FTS_PHYSICAL;
	  break;

	case 'h': /* --no-dereference: affect symlinks */
	  dereference = 0;
	  break;

	case DEREFERENCE_OPTION: /* --dereference: affect the referent
				    of each symlink */
	  dereference = 1;
	  break;

	case NO_PRESERVE_ROOT:
	  preserve_root = false;
	  break;

	case PRESERVE_ROOT:
	  preserve_root = true;
	  break;

	case REFERENCE_FILE_OPTION:
	  reference_file = optarg;
	  break;

	case 'R':
	  recurse = true;
	  break;

	case 'f':
	  /* ignore */
	  break;

	case 'v':
	  verbose = true;
	  break;

	case 'u':
	  specified_user = optarg;
	  component_specified = true;
	  break;

	case 'r':
	  specified_role = optarg;
	  component_specified = true;
	  break;

	case 't':
	  specified_type = optarg;
	  component_specified = true;
	  break;

	case 'l':
	  specified_range = optarg;
	  component_specified = true;
	  break;

	case_GETOPT_HELP_CHAR;
	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);
	default:
	  usage (EXIT_FAILURE);
	}
    }

  if (recurse)
    {
      if (bit_flags == FTS_PHYSICAL)
	{
	  if (dereference == 1)
	    error (EXIT_FAILURE, 0,
		   _("-R --dereference requires either -H or -L"));
	  affect_symlink_referent = false;
	}
      else
	{
	  if (dereference == 0)
	    error (EXIT_FAILURE, 0, _("-R -h requires -P"));
	  affect_symlink_referent = true;
	}
    }
  else
    {
      bit_flags = FTS_PHYSICAL;
      affect_symlink_referent = (dereference != 0);
    }

  if (argc - optind < (reference_file || component_specified ? 1 : 2))
    {
      if (argc <= optind)
	error (0, 0, _("missing operand"));
      else
	error (0, 0, _("missing operand after %s"), quote (argv[argc - 1]));
      usage (EXIT_FAILURE);
    }

  if (reference_file)
    {
      if (getfilecon (reference_file, &ref_context) < 0)
	error (EXIT_FAILURE, errno, _("failed to get security context of %s"),
	       quote (reference_file));

      specified_context = ref_context;
    }
  else if (component_specified)
    {
      /* FIXME: it's already null, so this is a no-op. */
      specified_context = NULL;
    }
  else
    {
      context_t context;
      specified_context = argv[optind++];
      context = context_new (specified_context);
      if (!context)
	error (EXIT_FAILURE, 0, _("invalid context: %s"),
	       quotearg_colon (specified_context));
      context_free (context);
    }

  if (reference_file && component_specified)
    {
      error (0, 0, _("conflicting security context specifiers given"));
      usage (1);
    }

  if (recurse & preserve_root)
    {
      static struct dev_ino dev_ino_buf;
      root_dev_ino = get_root_dev_ino (&dev_ino_buf);
      if (root_dev_ino == NULL)
	error (EXIT_FAILURE, errno, _("failed to get attributes of %s"),
	       quote ("/"));
    }
  else
    {
      root_dev_ino = NULL;
    }

  ok = process_files (argv + optind, bit_flags | FTS_NOSTAT);

  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}
