/* -*- buffer-read-only: t -*- vi: set ro: */
/* DO NOT EDIT! GENERATED AUTOMATICALLY! */
#line 1
/* An fseeko() function that, together with fflush(), is POSIX compliant.
   Copyright (C) 2007-2008 Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  */

#include <config.h>

/* Specification.  */
#include <stdio.h>

/* Get off_t and lseek.  */
#include <unistd.h>

#undef fseeko
#if !HAVE_FSEEKO
# undef fseek
# define fseeko fseek
#endif

int
rpl_fseeko (FILE *fp, off_t offset, int whence)
{
#if LSEEK_PIPE_BROKEN
  /* mingw gives bogus answers rather than failure on non-seekable files.  */
  if (lseek (fileno (fp), 0, SEEK_CUR) == -1)
    return EOF;
#endif

  /* These tests are based on fpurge.c.  */
#if defined _IO_ferror_unlocked || __GNU_LIBRARY__ == 1 /* GNU libc, BeOS, Linux libc5 */
  if (fp->_IO_read_end == fp->_IO_read_ptr
      && fp->_IO_write_ptr == fp->_IO_write_base
      && fp->_IO_save_base == NULL)
#elif defined __sferror             /* FreeBSD, NetBSD, OpenBSD, MacOS X, Cygwin */
# if defined __NetBSD__ || defined __OpenBSD__ /* NetBSD, OpenBSD */
   /* See <http://cvsweb.netbsd.org/bsdweb.cgi/src/lib/libc/stdio/fileext.h?rev=HEAD&content-type=text/x-cvsweb-markup>
      and <http://www.openbsd.org/cgi-bin/cvsweb/src/lib/libc/stdio/fileext.h?rev=HEAD&content-type=text/x-cvsweb-markup> */
#  define fp_ub ((struct { struct __sbuf _ub; } *) fp->_ext._base)->_ub
# else                                         /* FreeBSD, MacOS X, Cygwin */
#  define fp_ub fp->_ub
# endif
# if defined __SL64 && defined __SCLE /* Cygwin */
  if ((fp->_flags & __SL64) == 0)
    {
      /* Cygwin 1.5.0 through 1.5.24 failed to open stdin in 64-bit
	 mode; but has an fseeko that requires 64-bit mode.  */
      FILE *tmp = fopen ("/dev/null", "r");
      if (!tmp)
	return -1;
      fp->_flags |= __SL64;
      fp->_seek64 = tmp->_seek64;
      fclose (tmp);
    }
# endif
  if (fp->_p == fp->_bf._base
      && fp->_r == 0
      && fp->_w == ((fp->_flags & (__SLBF | __SNBF | __SRD)) == 0 /* fully buffered and not currently reading? */
		    ? fp->_bf._size
		    : 0)
      && fp_ub._base == NULL)
#elif defined __EMX__               /* emx+gcc */
  if (fp->_ptr == fp->_buffer
      && fp->_rcount == 0
      && fp->_wcount == 0
      && fp->_ungetc_count == 0)
#elif defined _IOERR                /* AIX, HP-UX, IRIX, OSF/1, Solaris, OpenServer, mingw */
# if defined __sun && defined _LP64 /* Solaris/{SPARC,AMD64} 64-bit */
#  define fp_ ((struct { unsigned char *_ptr; \
			 unsigned char *_base; \
			 unsigned char *_end; \
			 long _cnt; \
			 int _file; \
			 unsigned int _flag; \
		       } *) fp)
  if (fp_->_ptr == fp_->_base
      && (fp_->_ptr == NULL || fp_->_cnt == 0))
# else
#  if defined _SCO_DS               /* OpenServer */
#   define _base __base
#   define _ptr __ptr
#   define _cnt __cnt
#  endif
  if (fp->_ptr == fp->_base
      && (fp->_ptr == NULL || fp->_cnt == 0))
# endif
#elif defined __UCLIBC__            /* uClibc */
  if (((fp->__modeflags & __FLAG_WRITING) == 0
       || fp->__bufpos == fp->__bufstart)
      && ((fp->__modeflags & (__FLAG_READONLY | __FLAG_READING)) == 0
	  || fp->__bufpos == fp->__bufread))
#elif defined __QNX__               /* QNX */
  if ((fp->_Mode & _MWRITE ? fp->_Next == fp->_Buf : fp->_Next == fp->_Rend)
      && fp->_Rback == fp->_Back + sizeof (fp->_Back)
      && fp->_Rsave == NULL)
#else
  #error "Please port gnulib fseeko.c to your platform! Look at the code in fpurge.c, then report this to bug-gnulib."
#endif
    {
      off_t pos = lseek (fileno (fp), offset, whence);
      if (pos == -1)
	{
#if defined __sferror               /* FreeBSD, NetBSD, OpenBSD, MacOS X, Cygwin */
	  fp->_flags &= ~__SOFF;
#endif
	  return -1;
	}
      else
	{
#if defined __sferror               /* FreeBSD, NetBSD, OpenBSD, MacOS X, Cygwin */
	  fp->_offset = pos;
	  fp->_flags |= __SOFF;
	  fp->_flags &= ~__SEOF;
#elif defined __EMX__               /* emx+gcc */
          fp->_flags &= ~_IOEOF;
#elif defined _IOERR                /* AIX, HP-UX, IRIX, OSF/1, Solaris, OpenServer, mingw */
# if defined _SCO_DS                /* OpenServer */
#  define _flag __flag
# endif
          fp->_flag &= ~_IOEOF;
#endif
	  return 0;
	}
    }
  else
    return fseeko (fp, offset, whence);
}
