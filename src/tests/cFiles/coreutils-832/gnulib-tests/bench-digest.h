/*
 * Copyright (C) 2018-2020 Free Software Foundation, Inc.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/time.h>

struct timings_state
{
  /* Filled when the timings start.  */
  struct timeval real_start;
  struct timeval user_start;
  struct timeval sys_start;
  /* Filled when the timings end.  */
  long real_usec;
  long user_usec;
  long sys_usec;
};

static void
timing_start (struct timings_state *ts)
{
  struct rusage usage;

  getrusage (RUSAGE_SELF, &usage);
  ts->user_start = usage.ru_utime;
  ts->sys_start = usage.ru_stime;

  gettimeofday (&ts->real_start, NULL);
}

static void
timing_end (struct timings_state *ts)
{
  struct timeval real_end;
  struct rusage usage;

  gettimeofday (&real_end, NULL);

  getrusage (RUSAGE_SELF, &usage);

  ts->real_usec = (real_end.tv_sec - ts->real_start.tv_sec) * 1000000
                  + real_end.tv_usec - ts->real_start.tv_usec;
  ts->user_usec = (usage.ru_utime.tv_sec - ts->user_start.tv_sec) * 1000000
                  + usage.ru_utime.tv_usec - ts->user_start.tv_usec;
  ts->sys_usec = (usage.ru_stime.tv_sec - ts->sys_start.tv_sec) * 1000000
                 + usage.ru_stime.tv_usec - ts->sys_start.tv_usec;
}

static void
timing_output (const struct timings_state *ts)
{
  printf ("real %10.6f\n", (double)ts->real_usec / 1000000.0);
  printf ("user %7.3f\n", (double)ts->user_usec / 1000000.0);
  printf ("sys  %7.3f\n", (double)ts->sys_usec / 1000000.0);
}

int
main (int argc, char *argv[])
{
  if (argc != 3)
    {
      fprintf (stderr, "Usage: %s SIZE REPETITIONS\n", argv[0]);
      exit (1);
    }

  size_t size = atol (argv[1]);
  int repeat = atoi (argv[2]);

  char *memblock = (char *) malloc (size);

  /* Fill the memory block.  */
  {
    size_t i;
    for (i = 0; i < size; i++)
      memblock[i] =
        (unsigned char) (((i * (i-1) * (i-5)) >> 6) + (i % 499) + (i % 101));
  }

  struct timings_state ts;
  timing_start (&ts);

  int count;
  for (count = 0; count < repeat; count++)
    {
      char digest[64];
      FUNC (memblock, size, digest);
    }

  timing_end (&ts);
  timing_output (&ts);

  return 0;
}
