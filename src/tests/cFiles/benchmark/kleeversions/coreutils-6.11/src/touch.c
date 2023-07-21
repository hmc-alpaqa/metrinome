/* touch -- change modification and access times of files
   Copyright (C) 87, 1989-1991, 1995-2005, 2007-2008
   Free Software Foundation, Inc.

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

/* Written by Paul Rubin, Arnold Robbins, Jim Kingdon, David MacKenzie,
   and Randy Smith. */

#include <config.h>
#include <stdio.h>
#include <getopt.h>
#include <sys/types.h>

#include "system.h"
#include "argmatch.h"
#include "error.h"
#include "fd-reopen.h"
#include "getdate.h"
#include "posixtm.h"
#include "posixver.h"
#include "quote.h"
#include "stat-time.h"
#include "utimens.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "touch"

#define AUTHORS \
"Paul Rubin", "Arnold Robbins, Jim Kingdon, David MacKenzie", "Randy Smith"

/* Bitmasks for `change_times'. */
#define CH_ATIME 1
#define CH_MTIME 2

/* The name by which this program was run. */
char *program_name;

/* Which timestamps to change. */
static int change_times;

/* (-c) If true, don't create if not already there.  */
static bool no_create;

/* (-r) If true, use times from a reference file.  */
static bool use_ref;

/* If true, the only thing we have to do is change both the
   modification and access time to the current time, so we don't
   have to own the file, just be able to read and write it.
   On some systems, we can do this if we own the file, even though
   we have neither read nor write access to it.  */
static bool amtime_now;

/* New access and modification times to use when setting time.  */
static struct timespec newtime[2];

/* File to use for -r. */
static char *ref_file;

/* For long options that have no equivalent short option, use a
   non-character as a pseudo short option, starting with CHAR_MAX + 1.  */
enum
{
  TIME_OPTION = CHAR_MAX + 1
};

static struct option const longopts[] =
{
  {"time", required_argument, NULL, TIME_OPTION},
  {"no-create", no_argument, NULL, 'c'},
  {"date", required_argument, NULL, 'd'},
  {"file", required_argument, NULL, 'r'}, /* FIXME: remove --file in 2006 */
  {"reference", required_argument, NULL, 'r'},
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
  {NULL, 0, NULL, 0}
};

/* Valid arguments to the `--time' option. */
static char const* const time_args[] =
{
  "atime", "access", "use", "mtime", "modify", NULL
};

/* The bits in `change_times' that those arguments set. */
static int const time_masks[] =
{
  CH_ATIME, CH_ATIME, CH_ATIME, CH_MTIME, CH_MTIME
};

/* Store into *RESULT the result of interpreting FLEX_DATE as a date,
   relative to NOW.  If NOW is null, use the current time.  */

static void
get_reldate (struct timespec *result,
	     char const *flex_date, struct timespec const *now)
{
  if (! get_date (result, flex_date, now))
    error (EXIT_FAILURE, 0, _("invalid date format %s"), quote (flex_date));
}

/* Update the time of file FILE according to the options given.
   Return true if successful.  */

