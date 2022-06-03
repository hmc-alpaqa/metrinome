# sha1.m4 serial 8
dnl Copyright (C) 2002, 2003, 2004, 2005, 2006, 2008 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_SHA1],
[
  AC_LIBOBJ([sha1])

  dnl Prerequisites of lib/sha1.c.
  AC_REQUIRE([AC_C_BIGENDIAN])
  AC_REQUIRE([AC_C_INLINE])
  :
])
