# serial 9
# See if we need to provide mkfifo replacement.

dnl Copyright (C) 2009-2020 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

# Written by Eric Blake.

AC_DEFUN([gl_FUNC_MKFIFO],
[
  AC_REQUIRE([gl_SYS_STAT_H_DEFAULTS])
  AC_REQUIRE([AC_CANONICAL_HOST]) dnl for cross-compiles

  dnl We can't use AC_CHECK_FUNC here, because mkfifo() is defined as a
  dnl static inline function when compiling for Android 4.4 or older.
  AC_CACHE_CHECK([for mkfifo], [gl_cv_func_mkfifo],
    [AC_LINK_IFELSE(
       [AC_LANG_PROGRAM(
          [[#include <sys/stat.h>]],
          [[return mkfifo("/",0);]])
       ],
       [gl_cv_func_mkfifo=yes],
       [gl_cv_func_mkfifo=no])
    ])
  if test $gl_cv_func_mkfifo = no; then
    HAVE_MKFIFO=0
  else
    AC_DEFINE([HAVE_MKFIFO], [1],
      [Define to 1 if you have a 'mkfifo' function.])
    dnl Check for Solaris 9 and FreeBSD bug with trailing slash.
    AC_CHECK_FUNCS_ONCE([lstat])
    AC_CACHE_CHECK([whether mkfifo rejects trailing slashes],
      [gl_cv_func_mkfifo_works],
      [# Assume that if we have lstat, we can also check symlinks.
       if test $ac_cv_func_lstat = yes; then
         ln -s conftest.tmp conftest.lnk
       fi
       AC_RUN_IFELSE(
         [AC_LANG_PROGRAM(
           [[#include <sys/stat.h>
           ]],
           [[int result = 0;
             if (!mkfifo ("conftest.tmp/", 0600))
               result |= 1;
#if HAVE_LSTAT
             if (!mkfifo ("conftest.lnk/", 0600))
               result |= 2;
#endif
             return result;
           ]])],
         [gl_cv_func_mkfifo_works=yes], [gl_cv_func_mkfifo_works=no],
         [case "$host_os" in
                             # Guess yes on Linux systems.
            linux-* | linux) gl_cv_func_mkfifo_works="guessing yes" ;;
                             # Guess yes on glibc systems.
            *-gnu* | gnu*)   gl_cv_func_mkfifo_works="guessing yes" ;;
                             # If we don't know, obey --enable-cross-guesses.
            *)               gl_cv_func_mkfifo_works="$gl_cross_guess_normal" ;;
          esac
         ])
       rm -f conftest.tmp conftest.lnk])
    case "$gl_cv_func_mkfifo_works" in
      *yes) ;;
      *)
        AC_DEFINE([MKFIFO_TRAILING_SLASH_BUG], [1], [Define to 1 if mkfifo
          does not reject trailing slash])
        REPLACE_MKFIFO=1
        ;;
    esac
  fi
])
