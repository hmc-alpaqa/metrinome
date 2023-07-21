#serial 5
dnl Copyright (C) 2002, 2005, 2006 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_FUNC_SIG2STR],
[

  AC_REPLACE_FUNCS(sig2str)
  if test $ac_cv_func_sig2str = no; then
    gl_PREREQ_SIG2STR
  fi
])

# Prerequisites of lib/sig2str.c.
AC_DEFUN([gl_PREREQ_SIG2STR], [
  :
])
