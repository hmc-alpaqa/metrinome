#serial 23
# Check declarations for this package.

dnl Copyright (C) 1997, 1998, 1999, 2000, 2001, 2003, 2004, 2005, 2006
dnl Free Software Foundation, Inc.

dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.


dnl This is just a wrapper function to encapsulate this kludge.
dnl Putting it in a separate file like this helps share it between
dnl different packages.
AC_DEFUN([gl_CHECK_DECLS],
[
  AC_REQUIRE([AC_HEADER_TIME])

  AC_CHECK_HEADERS_ONCE(grp.h pwd.h)
  headers='
#include <sys/types.h>

#include <unistd.h>

#if HAVE_GRP_H
# include <grp.h>
#endif

#if HAVE_PWD_H
# include <pwd.h>
#endif
'
  AC_CHECK_DECLS([
    getgrgid,
    getpwuid,
    ttyname], , , $headers)

  AC_CHECK_DECLS([isblank], [], [], [#include <ctype.h>])

  AC_CHECK_DECLS_ONCE([free])
  AC_CHECK_DECLS_ONCE([getenv])
  AC_CHECK_DECLS_ONCE([geteuid])
  AC_CHECK_DECLS_ONCE([getlogin])
  AC_CHECK_DECLS_ONCE([getuid])
  AC_CHECK_DECLS_ONCE([lseek])
  AC_CHECK_DECLS_ONCE([malloc])
  AC_CHECK_DECLS_ONCE([memchr])
  AC_CHECK_DECLS_ONCE([realloc])
])
