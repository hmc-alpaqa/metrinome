# c-strtod.m4 serial 18

# Copyright (C) 2004-2006, 2009-2020 Free Software Foundation, Inc.
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# Written by Paul Eggert.

dnl Prerequisites of lib/c-strtod.c.
AC_DEFUN([gl_C_STRTOD],
[
  AC_REQUIRE([gl_USE_SYSTEM_EXTENSIONS])
  AC_REQUIRE([gt_FUNC_USELOCALE])

  AC_CHECK_HEADERS_ONCE([xlocale.h])
  dnl We can't use AC_CHECK_FUNC here, because strtod_l() is defined as a
  dnl static inline function when compiling for Android 7.1 or older.
  AC_CACHE_CHECK([for strtod_l], [gl_cv_func_strtod_l],
    [AC_LINK_IFELSE(
       [AC_LANG_PROGRAM(
          [[#include <stdlib.h>
            #include <locale.h>
            #if HAVE_XLOCALE_H
            # include <xlocale.h>
            #endif
            locale_t loc;
          ]],
          [[char *end;
            return strtod_l("0",&end,loc) < 0.0;
          ]])
       ],
       [gl_cv_func_strtod_l=yes],
       [gl_cv_func_strtod_l=no])
    ])
  if test $gl_cv_func_strtod_l = yes; then
    HAVE_STRTOD_L=1
  else
    HAVE_STRTOD_L=0
  fi
  AC_DEFINE_UNQUOTED([HAVE_STRTOD_L], [$HAVE_STRTOD_L],
    [Define to 1 if the system has the 'strtod_l' function.])
])

dnl Prerequisites of lib/c-strtold.c.
AC_DEFUN([gl_C_STRTOLD],
[
  AC_REQUIRE([gl_USE_SYSTEM_EXTENSIONS])
  AC_REQUIRE([gt_FUNC_USELOCALE])
  AC_CHECK_FUNCS([strtold_l])
])
