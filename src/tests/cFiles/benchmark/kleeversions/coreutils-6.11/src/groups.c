/* groups -- print the groups a user is in
   Copyright (C) 1989-2008 Free Software Foundation, Inc.

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

/* Written by James Youngman based on id.c and groups.sh,
   which were written by Arnold Robbins and David MacKenzie. */

#include <config.h>
#include <stdio.h>
#include <getopt.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>
#include <getopt.h>

#include "system.h"
#include "error.h"
#include "group-list.h"

/* The name this program was run with. */
char *program_name;

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "groups"

#define AUTHORS "David MacKenzie", "James Youngman"


static struct option const longopts[] =
{
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
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
      printf (_("Usage: %s [OPTION]... [USERNAME]\n"), program_name);
      fputs (_("\
Print information for USERNAME or, if no USERNAME is specified,\n\
the current process (which is different if the groups database has changed).\n"),
             stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

int
main (int argc, char **argv)
{
  int optc;
  bool ok = true;
  gid_t rgid, egid;
  uid_t ruid;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  /* Processing the arguments this way makes groups.c behave differently to
   * groups.sh if one of the arguments is "--".
   */
  while ((optc = getopt_long (argc, argv, "", longopts, NULL)) != -1)
    {
      switch (optc)
        {
        case_GETOPT_HELP_CHAR;
        case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);
        default:
          usage (EXIT_FAILURE);
        }
    }

  if (optind == argc)
    {
      /* No arguments.  Divulge the details of the current process. */
      ruid = getuid ();
      egid = getegid ();
      rgid = getgid ();

      if (!print_group_list (getlogin (), ruid, rgid, egid, true))
        ok = false;
      putchar ('\n');
    }
  else
    {
      /* At least one argument.  Divulge the details of the specified users. */
      while (optind < argc)
        {
          struct passwd *pwd = getpwnam (argv[optind]);
          if (pwd == NULL)
            error (EXIT_FAILURE, 0, _("%s: No such user"), argv[optind]);
          ruid = pwd->pw_uid;
          rgid = egid = pwd->pw_gid;

          printf ("%s : ", argv[optind]);
          if (!print_group_list (argv[optind++], ruid, rgid, egid, true))
            ok = false;
          putchar ('\n');
        }
    }

  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}

/*
 * Local variables:
 *  indent-tabs-mode: nil
 * End:
 */
