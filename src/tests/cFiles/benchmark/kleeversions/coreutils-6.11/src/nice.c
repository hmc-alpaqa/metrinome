/* nice -- run a program with modified niceness
   Copyright (C) 1990-2005, 2007 Free Software Foundation, Inc.

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

/* David MacKenzie <djm@gnu.ai.mit.edu> */

#include <config.h>
#include <stdio.h>
#include <getopt.h>
#include <sys/types.h>

#include "system.h"

#if ! HAVE_NICE
/* Include this after "system.h" so we're sure to have definitions
   (from time.h or sys/time.h) required for e.g. the ru_utime member.  */
# include <sys/resource.h>
#endif

#include "error.h"
#include "long-options.h"
#include "quote.h"
#include "xstrtol.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "nice"

#define AUTHORS "David MacKenzie"

#if HAVE_NICE
# define GET_NICENESS() nice (0)
#else
# define GET_NICENESS() getpriority (PRIO_PROCESS, 0)
#endif

#ifndef NZERO
# define NZERO 20
#endif

/* This is required for Darwin Kernel Version 7.7.0.  */
#if NZERO == 0
# undef  NZERO
# define NZERO 20
#endif

/* The name this program was run with. */
char *program_name;

static struct option const longopts[] =
{
  {"adjustment", required_argument, NULL, 'n'},
  {NULL, 0, NULL, 0}
};

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, _("Try `%s --help' for more information.\n"),
	     program_name);
  else
    {
      printf (_("Usage: %s [OPTION] [COMMAND [ARG]...]\n"), program_name);
      printf (_("\
Run COMMAND with an adjusted niceness, which affects process scheduling.\n\
With no COMMAND, print the current niceness.  Nicenesses range from\n\
%d (most favorable scheduling) to %d (least favorable).\n\
\n\
  -n, --adjustment=N   add integer N to the niceness (default 10)\n\
"),
	      - NZERO, NZERO - 1);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      printf (USAGE_BUILTIN_WARNING, PROGRAM_NAME);
      emit_bug_reporting_address ();
    }
  exit (status);
}

int
main (int argc, char **argv)
{
  int current_niceness;
  int adjustment = 10;
  char const *adjustment_given = NULL;
  bool ok;
  int i;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  initialize_exit_failure (EXIT_FAILURE);
  atexit (close_stdout);

  parse_long_options (argc, argv, PROGRAM_NAME, PACKAGE_NAME, VERSION,
		      usage, AUTHORS, (char const *) NULL);

  for (i = 1; i < argc; /* empty */)
    {
      char const *s = argv[i];

      if (s[0] == '-' && ISDIGIT (s[1 + (s[1] == '-' || s[1] == '+')]))
	{
	  adjustment_given = s + 1;
	  ++i;
	}
      else
	{
	  int optc;
	  int fake_argc = argc - (i - 1);
	  char **fake_argv = argv + (i - 1);

	  /* Ensure that any getopt diagnostics use the right name.  */
	  fake_argv[0] = program_name;

	  /* Initialize getopt_long's internal state.  */
	  optind = 0;

	  optc = getopt_long (fake_argc, fake_argv, "+n:", longopts, NULL);
	  i += optind - 1;

	  if (optc == '?')
	    usage (EXIT_FAILURE);
	  else if (optc == 'n')
	    adjustment_given = optarg;
	  else /* optc == -1 */
	    break;
	}
    }

  if (adjustment_given)
    {
      /* If the requested adjustment is outside the valid range,
	 silently bring it to just within range; this mimics what
	 "setpriority" and "nice" do.  */
      enum { MIN_ADJUSTMENT = 1 - 2 * NZERO, MAX_ADJUSTMENT = 2 * NZERO - 1 };
      long int tmp;
      if (LONGINT_OVERFLOW < xstrtol (adjustment_given, NULL, 10, &tmp, ""))
	error (EXIT_FAILURE, 0, _("invalid adjustment %s"),
	       quote (adjustment_given));
      adjustment = MAX (MIN_ADJUSTMENT, MIN (tmp, MAX_ADJUSTMENT));
    }

  if (i == argc)
    {
      if (adjustment_given)
	{
	  error (0, 0, _("a command must be given with an adjustment"));
	  usage (EXIT_FAILURE);
	}
      /* No command given; print the niceness.  */
      errno = 0;
      current_niceness = GET_NICENESS ();
      if (current_niceness == -1 && errno != 0)
	error (EXIT_FAILURE, errno, _("cannot get niceness"));
      printf ("%d\n", current_niceness);
      exit (EXIT_SUCCESS);
    }

  errno = 0;
#if HAVE_NICE
  ok = (nice (adjustment) != -1 || errno == 0);
#else
  current_niceness = GET_NICENESS ();
  if (current_niceness == -1 && errno != 0)
    error (EXIT_FAILURE, errno, _("cannot get niceness"));
  ok = (setpriority (PRIO_PROCESS, 0, current_niceness + adjustment) == 0);
#endif
  if (!ok)
    error (errno == EPERM ? 0 : EXIT_FAILURE, errno, _("cannot set niceness"));

  execvp (argv[i], &argv[i]);

  {
    int exit_status = (errno == ENOENT ? EXIT_ENOENT : EXIT_CANNOT_INVOKE);
    error (0, errno, "%s", argv[i]);
    exit (exit_status);
  }
}
