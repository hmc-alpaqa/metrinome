# printf-frexpl.m4 serial 5
dnl Copyright (C) 2007 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

dnl Check how to define printf_frexpl() without linking with libm.

AC_DEFUN([gl_FUNC_PRINTF_FREXPL],
[
  AC_REQUIRE([gl_MATH_H_DEFAULTS])
  dnl Subset of gl_FUNC_FREXPL_NO_LIBM.
  AC_CACHE_CHECK([whether frexpl can be used without linking with libm],
    [gl_cv_func_frexpl_no_libm],
    [
      AC_TRY_LINK([#include <math.h>
                   long double x;
                   int y;],
                  [return frexpl (x, &y) < 1;],
        [gl_cv_func_frexpl_no_libm=yes],
        [gl_cv_func_frexpl_no_libm=no])
    ])
  if test $gl_cv_func_frexpl_no_libm = yes; then
    gl_FUNC_FREXPL_WORKS
    case "$gl_cv_func_frexpl_works" in
      *yes) gl_func_frexpl_no_libm=yes ;;
      *)    gl_func_frexpl_no_libm=no; REPLACE_FREXPL=1 ;;
    esac
  else
    gl_func_frexpl_no_libm=no
    dnl Set REPLACE_FREXPL here because the system may have frexpl in libm.
    REPLACE_FREXPL=1
  fi
  if test $gl_func_frexpl_no_libm = yes; then
    AC_DEFINE([HAVE_FREXPL_IN_LIBC], 1,
      [Define if the frexpl function is available in libc.])
    dnl Also check whether it's declared.
    dnl MacOS X 10.3 has frexpl() in libc but doesn't declare it in <math.h>.
    AC_CHECK_DECL([frexpl], , [HAVE_DECL_FREXPL=0], [#include <math.h>])
  fi

  AC_CACHE_CHECK([whether ldexpl can be used without linking with libm],
    [gl_cv_func_ldexpl_no_libm],
    [
      AC_TRY_LINK([#include <math.h>
                   long double x;
                   int y;],
                  [return ldexpl (x, y) < 1;],
        [gl_cv_func_ldexpl_no_libm=yes],
        [gl_cv_func_ldexpl_no_libm=no])
    ])
  if test $gl_cv_func_ldexpl_no_libm = yes; then
    gl_FUNC_LDEXPL_WORKS
    case "$gl_cv_func_ldexpl_works" in
      *yes)
        AC_DEFINE([HAVE_LDEXPL_IN_LIBC], 1,
          [Define if the ldexpl function is available in libc.])
        dnl Also check whether it's declared.
        dnl MacOS X 10.3 has ldexpl() in libc but doesn't declare it in <math.h>.
        AC_CHECK_DECL([ldexpl], , [HAVE_DECL_LDEXPL=0], [#include <math.h>])
        ;;
    esac
  fi
])
