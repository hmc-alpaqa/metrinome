#serial 10
dnl Copyright (C) 2002-2003, 2005-2006, 2009-2020 Free Software Foundation,
dnl Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

dnl Prerequisites of lib/same.c.
AC_DEFUN([gl_SAME],
[
  AC_REQUIRE([AC_SYS_LONG_FILE_NAMES])
  AC_CHECK_FUNCS_ONCE([fpathconf])
])
