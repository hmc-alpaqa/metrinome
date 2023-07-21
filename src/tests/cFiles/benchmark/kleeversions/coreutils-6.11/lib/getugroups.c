/* getugroups.c -- return a list of the groups a user is in

   Copyright (C) 1990, 1991, 1998-2000, 2003-2008 Free Software Foundation.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* Written by David MacKenzie. */

#include <config.h>

#include "getugroups.h"

#include <limits.h>
#include <stdio.h> /* grp.h on alpha OSF1 V2.0 uses "FILE *". */
#include <grp.h>

#include <unistd.h>

#include <errno.h>

/* Some old header files might not declare setgrent, getgrent, and endgrent.
   If you don't have them at all, we can't implement this function.
   You lose!  */
struct group *getgrent ();

#include <string.h>

#define STREQ(s1, s2) ((strcmp (s1, s2) == 0))

/* Like `getgroups', but for user USERNAME instead of for the current
   process.  Store at most MAXCOUNT group IDs in the GROUPLIST array.
   If GID is not -1, store it first (if possible).  GID should be the
   group ID (pw_gid) obtained from getpwuid, in case USERNAME is not
   listed in /etc/groups.  Upon failure, set errno and return -1.
   Otherwise, return the number of IDs we've written into GROUPLIST.  */

int
getugroups (int maxcount, GETGROUPS_T *grouplist, char const *username,
	    gid_t gid)
{
  int count = 0;

  if (gid != (gid_t) -1)
    {
      if (maxcount != 0)
	grouplist[count] = gid;
      ++count;
    }

  setgrent ();
  while (1)
    {
      char **cp;
      struct group *grp;

      errno = 0;
      grp = getgrent ();
      if (grp == NULL)
	break;

      for (cp = grp->gr_mem; *cp; ++cp)
	{
	  int n;

	  if ( ! STREQ (username, *cp))
	    continue;

	  /* See if this group number is already on the list.  */
	  for (n = 0; n < count; ++n)
	    if (grouplist && grouplist[n] == grp->gr_gid)
	      break;

	  /* If it's a new group number, then try to add it to the list.  */
	  if (n == count)
	    {
	      if (maxcount != 0)
		{
		  if (count >= maxcount)
		    goto done;
		  grouplist[count] = grp->gr_gid;
		}
	      if (count == INT_MAX)
		{
		  errno = EOVERFLOW;
		  goto done;
		}
	      count++;
	    }
	}
    }

  if (errno != 0)
    count = -1;

 done:
  {
    int saved_errno = errno;
    endgrent ();
    errno = saved_errno;
  }

  return count;
}
