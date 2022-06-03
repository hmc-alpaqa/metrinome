/* fflush.c -- allow flushing input streams
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

/* Written by Eric Blake. */

#include <config.h>

/* Specification.  */
#include <stdio.h>

#include <errno.h>
#include <unistd.h>

#include "freading.h"
#include "fpurge.h"

#undef fflush

/* Flush all pending data on STREAM according to POSIX rules.  Both
   output and seekable input streams are supported.  */
int
rpl_fflush (FILE *stream)
{
  int result;
  off_t pos;

  /* When stream is NULL, POSIX and C99 only require flushing of "output
     streams and update streams in which the most recent operation was not
     input", and all implementations do this.

     When stream is "an output stream or an update stream in which the most
     recent operation was not input", POSIX and C99 requires that fflush
     writes out any buffered data, and all implementations do this.

     When stream is, however, an input stream or an update stream in
     which the most recent operation was input, C99 specifies nothing,
     and POSIX only specifies behavior if the stream is seekable.
     mingw, in particular, drops the input buffer, leaving the file
     descriptor positioned at the end of the input buffer. I.e. ftell
     (stream) is lost.  We don't want to call the implementation's
     fflush in this case.

     We test ! freading (stream) here, rather than fwriting (stream), because
     what we need to know is whether the stream holds a "read buffer", and on
     mingw this is indicated by _IOREAD, regardless of _IOWRT.  */
  if (stream == NULL || ! freading (stream))
    return fflush (stream);

  /* Clear the ungetc buffer.

     This is needed before fetching the file-position indicator, because
     1) The file position indicator is incremented by fgetc() and decremented
        by ungetc():
        <http://www.opengroup.org/susv3/functions/fgetc.html>
          "... the fgetc() function shall ... advance the associated file
           position indicator for the stream ..."
        <http://www.opengroup.org/susv3/functions/ungetc.html>
          "The file-position indicator is decremented by each successful
           call to ungetc()..."
     2) <http://www.opengroup.org/susv3/functions/ungetc.html> says:
          "The value of the file-position indicator for the stream after
           reading or discarding all pushed-back bytes shall be the same
           as it was before the bytes were pushed back."
     3) Here we are discarding all pushed-back bytes.

     Unfortunately it is impossible to implement this on platforms with
     _IOERR, because an ungetc() on this platform prepends the pushed-back
     bytes to the buffer without an indication of the limit between the
     pushed-back bytes and the read-ahead bytes.  */
#if defined __sferror               /* FreeBSD, NetBSD, OpenBSD, MacOS X, Cygwin */
  {
# if defined __NetBSD__ || defined __OpenBSD__
    struct __sfileext
      {
	struct  __sbuf _ub; /* ungetc buffer */
	/* More fields, not relevant here.  */
      };
    if (((struct __sfileext *) stream->_ext._base)->_ub._base != NULL)
# else
    if (stream->_ub._base != NULL)
# endif
      {
	stream->_p += stream->_r;
	stream->_r = 0;
      }
  }
#endif

  /* POSIX does not specify fflush behavior for non-seekable input
     streams.  Some implementations purge unread data, some return
     EBADF, some do nothing.  */
  pos = ftello (stream);
  if (pos == -1)
    {
      errno = EBADF;
      return EOF;
    }

  /* To get here, we must be flushing a seekable input stream, so the
     semantics of fpurge are now appropriate to clear the buffer.  To
     avoid losing data, the lseek is also necessary.  */
  result = fpurge (stream);
  if (result != 0)
    return result;

#if defined __sferror && defined __SNPT /* FreeBSD, NetBSD, OpenBSD, MacOS X, Cygwin */

  {
    /* Disable seek optimization for the next fseeko call.  This tells the
       following fseeko call to seek to the desired position directly, rather
       than to seek to a block-aligned boundary.  */
    int saved_flags = stream->_flags & (__SOPT | __SNPT);
    stream->_flags = (stream->_flags & ~__SOPT) | __SNPT;

    result = fseeko (stream, pos, SEEK_SET);

    stream->_flags = (stream->_flags & ~(__SOPT | __SNPT)) | saved_flags;
  }
  return result;

#else

  pos = lseek (fileno (stream), pos, SEEK_SET);
  if (pos == -1)
    return EOF;
  /* After a successful lseek, update the file descriptor's position cache
     in the stream.  */
# if defined __sferror           /* FreeBSD, NetBSD, OpenBSD, MacOS X, Cygwin */
  stream->_offset = pos;
  stream->_flags |= __SOFF;
# endif

  return 0;

#endif
}
