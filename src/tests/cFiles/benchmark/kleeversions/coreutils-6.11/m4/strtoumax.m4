# strtoumax.m4 serial 6
dnl Copyright (C) 2002, 2003, 2004, 2006 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_FUNC_STRTOUMAX],
[
  dnl Work around a bug of AC_EGREP_CPP in autoconf-2.57.
  AC_REQUIRE([AC_PROG_CPP])
  AC_REQUIRE([AC_PROG_EGREP])

  AC_CACHE_CHECK([whether <inttypes.h> defines strtoumax as a macro],
    gl_cv_func_strtoumax_macro,
    [AC_EGREP_CPP([inttypes_h_defines_strtoumax], [#include <inttypes.h>
#ifdef strtoumax
 inttypes_h_defines_strtoumax
#endif],
       gl_cv_func_strtoumax_macro=yes,
       gl_cv_func_strtoumax_macro=no)])

  if test "$gl_cv_func_strtoumax_macro" != yes; then
    AC_REPLACE_FUNCS(strtoumax)
    if test $ac_cv_func_strtoumax = no; then
      gl_PREREQ_STRTOUMAX
    fi
  fi
])

# Prerequisites of lib/strtoumax.c.
AC_DEFUN([gl_PREREQ_STRTOUMAX], [
  AC_CHECK_DECLS(strtoull)
  AC_REQUIRE([AC_TYPE_UNSIGNED_LONG_LONG_INT])
])
