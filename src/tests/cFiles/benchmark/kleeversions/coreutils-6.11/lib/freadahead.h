/* Retrieve information about a FILE stream.
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

#include <stddef.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Assuming the stream STREAM is open for reading:
   Return the number of bytes waiting in the input buffer of STREAM.
   This includes both the bytes that have been read from the underlying input
   source and the bytes that have been pushed back through 'ungetc'.

   If this number is 0 and the stream is not currently writing,
   fflush (STREAM) is known to be a no-op.

   STREAM must not be wide-character oriented.  */

extern size_t freadahead (FILE *stream);

#ifdef __cplusplus
}
#endif
