/* Rename a file relative to open directories.
   Copyright 2017-2020 Free Software Foundation, Inc.

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

/* written by Paul Eggert */

/* Get RENAME_* macros from <stdio.h> if present, otherwise supply
   the traditional Linux values.  */
#include <stdio.h>
#ifndef RENAME_NOREPLACE
# define RENAME_NOREPLACE  (1 << 0)
# define RENAME_EXCHANGE   (1 << 1)
# define RENAME_WHITEOUT   (1 << 2)
#endif

extern int renameatu (int, char const *, int, char const *, unsigned int);
