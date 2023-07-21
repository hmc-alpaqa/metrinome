# filemode.m4 serial 7
dnl Copyright (C) 2002, 2005, 2006 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_FILEMODE],
[
  AC_REQUIRE([AC_STRUCT_ST_DM_MODE])
  AC_LIBOBJ([filemode])
  AC_CHECK_DECLS_ONCE([strmode])
])