static bool
touch (const char *file)
{
  bool ok;
  struct stat sbuf;
  int fd = -1;
  int open_errno = 0;
  struct timespec timespec[2];
  struct timespec const *t;

  if (STREQ (file, "-"))
    fd = STDOUT_FILENO;
  else if (! no_create)
    {
      /* Try to open FILE, creating it if necessary.  */
      fd = fd_reopen (STDIN_FILENO, file,
		      O_WRONLY | O_CREAT | O_NONBLOCK | O_NOCTTY,
		      S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);

      /* Don't save a copy of errno if it's EISDIR, since that would lead
	 touch to give a bogus diagnostic for e.g., `touch /' (assuming
	 we don't own / or have write access to it).  On Solaris 5.6,
	 and probably other systems, it is EINVAL.  On SunOS4, it's EPERM.  */
      if (fd == -1 && errno != EISDIR && errno != EINVAL && errno != EPERM)
	open_errno = errno;
    }

  if (change_times != (CH_ATIME | CH_MTIME))
    {
      /* We're setting only one of the time values.  stat the target to get
	 the other one.  If we have the file descriptor already, use fstat.
	 Otherwise, either we're in no-create mode (and hence didn't call open)
	 or FILE is inaccessible or a directory, so we have to use stat.  */
      if (fd != -1 ? fstat (fd, &sbuf) : stat (file, &sbuf))
	{
	  if (open_errno)
	    error (0, open_errno, _("creating %s"), quote (file));
	  else
	    {
	      if (no_create && (errno == ENOENT || errno == EBADF))
		return true;
	      error (0, errno, _("failed to get attributes of %s"),
		     quote (file));
	    }
	  if (fd == STDIN_FILENO)
	    close (fd);
	  return false;
	}
    }

  if (amtime_now)
    {
      /* Pass NULL to futimens so it will not fail if we have
	 write access to the file, but don't own it.  */
      t = NULL;
    }
  else
    {
      timespec[0] = (change_times & CH_ATIME
		     ? newtime[0]
		     : get_stat_atime (&sbuf));
      timespec[1] = (change_times & CH_MTIME
		     ? newtime[1]
		     : get_stat_mtime (&sbuf));
      t = timespec;
    }

  ok = (gl_futimens (fd, (fd == STDOUT_FILENO ? NULL : file), t) == 0);

  if (fd == STDIN_FILENO)
    {
      if (close (STDIN_FILENO) != 0)
	{
	  error (0, errno, _("closing %s"), quote (file));
	  return false;
	}
    }
  else if (fd == STDOUT_FILENO)
    {
      /* Do not diagnose "touch -c - >&-".  */
      if (!ok && errno == EBADF && no_create
	  && change_times == (CH_ATIME | CH_MTIME))
	return true;
    }

  if (!ok)
    {
      if (open_errno)
	{
	  /* The wording of this diagnostic should cover at least two cases:
	     - the file does not exist, but the parent directory is unwritable
	     - the file exists, but it isn't writable
	     I think it's not worth trying to distinguish them.  */
	  error (0, open_errno, _("cannot touch %s"), quote (file));
	}
      else
	{
	  if (no_create && errno == ENOENT)
	    return true;
	  error (0, errno, _("setting times of %s"), quote (file));
	}
      return false;
    }

  return true;
}

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, _("Try `%s --help' for more information.\n"),
	     program_name);
  else
    {
      printf (_("Usage: %s [OPTION]... FILE...\n"), program_name);
      fputs (_("\
Update the access and modification times of each FILE to the current time.\n\
\n\
A FILE argument that does not exist is created empty.\n\
\n\
A FILE argument string of - is handled specially and causes touch to\n\
change the times of the file associated with standard output.\n\
\n\
"), stdout);
      fputs (_("\
Mandatory arguments to long options are mandatory for short options too.\n\
"), stdout);
      fputs (_("\
  -a                     change only the access time\n\
  -c, --no-create        do not create any files\n\
  -d, --date=STRING      parse STRING and use it instead of current time\n\
  -f                     (ignored)\n\
  -m                     change only the modification time\n\
"), stdout);
      fputs (_("\
  -r, --reference=FILE   use this file's times instead of current time\n\
  -t STAMP               use [[CC]YY]MMDDhhmm[.ss] instead of current time\n\
  --time=WORD            change the specified time:\n\
                           WORD is access, atime, or use: equivalent to -a\n\
                           WORD is modify or mtime: equivalent to -m\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      fputs (_("\
\n\
Note that the -d and -t options accept different time-date formats.\n\
"), stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

int
main (int argc, char **argv)
{
  int c;
  bool date_set = false;
  bool ok = true;
  char const *flex_date = NULL;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  change_times = 0;
  no_create = use_ref = false;

  while ((c = getopt_long (argc, argv, "acd:fmr:t:", longopts, NULL)) != -1)
    {
      switch (c)
	{
	case 'a':
	  change_times |= CH_ATIME;
	  break;

	case 'c':
	  no_create = true;
	  break;

	case 'd':
	  flex_date = optarg;
	  break;

	case 'f':
	  break;

	case 'm':
	  change_times |= CH_MTIME;
	  break;

	case 'r':
	  use_ref = true;
	  ref_file = optarg;
	  break;

	case 't':
	  if (! posixtime (&newtime[0].tv_sec, optarg,
			   PDS_LEADING_YEAR | PDS_CENTURY | PDS_SECONDS))
	    error (EXIT_FAILURE, 0, _("invalid date format %s"),
		   quote (optarg));
	  newtime[0].tv_nsec = 0;
	  newtime[1] = newtime[0];
	  date_set = true;
	  break;

	case TIME_OPTION:	/* --time */
	  change_times |= XARGMATCH ("--time", optarg,
				     time_args, time_masks);
	  break;

	case_GETOPT_HELP_CHAR;

	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);

	default:
	  usage (EXIT_FAILURE);
	}
    }

  if (change_times == 0)
    change_times = CH_ATIME | CH_MTIME;

  if (date_set && (use_ref || flex_date))
    {
      error (0, 0, _("cannot specify times from more than one source"));
      usage (EXIT_FAILURE);
    }

  if (use_ref)
    {
      struct stat ref_stats;
      if (stat (ref_file, &ref_stats))
	error (EXIT_FAILURE, errno,
	       _("failed to get attributes of %s"), quote (ref_file));
      newtime[0] = get_stat_atime (&ref_stats);
      newtime[1] = get_stat_mtime (&ref_stats);
      date_set = true;
      if (flex_date)
	{
	  if (change_times & CH_ATIME)
	    get_reldate (&newtime[0], flex_date, &newtime[0]);
	  if (change_times & CH_MTIME)
	    get_reldate (&newtime[1], flex_date, &newtime[1]);
	}
    }
  else
    {
      if (flex_date)
	{
	  struct timespec now;
	  gettime (&now);
	  get_reldate (&newtime[0], flex_date, &now);
	  newtime[1] = newtime[0];
	  date_set = true;

	  /* If neither -a nor -m is specified, treat "-d now" as if
	     it were absent; this lets "touch" succeed more often in
	     the presence of restrictive permissions.  */
	  if (change_times == (CH_ATIME | CH_MTIME)
	      && newtime[0].tv_sec == now.tv_sec
	      && newtime[0].tv_nsec == now.tv_nsec)
	    {
	      /* Check that it really was "-d now", and not a time
		 stamp that just happens to be the current time.  */
	      struct timespec notnow, notnow1;
	      notnow.tv_sec = now.tv_sec ^ 1;
	      notnow.tv_nsec = now.tv_nsec;
	      get_reldate (&notnow1, flex_date, &notnow);
	      if (notnow1.tv_sec == notnow.tv_sec
		  && notnow1.tv_nsec == notnow.tv_nsec)
		date_set = false;
	    }
	}
    }

  /* The obsolete `MMDDhhmm[YY]' form is valid IFF there are
     two or more non-option arguments.  */
  if (!date_set && 2 <= argc - optind && posix2_version () < 200112
      && posixtime (&newtime[0].tv_sec, argv[optind],
		    PDS_TRAILING_YEAR | PDS_PRE_2000))
    {
      newtime[0].tv_nsec = 0;
      newtime[1] = newtime[0];
      date_set = true;

      if (! getenv ("POSIXLY_CORRECT"))
	{
	  struct tm const *tm = localtime (&newtime[0].tv_sec);
	  error (0, 0,
		 _("warning: `touch %s' is obsolete; use "
		   "`touch -t %04ld%02d%02d%02d%02d.%02d'"),
		 argv[optind],
		 tm->tm_year + 1900L, tm->tm_mon + 1, tm->tm_mday,
		 tm->tm_hour, tm->tm_min, tm->tm_sec);
	}

      optind++;
    }

  if (!date_set)
    {
      if (change_times == (CH_ATIME | CH_MTIME))
	amtime_now = true;
      else
	{
	  gettime (&newtime[0]);
	  newtime[1] = newtime[0];
	}
    }

  if (optind == argc)
    {
      error (0, 0, _("missing file operand"));
      usage (EXIT_FAILURE);
    }

  for (; optind < argc; ++optind)
    ok &= touch (argv[optind]);

  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}
