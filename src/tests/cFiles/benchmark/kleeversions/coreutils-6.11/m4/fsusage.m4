#serial 23
# Obtaining file system usage information.

# Copyright (C) 1997, 1998, 2000, 2001, 2003-2007 Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# Written by Jim Meyering.

AC_DEFUN([gl_FSUSAGE],
[
  AC_CHECK_HEADERS_ONCE(sys/param.h)
  AC_CHECK_HEADERS_ONCE(sys/vfs.h sys/fs_types.h)
  AC_CHECK_HEADERS(sys/mount.h, [], [],
    [AC_INCLUDES_DEFAULT
     [#if HAVE_SYS_PARAM_H
       #include <sys/param.h>
      #endif]])
  gl_FILE_SYSTEM_USAGE([gl_cv_fs_space=yes], [gl_cv_fs_space=no])
  if test $gl_cv_fs_space = yes; then
    AC_LIBOBJ(fsusage)
    gl_PREREQ_FSUSAGE_EXTRA
  fi
])

# Try to determine how a program can obtain file system usage information.
# If successful, define the appropriate symbol (see fsusage.c) and
# execute ACTION-IF-FOUND.  Otherwise, execute ACTION-IF-NOT-FOUND.
#
# gl_FILE_SYSTEM_USAGE([ACTION-IF-FOUND[, ACTION-IF-NOT-FOUND]])

AC_DEFUN([gl_FILE_SYSTEM_USAGE],
[

AC_MSG_NOTICE([checking how to get file system space usage])
ac_fsusage_space=no

# Perform only the link test since it seems there are no variants of the
# statvfs function.  This check is more than just AC_CHECK_FUNCS(statvfs)
# because that got a false positive on SCO OSR5.  Adding the declaration
# of a `struct statvfs' causes this test to fail (as it should) on such
# systems.  That system is reported to work fine with STAT_STATFS4 which
# is what it gets when this test fails.
if test $ac_fsusage_space = no; then
  # SVR4
  AC_CACHE_CHECK([for statvfs function (SVR4)], fu_cv_sys_stat_statvfs,
		 [AC_TRY_LINK([#include <sys/types.h>
#if defined __GLIBC__ && !defined __BEOS__
Do not use statvfs on systems with GNU libc, because that function stats
all preceding entries in /proc/mounts, and that makes df hang if even
one of the corresponding file systems is hard-mounted, but not available.
statvfs in GNU libc on BeOS operates differently: it only makes a system
call.
#endif

#ifdef __osf__
"Do not use Tru64's statvfs implementation"
#endif

#include <sys/statvfs.h>],
			      [struct statvfs fsd; statvfs (0, &fsd);],
			      fu_cv_sys_stat_statvfs=yes,
			      fu_cv_sys_stat_statvfs=no)])
  if test $fu_cv_sys_stat_statvfs = yes; then
    ac_fsusage_space=yes
    AC_DEFINE(STAT_STATVFS, 1,
	      [  Define if there is a function named statvfs.  (SVR4)])
  fi
fi

if test $ac_fsusage_space = no; then
  # DEC Alpha running OSF/1
  AC_MSG_CHECKING([for 3-argument statfs function (DEC OSF/1)])
  AC_CACHE_VAL(fu_cv_sys_stat_statfs3_osf1,
  [AC_TRY_RUN([
#include <sys/param.h>
#include <sys/types.h>
#include <sys/mount.h>
  int
  main ()
  {
    struct statfs fsd;
    fsd.f_fsize = 0;
    return statfs (".", &fsd, sizeof (struct statfs)) != 0;
  }],
  fu_cv_sys_stat_statfs3_osf1=yes,
  fu_cv_sys_stat_statfs3_osf1=no,
  fu_cv_sys_stat_statfs3_osf1=no)])
  AC_MSG_RESULT($fu_cv_sys_stat_statfs3_osf1)
  if test $fu_cv_sys_stat_statfs3_osf1 = yes; then
    ac_fsusage_space=yes
    AC_DEFINE(STAT_STATFS3_OSF1, 1,
	      [   Define if  statfs takes 3 args.  (DEC Alpha running OSF/1)])
  fi
fi

if test $ac_fsusage_space = no; then
# AIX
  AC_MSG_CHECKING([for two-argument statfs with statfs.bsize dnl
member (AIX, 4.3BSD)])
  AC_CACHE_VAL(fu_cv_sys_stat_statfs2_bsize,
  [AC_TRY_RUN([
#ifdef HAVE_SYS_PARAM_H
#include <sys/param.h>
#endif
#ifdef HAVE_SYS_MOUNT_H
#include <sys/mount.h>
#endif
#ifdef HAVE_SYS_VFS_H
#include <sys/vfs.h>
#endif
  int
  main ()
  {
  struct statfs fsd;
  fsd.f_bsize = 0;
  return statfs (".", &fsd) != 0;
  }],
  fu_cv_sys_stat_statfs2_bsize=yes,
  fu_cv_sys_stat_statfs2_bsize=no,
  fu_cv_sys_stat_statfs2_bsize=no)])
  AC_MSG_RESULT($fu_cv_sys_stat_statfs2_bsize)
  if test $fu_cv_sys_stat_statfs2_bsize = yes; then
    ac_fsusage_space=yes
    AC_DEFINE(STAT_STATFS2_BSIZE, 1,
[  Define if statfs takes 2 args and struct statfs has a field named f_bsize.
   (4.3BSD, SunOS 4, HP-UX, AIX PS/2)])
  fi
fi

if test $ac_fsusage_space = no; then
# SVR3
  AC_MSG_CHECKING([for four-argument statfs (AIX-3.2.5, SVR3)])
  AC_CACHE_VAL(fu_cv_sys_stat_statfs4,
  [AC_TRY_RUN([#include <sys/types.h>
#include <sys/statfs.h>
  int
  main ()
  {
  struct statfs fsd;
  return statfs (".", &fsd, sizeof fsd, 0) != 0;
  }],
    fu_cv_sys_stat_statfs4=yes,
    fu_cv_sys_stat_statfs4=no,
    fu_cv_sys_stat_statfs4=no)])
  AC_MSG_RESULT($fu_cv_sys_stat_statfs4)
  if test $fu_cv_sys_stat_statfs4 = yes; then
    ac_fsusage_space=yes
    AC_DEFINE(STAT_STATFS4, 1,
	      [  Define if statfs takes 4 args.  (SVR3, Dynix, Irix, Dolphin)])
  fi
fi

if test $ac_fsusage_space = no; then
# 4.4BSD and NetBSD
  AC_MSG_CHECKING([for two-argument statfs with statfs.fsize dnl
member (4.4BSD and NetBSD)])
  AC_CACHE_VAL(fu_cv_sys_stat_statfs2_fsize,
  [AC_TRY_RUN([#include <sys/types.h>
#ifdef HAVE_SYS_PARAM_H
#include <sys/param.h>
#endif
#ifdef HAVE_SYS_MOUNT_H
#include <sys/mount.h>
#endif
  int
  main ()
  {
  struct statfs fsd;
  fsd.f_fsize = 0;
  return statfs (".", &fsd) != 0;
  }],
  fu_cv_sys_stat_statfs2_fsize=yes,
  fu_cv_sys_stat_statfs2_fsize=no,
  fu_cv_sys_stat_statfs2_fsize=no)])
  AC_MSG_RESULT($fu_cv_sys_stat_statfs2_fsize)
  if test $fu_cv_sys_stat_statfs2_fsize = yes; then
    ac_fsusage_space=yes
    AC_DEFINE(STAT_STATFS2_FSIZE, 1,
[  Define if statfs takes 2 args and struct statfs has a field named f_fsize.
   (4.4BSD, NetBSD)])
  fi
fi

if test $ac_fsusage_space = no; then
  # Ultrix
  AC_MSG_CHECKING([for two-argument statfs with struct fs_data (Ultrix)])
  AC_CACHE_VAL(fu_cv_sys_stat_fs_data,
  [AC_TRY_RUN([#include <sys/types.h>
#ifdef HAVE_SYS_PARAM_H
#include <sys/param.h>
#endif
#ifdef HAVE_SYS_MOUNT_H
#include <sys/mount.h>
#endif
#ifdef HAVE_SYS_FS_TYPES_H
#include <sys/fs_types.h>
#endif
  int
  main ()
  {
  struct fs_data fsd;
  /* Ultrix's statfs returns 1 for success,
     0 for not mounted, -1 for failure.  */
  return statfs (".", &fsd) != 1;
  }],
  fu_cv_sys_stat_fs_data=yes,
  fu_cv_sys_stat_fs_data=no,
  fu_cv_sys_stat_fs_data=no)])
  AC_MSG_RESULT($fu_cv_sys_stat_fs_data)
  if test $fu_cv_sys_stat_fs_data = yes; then
    ac_fsusage_space=yes
    AC_DEFINE(STAT_STATFS2_FS_DATA, 1,
[  Define if statfs takes 2 args and the second argument has
   type struct fs_data.  (Ultrix)])
  fi
fi

if test $ac_fsusage_space = no; then
  # SVR2
  AC_TRY_CPP([#include <sys/filsys.h>
    ],
    AC_DEFINE(STAT_READ_FILSYS, 1,
      [Define if there is no specific function for reading file systems usage
       information and you have the <sys/filsys.h> header file.  (SVR2)])
    ac_fsusage_space=yes)
fi

AS_IF([test $ac_fsusage_space = yes], [$1], [$2])

])


# Check for SunOS statfs brokenness wrt partitions 2GB and larger.
# If <sys/vfs.h> exists and struct statfs has a member named f_spare,
# enable the work-around code in fsusage.c.
AC_DEFUN([gl_STATFS_TRUNCATES],
[
  AC_MSG_CHECKING([for statfs that truncates block counts])
  AC_CACHE_VAL(fu_cv_sys_truncating_statfs,
  [AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[
#if !defined(sun) && !defined(__sun)
choke -- this is a workaround for a Sun-specific problem
#endif
#include <sys/types.h>
#include <sys/vfs.h>]],
    [[struct statfs t; long c = *(t.f_spare);
      if (c) return 0;]])],
    [fu_cv_sys_truncating_statfs=yes],
    [fu_cv_sys_truncating_statfs=no])])
  if test $fu_cv_sys_truncating_statfs = yes; then
    AC_DEFINE(STATFS_TRUNCATES_BLOCK_COUNTS, 1,
      [Define if the block counts reported by statfs may be truncated to 2GB
       and the correct values may be stored in the f_spare array.
       (SunOS 4.1.2, 4.1.3, and 4.1.3_U1 are reported to have this problem.
       SunOS 4.1.1 seems not to be affected.)])
  fi
  AC_MSG_RESULT($fu_cv_sys_truncating_statfs)
])


# Prerequisites of lib/fsusage.c not done by gl_FILE_SYSTEM_USAGE.
AC_DEFUN([gl_PREREQ_FSUSAGE_EXTRA],
[
  AC_CHECK_HEADERS(dustat.h sys/fs/s5param.h sys/filsys.h sys/statfs.h)
  gl_STATFS_TRUNCATES
])
