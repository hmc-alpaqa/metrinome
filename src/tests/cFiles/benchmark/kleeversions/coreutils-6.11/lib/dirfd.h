/* Declare dirfd, if necessary.
   Copyright (C) 2001, 2002, 2006 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

   Written by Jim Meyering.  */

#include <sys/types.h>

#include <dirent.h>

#ifndef HAVE_DECL_DIRFD
"this configure-time declaration test was not run"
#endif
#if !HAVE_DECL_DIRFD && !defined dirfd
int dirfd (DIR const *);
#endif
