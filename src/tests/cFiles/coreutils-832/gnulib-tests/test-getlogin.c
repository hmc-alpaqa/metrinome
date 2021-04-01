/* Test of getting user name.
   Copyright (C) 2010-2020 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* Written by Bruno Haible and Paul Eggert.  */

#include <config.h>

#include <unistd.h>

#include "signature.h"
SIGNATURE_CHECK (getlogin, char *, (void));

#include "test-getlogin.h"

int
main (void)
{
  /* Test value.  */
  char *buf = getlogin ();
  int err = buf ? 0 : errno;
  ASSERT (buf || err);
  test_getlogin_result (buf, err);

  return 0;
}
