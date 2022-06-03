#serial 13
dnl Copyright (C) 2002, 2003, 2005, 2006, 2007 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

dnl From Jim Meyering.

# Redefine AC_FUNC_MKTIME, to fix a bug in Autoconf 2.61a and earlier.
# This redefinition can be removed once a new version of Autoconf is assumed.
# The redefinition is taken from
# <http://cvs.sv.gnu.org/viewcvs/*checkout*/autoconf/autoconf/lib/autoconf/functions.m4?rev=1.119>.
# AC_FUNC_MKTIME
# --------------
AC_DEFUN([AC_FUNC_MKTIME],
[AC_CHECK_HEADERS_ONCE(unistd.h)
AC_CHECK_FUNCS_ONCE(alarm)
AC_CACHE_CHECK([for working mktime], ac_cv_func_working_mktime,
[AC_RUN_IFELSE([AC_LANG_SOURCE(
[[/* Test program from Paul Eggert and Tony Leneis.  */
#include <limits.h>
#include <stdlib.h>
#include <time.h>

#ifdef HAVE_UNISTD_H
# include <unistd.h>
#endif

#ifndef HAVE_ALARM
# define alarm(X) /* empty */
#endif

/* Work around redefinition to rpl_putenv by other config tests.  */
#undef putenv

static time_t time_t_max;
static time_t time_t_min;

/* Values we'll use to set the TZ environment variable.  */
static char *tz_strings[] = {
  (char *) 0, "TZ=GMT0", "TZ=JST-9",
  "TZ=EST+3EDT+2,M10.1.0/00:00:00,M2.3.0/00:00:00"
};
#define N_STRINGS (sizeof (tz_strings) / sizeof (tz_strings[0]))

/* Return 0 if mktime fails to convert a date in the spring-forward gap.
   Based on a problem report from Andreas Jaeger.  */
static int
spring_forward_gap ()
{
  /* glibc (up to about 1998-10-07) failed this test. */
  struct tm tm;

  /* Use the portable POSIX.1 specification "TZ=PST8PDT,M4.1.0,M10.5.0"
     instead of "TZ=America/Vancouver" in order to detect the bug even
     on systems that don't support the Olson extension, or don't have the
     full zoneinfo tables installed.  */
  putenv ("TZ=PST8PDT,M4.1.0,M10.5.0");

  tm.tm_year = 98;
  tm.tm_mon = 3;
  tm.tm_mday = 5;
  tm.tm_hour = 2;
  tm.tm_min = 0;
  tm.tm_sec = 0;
  tm.tm_isdst = -1;
  return mktime (&tm) != (time_t) -1;
}

static int
mktime_test1 (now)
     time_t now;
{
  struct tm *lt;
  return ! (lt = localtime (&now)) || mktime (lt) == now;
}

static int
mktime_test (now)
     time_t now;
{
  return (mktime_test1 (now)
	  && mktime_test1 ((time_t) (time_t_max - now))
	  && mktime_test1 ((time_t) (time_t_min + now)));
}

static int
irix_6_4_bug ()
{
  /* Based on code from Ariel Faigon.  */
  struct tm tm;
  tm.tm_year = 96;
  tm.tm_mon = 3;
  tm.tm_mday = 0;
  tm.tm_hour = 0;
  tm.tm_min = 0;
  tm.tm_sec = 0;
  tm.tm_isdst = -1;
  mktime (&tm);
  return tm.tm_mon == 2 && tm.tm_mday == 31;
}

static int
bigtime_test (j)
     int j;
{
  struct tm tm;
  time_t now;
  tm.tm_year = tm.tm_mon = tm.tm_mday = tm.tm_hour = tm.tm_min = tm.tm_sec = j;
  now = mktime (&tm);
  if (now != (time_t) -1)
    {
      struct tm *lt = localtime (&now);
      if (! (lt
	     && lt->tm_year == tm.tm_year
	     && lt->tm_mon == tm.tm_mon
	     && lt->tm_mday == tm.tm_mday
	     && lt->tm_hour == tm.tm_hour
	     && lt->tm_min == tm.tm_min
	     && lt->tm_sec == tm.tm_sec
	     && lt->tm_yday == tm.tm_yday
	     && lt->tm_wday == tm.tm_wday
	     && ((lt->tm_isdst < 0 ? -1 : 0 < lt->tm_isdst)
		  == (tm.tm_isdst < 0 ? -1 : 0 < tm.tm_isdst))))
	return 0;
    }
  return 1;
}

static int
year_2050_test ()
{
  /* The correct answer for 2050-02-01 00:00:00 in Pacific time,
     ignoring leap seconds.  */
  unsigned long int answer = 2527315200UL;

  struct tm tm;
  time_t t;
  tm.tm_year = 2050 - 1900;
  tm.tm_mon = 2 - 1;
  tm.tm_mday = 1;
  tm.tm_hour = tm.tm_min = tm.tm_sec = 0;
  tm.tm_isdst = -1;

  /* Use the portable POSIX.1 specification "TZ=PST8PDT,M4.1.0,M10.5.0"
     instead of "TZ=America/Vancouver" in order to detect the bug even
     on systems that don't support the Olson extension, or don't have the
     full zoneinfo tables installed.  */
  putenv ("TZ=PST8PDT,M4.1.0,M10.5.0");

  t = mktime (&tm);

  /* Check that the result is either a failure, or close enough
     to the correct answer that we can assume the discrepancy is
     due to leap seconds.  */
  return (t == (time_t) -1
	  || (0 < t && answer - 120 <= t && t <= answer + 120));
}

int
main ()
{
  time_t t, delta;
  int i, j;

  /* This test makes some buggy mktime implementations loop.
     Give up after 60 seconds; a mktime slower than that
     isn't worth using anyway.  */
  alarm (60);

  for (;;)
    {
      t = (time_t_max << 1) + 1;
      if (t <= time_t_max)
	break;
      time_t_max = t;
    }
  time_t_min = - ((time_t) ~ (time_t) 0 == (time_t) -1) - time_t_max;

  delta = time_t_max / 997; /* a suitable prime number */
  for (i = 0; i < N_STRINGS; i++)
    {
      if (tz_strings[i])
	putenv (tz_strings[i]);

      for (t = 0; t <= time_t_max - delta; t += delta)
	if (! mktime_test (t))
	  return 1;
      if (! (mktime_test ((time_t) 1)
	     && mktime_test ((time_t) (60 * 60))
	     && mktime_test ((time_t) (60 * 60 * 24))))
	return 1;

      for (j = 1; ; j <<= 1)
	if (! bigtime_test (j))
	  return 1;
	else if (INT_MAX / 2 < j)
	  break;
      if (! bigtime_test (INT_MAX))
	return 1;
    }
  return ! (irix_6_4_bug () && spring_forward_gap () && year_2050_test ());
}]])],
	       [ac_cv_func_working_mktime=yes],
	       [ac_cv_func_working_mktime=no],
	       [ac_cv_func_working_mktime=no])])
if test $ac_cv_func_working_mktime = no; then
  AC_LIBOBJ([mktime])
fi
])# AC_FUNC_MKTIME

AC_DEFUN([gl_FUNC_MKTIME],
[
  AC_FUNC_MKTIME
  dnl Note: AC_FUNC_MKTIME does AC_LIBOBJ(mktime).
  if test $ac_cv_func_working_mktime = no; then
    AC_DEFINE(mktime, rpl_mktime,
      [Define to rpl_mktime if the replacement function should be used.])
    gl_PREREQ_MKTIME
  fi
])

# Prerequisites of lib/mktime.c.
AC_DEFUN([gl_PREREQ_MKTIME],
[
  AC_REQUIRE([AC_C_INLINE])
])
