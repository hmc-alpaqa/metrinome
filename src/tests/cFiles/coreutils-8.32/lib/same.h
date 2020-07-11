/* Determine whether two file names refer to the same file.

   Copyright (C) 1997-2000, 2003-2004, 2009-2020 Free Software Foundation, Inc.

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

#ifndef SAME_H_
# define SAME_H_ 1

# include <stdbool.h>

bool same_name (const char *source, const char *dest);
bool same_nameat (int, char const *, int, char const *);

#endif /* SAME_H_ */
