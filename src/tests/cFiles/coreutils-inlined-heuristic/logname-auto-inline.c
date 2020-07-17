/* logname -- print user's login name
   Copyright (C) 1990-2020 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

#include <config.h>
#include <stdio.h>
#include <sys/types.h>

#include "die.h"
#include "error.h"
#include "long-options.h"
#include "quote.h"
#include "system.h"

/* The official name of this program (e.g., no 'g' prefix).  */
#define PROGRAM_NAME "logname"

#define AUTHORS proper_name("FIXME: unknown")

__attribute__((always_inline)) inline void usage(int status) {
  if (status != EXIT_SUCCESS)
    emit_try_help();
  else {
    printf(_("Usage: %s [OPTION]\n"), program_name);
    fputs(_("\
Print the name of the current user.\n\
\n\
"),
          stdout);
    fputs(HELP_OPTION_DESCRIPTION, stdout);
    fputs(VERSION_OPTION_DESCRIPTION, stdout);
    emit_ancillary_info(PROGRAM_NAME);
  }
  exit(status);
}

int main(int argc, char **argv) {
  char *cp;

  initialize_main(&argc, &argv);
  set_program_name(argv[0]);
  setlocale(LC_ALL, "");
  bindtextdomain(PACKAGE, LOCALEDIR);
  textdomain(PACKAGE);

  atexit(close_stdout);

  parse_gnu_standard_options_only(argc, argv, PROGRAM_NAME, PACKAGE_NAME,
                                  Version, true, usage, AUTHORS,
                                  (char const *)NULL);

  if (optind < argc) {
    error(0, 0, _("extra operand %s"), quote(argv[optind]));
    usage(EXIT_FAILURE);
  }

  /* POSIX requires using getlogin (or equivalent code) and prohibits
     using a fallback technique.  */
  cp = getlogin();
  if (!cp) die(EXIT_FAILURE, 0, _("no login name"));

  puts(cp);
  return EXIT_SUCCESS;
}