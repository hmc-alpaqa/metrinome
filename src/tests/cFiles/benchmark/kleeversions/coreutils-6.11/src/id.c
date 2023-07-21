/* id -- print real and effective UIDs and GIDs
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

/* Written by Arnold Robbins.
   Major rewrite by David MacKenzie, djm@gnu.ai.mit.edu. */

#include <config.h>
#include <stdio.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>
#include <getopt.h>
#include <selinux/selinux.h>

#include "system.h"
#include "error.h"
#include "mgetgroups.h"
#include "quote.h"
#include "group-list.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "id"

#define AUTHORS "Arnold Robbins", "David MacKenzie"

/* If nonzero, output only the SELinux context. -Z */
static int just_context = 0;

static void print_user (uid_t uid);
static void print_full_info (const char *username);

/* The name this program was run with. */
char *program_name;

/* If true, output user/group name instead of ID number. -n */
static bool use_name = false;

/* The real and effective IDs of the user to print. */
static uid_t ruid, euid;
static gid_t rgid, egid;

/* True unless errors have been encountered.  */
static bool ok = true;

/* The SELinux context.  Start with a known invalid value so print_full_info
   knows when `context' has not been set to a meaningful value.  */
static security_context_t context = NULL;

static struct option const longopts[] =
{
  {"context", no_argument, NULL, 'Z'},
  {"group", no_argument, NULL, 'g'},
  {"groups", no_argument, NULL, 'G'},
  {"name", no_argument, NULL, 'n'},
  {"real", no_argument, NULL, 'r'},
  {"user", no_argument, NULL, 'u'},
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
Print information for USERNAME, or the current user.\n\
\n\
  -a              ignore, for compatibility with other versions\n\
  -Z, --context   print only the security context of the current user\n\
  -g, --group     print only the effective group ID\n\
  -G, --groups    print all group IDs\n\
  -n, --name      print a name instead of a number, for -ugG\n\
  -r, --real      print the real ID instead of the effective ID, with -ugG\n\
  -u, --user      print only the effective user ID\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      fputs (_("\
\n\
Without any OPTION, print some useful set of identified information.\n\
"), stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

int
main (int argc, char **argv)
{
  int optc;
  int selinux_enabled = (is_selinux_enabled () > 0);

  /* If true, output the list of all group IDs. -G */
  bool just_group_list = false;
  /* If true, output only the group ID(s). -g */
  bool just_group = false;
  /* If true, output real UID/GID instead of default effective UID/GID. -r */
  bool use_real = false;
  /* If true, output only the user ID(s). -u */
  bool just_user = false;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  while ((optc = getopt_long (argc, argv, "agnruGZ", longopts, NULL)) != -1)
    {
      switch (optc)
	{
	case 'a':
	  /* Ignore -a, for compatibility with SVR4.  */
	  break;

        case 'Z':
	  /* politely decline if we're not on a selinux-enabled kernel. */
	  if (!selinux_enabled)
	    error (EXIT_FAILURE, 0,
		   _("--context (-Z) works only on an SELinux-enabled kernel"));
          just_context = 1;
          break;

	case 'g':
	  just_group = true;
	  break;
	case 'n':
	  use_name = true;
	  break;
	case 'r':
	  use_real = true;
	  break;
	case 'u':
	  just_user = true;
	  break;
	case 'G':
	  just_group_list = true;
	  break;
	case_GETOPT_HELP_CHAR;
	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);
	default:
	  usage (EXIT_FAILURE);
	}
    }

  if (1 < argc - optind)
    {
      error (0, 0, _("extra operand %s"), quote (argv[optind + 1]));
      usage (EXIT_FAILURE);
    }

  if (argc - optind == 1 && just_context)
    error (EXIT_FAILURE, 0,
	   _("cannot print security context when user specified"));

  if (just_context && !selinux_enabled)
    error (EXIT_FAILURE, 0, _("\
cannot display context when selinux not enabled or when displaying the id\n\
of a different user"));

  /* If we are on a selinux-enabled kernel, get our context.
     Otherwise, leave the context variable alone - it has
     been initialized known invalid value; if we see this invalid
     value later, we will know we are on a non-selinux kernel.  */
  if (selinux_enabled)
    {
      if (getcon (&context) && just_context)
        error (EXIT_FAILURE, 0, _("can't get process context"));
    }

  if (just_user + just_group + just_group_list + just_context > 1)
    error (EXIT_FAILURE, 0, _("cannot print \"only\" of more than one choice"));

  if (just_user + just_group + just_group_list == 0 && (use_real | use_name))
    error (EXIT_FAILURE, 0,
	   _("cannot print only names or real IDs in default format"));

  char const *user_name;
  if (argc - optind == 1)
    {
      struct passwd const *pwd = getpwnam (argv[optind]);
      if (pwd == NULL)
	error (EXIT_FAILURE, 0, _("%s: No such user"), argv[optind]);
      user_name = argv[optind];
      ruid = euid = pwd->pw_uid;
      rgid = egid = pwd->pw_gid;
    }
  else
    {
      struct passwd const *pwd;
      euid = geteuid ();
      pwd = getpwuid (euid);
      user_name = pwd ? xstrdup (pwd->pw_name) : NULL;
      ruid = getuid ();
      egid = getegid ();
      rgid = getgid ();
    }

  if (just_user)
    {
      print_user (use_real ? ruid : euid);
    }
  else if (just_group)
    {
      if (!print_group (use_real ? rgid : egid, use_name))
	ok = false;
    }
  else if (just_group_list)
    {
      if (!print_group_list (user_name, ruid, rgid, egid, use_name))
	ok = false;
    }
  else if (just_context)
    {
      fputs (context, stdout);
    }
  else
    {
      print_full_info (user_name);
    }
  putchar ('\n');

  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}

/* Print the name or value of user ID UID. */

static void
print_user (uid_t uid)
{
  struct passwd *pwd = NULL;

  if (use_name)
    {
      pwd = getpwuid (uid);
      if (pwd == NULL)
	{
	  error (0, 0, _("cannot find name for user ID %lu"),
		 (unsigned long int) uid);
	  ok = false;
	}
    }

  if (pwd == NULL)
    printf ("%lu", (unsigned long int) uid);
  else
    printf ("%s", pwd->pw_name);
}

/* Print all of the info about the user's user and group IDs. */

static void
print_full_info (const char *username)
{
  struct passwd *pwd;
  struct group *grp;

  printf ("uid=%lu", (unsigned long int) ruid);
  pwd = getpwuid (ruid);
  if (pwd)
    printf ("(%s)", pwd->pw_name);

  printf (" gid=%lu", (unsigned long int) rgid);
  grp = getgrgid (rgid);
  if (grp)
    printf ("(%s)", grp->gr_name);

  if (euid != ruid)
    {
      printf (" euid=%lu", (unsigned long int) euid);
      pwd = getpwuid (euid);
      if (pwd)
	printf ("(%s)", pwd->pw_name);
    }

  if (egid != rgid)
    {
      printf (" egid=%lu", (unsigned long int) egid);
      grp = getgrgid (egid);
      if (grp)
	printf ("(%s)", grp->gr_name);
    }

#if HAVE_GETGROUPS
  {
    GETGROUPS_T *groups;
    size_t i;

    int n_groups = mgetgroups (username, (pwd ? pwd->pw_gid : (gid_t) -1),
			       &groups);
    if (n_groups < 0)
      {
	if (username)
	  {
	    error (0, errno, _("failed to get groups for user %s"),
		   quote (username));
	  }
	else
	  {
	    error (0, errno, _("failed to get groups for the current process"));
	  }
	ok = false;
	return;
      }

    if (n_groups > 0)
      fputs (_(" groups="), stdout);
    for (i = 0; i < n_groups; i++)
      {
	if (i > 0)
	  putchar (',');
	printf ("%lu", (unsigned long int) groups[i]);
	grp = getgrgid (groups[i]);
	if (grp)
	  printf ("(%s)", grp->gr_name);
      }
    free (groups);
  }
#endif /* HAVE_GETGROUPS */
  if (context != NULL)
    printf (" context=%s", context);
}
