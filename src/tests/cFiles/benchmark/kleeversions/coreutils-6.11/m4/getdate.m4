# getdate.m4 serial 12
dnl Copyright (C) 2002, 2003, 2004, 2005, 2006 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_C_COMPOUND_LITERALS],
[
  AC_CACHE_CHECK([for compound literals], gl_cv_compound_literals,
  [AC_TRY_COMPILE([struct s { int i, j; }; struct s s = (struct s) { 1, 2 };],
    [struct s t = (struct s) { 3, 4 };
     if (t.i != 0) return 0;],
    gl_cv_compound_literals=yes,
    gl_cv_compound_literals=no)])
  if test $gl_cv_compound_literals = yes; then
    AC_DEFINE(HAVE_COMPOUND_LITERALS, 1,
      [Define if you have compound literals.])
  fi
])

AC_DEFUN([gl_GETDATE],
[
  dnl Prerequisites of lib/getdate.h.
  AC_REQUIRE([AM_STDBOOL_H])
  AC_REQUIRE([gl_TIMESPEC])

  dnl Prerequisites of lib/getdate.y.
  AC_REQUIRE([gl_BISON])
  AC_REQUIRE([gl_C_COMPOUND_LITERALS])
  AC_STRUCT_TIMEZONE
  AC_REQUIRE([gl_CLOCK_TIME])
  AC_REQUIRE([gl_TM_GMTOFF])
])
