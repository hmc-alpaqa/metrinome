/* Lock a mutex, abandoning after a certain time.
   Copyright (C) 2019-2020 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

#include <config.h>

/* Specification.  */
#include <pthread.h>

#include <errno.h>
#include <limits.h>
#include <sys/time.h>
#include <time.h>

int
pthread_mutex_timedlock (pthread_mutex_t *mutex, const struct timespec *abstime)
{
  /* Poll the mutex's state in regular intervals.  Ugh.  */
  /* POSIX says:
      "Under no circumstance shall the function fail with a timeout if
       the mutex can be locked immediately. The validity of the abstime
       parameter need not be checked if the mutex can be locked
       immediately."
     Therefore start the loop with a pthread_mutex_trylock call.  */
  for (;;)
    {
      int err;
      struct timeval currtime;
      unsigned long remaining;
      struct timespec duration;

      err = pthread_mutex_trylock (mutex);
      if (err != EBUSY)
        return err;

      gettimeofday (&currtime, NULL);

      if (currtime.tv_sec > abstime->tv_sec)
        remaining = 0;
      else
        {
          unsigned long seconds = abstime->tv_sec - currtime.tv_sec;
          remaining = seconds * 1000000000;
          if (remaining / 1000000000 != seconds) /* overflow? */
            remaining = ULONG_MAX;
          else
            {
              long nanoseconds =
                abstime->tv_nsec - currtime.tv_usec * 1000;
              if (nanoseconds >= 0)
                {
                  remaining += nanoseconds;
                  if (remaining < nanoseconds) /* overflow? */
                    remaining = ULONG_MAX;
                }
              else
                {
                  if (remaining >= - nanoseconds)
                    remaining -= (- nanoseconds);
                  else
                    remaining = 0;
                }
            }
        }
      if (remaining == 0)
        return ETIMEDOUT;

      /* Sleep 1 ms.  */
      duration.tv_sec = 0;
      duration.tv_nsec = 1000000;
      if (duration.tv_nsec > remaining)
        duration.tv_nsec = remaining;
      nanosleep (&duration, NULL);
    }
}
