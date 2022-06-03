/* -*- buffer-read-only: t -*- vi: set ro: */
/* DO NOT EDIT! GENERATED AUTOMATICALLY! */
#line 1
/* Test of POSIX compatible fflush() function.
   Copyright (C) 2007 Free Software Foundation, Inc.

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

/* Written by Eric Blake, 2007.  */

#include <config.h>

#include <stdio.h>
#include <unistd.h>

int
main (int argc, char *argv[])
{
  FILE *f;
  char buffer[10];
  int fd;

  /* Create test file.  */
  f = fopen ("test-fflush.txt", "w");
  if (!f || fwrite ("1234567890ABCDEFG", 1, 17, f) != 17 || fclose (f) != 0)
    {
      fputs ("Failed to create sample file.\n", stderr);
      unlink ("test-fflush.txt");
      return 1;
    }

  /* Test fflush.  */
  f = fopen ("test-fflush.txt", "r");
  fd = fileno (f);
  if (!f || 0 > fd || fread (buffer, 1, 5, f) != 5)
    {
      fputs ("Failed initial read of sample file.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* For deterministic results, ensure f read a bigger buffer.
     This is not the case on BeOS, nor on uClibc.  */
#if !(defined __BEOS__ || defined __UCLIBC__)
  if (lseek (fd, 0, SEEK_CUR) == 5)
    {
      fputs ("Sample file was not buffered after fread.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
#endif
  /* POSIX requires fflush-fseek to set file offset of fd.  */
  if (fflush (f) != 0 || fseek (f, 0, SEEK_CUR) != 0)
    {
      fputs ("Failed to flush-fseek sample file.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* Check that offset is correct.  */
  if (lseek (fd, 0, SEEK_CUR) != 5)
    {
      fprintf (stderr, "File offset is wrong after fseek: %ld.\n",
	       (long) lseek (fd, 0, SEEK_CUR));
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  if (ftell (f) != 5)
    {
      fprintf (stderr, "ftell result is wrong after fseek: %ld.\n",
	       (long) ftell (f));
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* Check that file reading resumes at correct location.  */
  if (fgetc (f) != '6')
    {
      fputs ("Failed to read next byte after fseek.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* For deterministic results, ensure f read a bigger buffer.  */
  if (lseek (fd, 0, SEEK_CUR) == 6)
    {
      fputs ("Sample file was not buffered after fgetc.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* POSIX requires fflush-fseeko to set file offset of fd.  */
  if (fflush (f) != 0 || fseeko (f, 0, SEEK_CUR) != 0)
    {
      fputs ("Failed to flush-fseeko sample file.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* Check that offset is correct.  */
  if (lseek (fd, 0, SEEK_CUR) != 6)
    {
      fprintf (stderr, "File offset is wrong after fseeko: %ld.\n",
	       (long) lseek (fd, 0, SEEK_CUR));
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  if (ftell (f) != 6)
    {
      fprintf (stderr, "ftell result is wrong after fseeko: %ld.\n",
	       (long) ftell (f));
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  /* Check that file reading resumes at correct location.  */
  if (fgetc (f) != '7')
    {
      fputs ("Failed to read next byte after fseeko.\n", stderr);
      fclose (f);
      unlink ("test-fflush.txt");
      return 1;
    }
  fclose (f);
  unlink ("test-fflush.txt");
  return 0;
}
