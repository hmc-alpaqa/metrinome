/* -*- buffer-read-only: t -*- vi: set ro: */
/* DO NOT EDIT! GENERATED AUTOMATICALLY! */
#line 1
/* Test of vasprintf() and asprintf() functions.
   Copyright (C) 2007-2008 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* Written by Bruno Haible <bruno@clisp.org>, 2007.  */

#include <config.h>

#include <stdio.h>

#include <stdarg.h>
#include <stdlib.h>
#include <string.h>

#define ASSERT(expr) \
  do									     \
    {									     \
      if (!(expr))							     \
        {								     \
          fprintf (stderr, "%s:%d: assertion failed\n", __FILE__, __LINE__); \
          fflush (stderr);						     \
          abort ();							     \
        }								     \
    }									     \
  while (0)

static int
my_asprintf (char **result, const char *format, ...)
{
  va_list args;
  int ret;

  va_start (args, format);
  ret = vasprintf (result, format, args);
  va_end (args);
  return ret;
}

static void
test_vasprintf ()
{
  int repeat;

  for (repeat = 0; repeat <= 8; repeat++)
    {
      char *result;
      int retval = my_asprintf (&result, "%d", 12345);
      ASSERT (retval == 5);
      ASSERT (result != NULL);
      ASSERT (strcmp (result, "12345") == 0);
      free (result);
    }
}

static void
test_asprintf ()
{
  int repeat;

  for (repeat = 0; repeat <= 8; repeat++)
    {
      char *result;
      int retval = asprintf (&result, "%d", 12345);
      ASSERT (retval == 5);
      ASSERT (result != NULL);
      ASSERT (strcmp (result, "12345") == 0);
      free (result);
    }
}

int
main (int argc, char *argv[])
{
  test_vasprintf ();
  test_asprintf ();
  return 0;
}
