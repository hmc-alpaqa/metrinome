#serial 23

dnl From Jim Meyering.
dnl Check for the nanosleep function.
dnl If not found, use the supplied replacement.
dnl

# Copyright (C) 1999, 2000, 2001, 2003, 2004, 2005, 2006, 2007 Free
# Software Foundation, Inc.

# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_FUNC_NANOSLEEP],
[
 dnl Persuade glibc and Solaris <time.h> to declare nanosleep.
 AC_REQUIRE([gl_USE_SYSTEM_EXTENSIONS])

 AC_REQUIRE([gl_HEADER_TIME_H_DEFAULTS])
 AC_REQUIRE([gl_CLOCK_TIME])
 AC_CHECK_HEADERS_ONCE(sys/time.h)

 nanosleep_save_libs=$LIBS

 # Solaris 2.5.1 needs -lposix4 to get the nanosleep function.
 # Solaris 7 prefers the library name -lrt to the obsolescent name -lposix4.
 AC_SEARCH_LIBS([nanosleep], [rt posix4],
                [test "$ac_cv_search_nanosleep" = "none required" ||
	         LIB_NANOSLEEP=$ac_cv_search_nanosleep])

 AC_CACHE_CHECK([for working nanosleep],
  [gl_cv_func_nanosleep],
  [
   AC_RUN_IFELSE(
     [AC_LANG_SOURCE([[
	#include <errno.h>
	#include <limits.h>
	#include <signal.h>
	#if HAVE_SYS_TIME_H
	 #include <sys/time.h>
	#endif
	#include <time.h>
	#include <unistd.h>
	#define TYPE_SIGNED(t) (! ((t) 0 < (t) -1))
	#define TYPE_MAXIMUM(t) \
	  ((t) (! TYPE_SIGNED (t) \
		? (t) -1 \
		: ~ (~ (t) 0 << (sizeof (t) * CHAR_BIT - 1))))

	static void
	check_for_SIGALRM (int sig)
	{
	  if (sig != SIGALRM)
	    _exit (1);
	}

	int
	main ()
	{
	  static struct timespec ts_sleep;
	  static struct timespec ts_remaining;
	  static struct sigaction act;
	  if (! nanosleep)
	    return 1;
	  act.sa_handler = check_for_SIGALRM;
	  sigemptyset (&act.sa_mask);
	  sigaction (SIGALRM, &act, NULL);
	  ts_sleep.tv_sec = 0;
	  ts_sleep.tv_nsec = 1;
	  alarm (1);
	  if (nanosleep (&ts_sleep, NULL) != 0)
	    return 1;
	  ts_sleep.tv_sec = TYPE_MAXIMUM (time_t);
	  ts_sleep.tv_nsec = 999999999;
	  alarm (1);
	  if (nanosleep (&ts_sleep, &ts_remaining) == -1 && errno == EINTR
	      && TYPE_MAXIMUM (time_t) - 10 < ts_remaining.tv_sec)
	    return 0;
	  return 119;
	}]])],
     [gl_cv_func_nanosleep=yes],
     [case $? in dnl (
      119) gl_cv_func_nanosleep='no (mishandles large arguments)';; dnl (
      *)   gl_cv_func_nanosleep=no;;
      esac],
     [gl_cv_func_nanosleep=cross-compiling])
  ])
  if test "$gl_cv_func_nanosleep" = yes; then
    REPLACE_NANOSLEEP=0
  else
    REPLACE_NANOSLEEP=1
    if test "$gl_cv_func_nanosleep" = 'no (mishandles large arguments)'; then
      AC_DEFINE([HAVE_BUG_BIG_NANOSLEEP], 1,
	[Define to 1 if nanosleep mishandles large arguments.])
      for ac_lib in $LIB_CLOCK_GETTIME; do
	case " $LIB_NANOSLEEP " in
	*" $ac_lib "*) ;;
	*) LIB_NANOSLEEP="$LIB_NANOSLEEP $ac_lib";;
	esac
      done
    fi
    AC_LIBOBJ(nanosleep)
    gl_PREREQ_NANOSLEEP
  fi

 AC_SUBST([LIB_NANOSLEEP])
 LIBS=$nanosleep_save_libs
])

# Prerequisites of lib/nanosleep.c.
AC_DEFUN([gl_PREREQ_NANOSLEEP],
[
  AC_CHECK_FUNCS_ONCE(siginterrupt)
  AC_CHECK_HEADERS_ONCE(sys/select.h)
])
