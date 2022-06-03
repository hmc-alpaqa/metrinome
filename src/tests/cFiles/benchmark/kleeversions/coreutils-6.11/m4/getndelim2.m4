# getndelim2.m4 serial 5
dnl Copyright (C) 2003, 2006 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_GETNDELIM2],
[
  AC_LIBOBJ(getndelim2)
  gl_PREREQ_GETNDELIM2
])

# Prerequisites of lib/getndelim2.h and lib/getndelim2.c.
AC_DEFUN([gl_PREREQ_GETNDELIM2],
[
  dnl Prerequisites of lib/getndelim2.h.
  AC_REQUIRE([gt_TYPE_SSIZE_T])
  dnl No prerequisites of lib/getndelim2.c.
])
