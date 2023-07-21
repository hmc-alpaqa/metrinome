/* -*- buffer-read-only: t -*- vi: set ro: */
/* DO NOT EDIT! GENERATED AUTOMATICALLY! */
#line 1
/* Test of strerror() function.
   Copyright (C) 2007-2008 Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  */

/* Written by Eric Blake <ebb9@byu.net>, 2007.  */

#include <config.h>

#include <errno.h>
#include <stdio.h>
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

int
main (int argc, char **argv)
{
  char *str;
  str = strerror (EACCES);
  ASSERT (str);
  ASSERT (*str);

  str = strerror (0);
  ASSERT (str);
  ASSERT (*str);

  str = strerror (-3);
  ASSERT (str);
  ASSERT (*str);

  return 0;
}
