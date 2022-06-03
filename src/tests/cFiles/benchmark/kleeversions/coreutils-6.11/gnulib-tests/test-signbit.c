/* -*- buffer-read-only: t -*- vi: set ro: */
/* DO NOT EDIT! GENERATED AUTOMATICALLY! */
#line 1
/* Test of signbit() substitute.
   Copyright (C) 2007, 2008 Free Software Foundation, Inc.

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

/* Written by Bruno Haible <bruno@clisp.org>, 2007.  */

#include <config.h>

#include <math.h>

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

#define ASSERT(expr) \
  do									     \
    {									     \
      if (!(expr))							     \
        {								     \
          fprintf (stderr, "%s:%d: assertion failed\n", __FILE__, __LINE__); \
          fflush (stderr);						     \
          abort ();							     \
        }								     \
    }									     \
  while (0)

float zerof = 0.0f;
double zerod = 0.0;
long double zerol = 0.0L;
/* We cannot use the expression '-zerol' here, because on HP-UX/hppa it
   evaluates to 0.0L, not -0.0L.  */
long double minus_zerol = -0.0L;

static void
test_signbitf ()
{
  /* Finite values.  */
  ASSERT (!signbit (3.141f));
  ASSERT (!signbit (3.141e30f));
  ASSERT (!signbit (3.141e-30f));
  ASSERT (signbit (-2.718f));
  ASSERT (signbit (-2.718e30f));
  ASSERT (signbit (-2.718e-30f));
  /* Zeros.  */
  ASSERT (!signbit (0.0f));
  if (1.0f / -zerof < 0)
    ASSERT (signbit (-0.0f));
  else
    ASSERT (!signbit (-0.0f));
  /* Infinite values.  */
  ASSERT (!signbit (1.0f / 0.0f));
  ASSERT (signbit (-1.0f / 0.0f));
  /* Quiet NaN.  */
  (void) signbit (zerof / zerof);
#if defined FLT_EXPBIT0_WORD && defined FLT_EXPBIT0_BIT
  /* Signalling NaN.  */
  {
    #define NWORDS \
      ((sizeof (float) + sizeof (unsigned int) - 1) / sizeof (unsigned int))
    typedef union { float value; unsigned int word[NWORDS]; } memory_float;
    memory_float m;
    m.value = zerof / zerof;
# if FLT_EXPBIT0_BIT > 0
    m.word[FLT_EXPBIT0_WORD] ^= (unsigned int) 1 << (FLT_EXPBIT0_BIT - 1);
# else
    m.word[FLT_EXPBIT0_WORD + (FLT_EXPBIT0_WORD < NWORDS / 2 ? 1 : - 1)]
      ^= (unsigned int) 1 << (sizeof (unsigned int) * CHAR_BIT - 1);
# endif
    if (FLT_EXPBIT0_WORD < NWORDS / 2)
      m.word[FLT_EXPBIT0_WORD + 1] |= (unsigned int) 1 << FLT_EXPBIT0_BIT;
    else
      m.word[0] |= (unsigned int) 1;
    (void) signbit (m.value);
    #undef NWORDS
  }
#endif
}

static void
test_signbitd ()
{
  /* Finite values.  */
  ASSERT (!signbit (3.141));
  ASSERT (!signbit (3.141e30));
  ASSERT (!signbit (3.141e-30));
  ASSERT (signbit (-2.718));
  ASSERT (signbit (-2.718e30));
  ASSERT (signbit (-2.718e-30));
  /* Zeros.  */
  ASSERT (!signbit (0.0));
  if (1.0 / -zerod < 0)
    ASSERT (signbit (-0.0));
  else
    ASSERT (!signbit (-0.0));
  /* Infinite values.  */
  ASSERT (!signbit (1.0 / 0.0));
  ASSERT (signbit (-1.0 / 0.0));
  /* Quiet NaN.  */
  (void) signbit (zerod / zerod);
#if defined DBL_EXPBIT0_WORD && defined DBL_EXPBIT0_BIT
  /* Signalling NaN.  */
  {
    #define NWORDS \
      ((sizeof (double) + sizeof (unsigned int) - 1) / sizeof (unsigned int))
    typedef union { double value; unsigned int word[NWORDS]; } memory_double;
    memory_double m;
    m.value = zerod / zerod;
# if DBL_EXPBIT0_BIT > 0
    m.word[DBL_EXPBIT0_WORD] ^= (unsigned int) 1 << (DBL_EXPBIT0_BIT - 1);
# else
    m.word[DBL_EXPBIT0_WORD + (DBL_EXPBIT0_WORD < NWORDS / 2 ? 1 : - 1)]
      ^= (unsigned int) 1 << (sizeof (unsigned int) * CHAR_BIT - 1);
# endif
    m.word[DBL_EXPBIT0_WORD + (DBL_EXPBIT0_WORD < NWORDS / 2 ? 1 : - 1)]
      |= (unsigned int) 1 << DBL_EXPBIT0_BIT;
    (void) signbit (m.value);
    #undef NWORDS
  }
#endif
}

static void
test_signbitl ()
{
  /* Finite values.  */
  ASSERT (!signbit (3.141L));
  ASSERT (!signbit (3.141e30L));
  ASSERT (!signbit (3.141e-30L));
  ASSERT (signbit (-2.718L));
  ASSERT (signbit (-2.718e30L));
  ASSERT (signbit (-2.718e-30L));
  /* Zeros.  */
  ASSERT (!signbit (0.0L));
  if (1.0L / minus_zerol < 0)
    ASSERT (signbit (-0.0L));
  else
    ASSERT (!signbit (-0.0L));
  /* Infinite values.  */
  ASSERT (!signbit (1.0L / 0.0L));
  ASSERT (signbit (-1.0L / 0.0L));
  /* Quiet NaN.  */
  (void) signbit (zerol / zerol);
#if defined LDBL_EXPBIT0_WORD && defined LDBL_EXPBIT0_BIT
  /* Signalling NaN.  */
  {
    #define NWORDS \
      ((sizeof (long double) + sizeof (unsigned int) - 1) / sizeof (unsigned int))
    typedef union { long double value; unsigned int word[NWORDS]; } memory_long_double;
    memory_long_double m;
    m.value = zerol / zerol;
# if LDBL_EXPBIT0_BIT > 0
    m.word[LDBL_EXPBIT0_WORD] ^= (unsigned int) 1 << (LDBL_EXPBIT0_BIT - 1);
# else
    m.word[LDBL_EXPBIT0_WORD + (LDBL_EXPBIT0_WORD < NWORDS / 2 ? 1 : - 1)]
      ^= (unsigned int) 1 << (sizeof (unsigned int) * CHAR_BIT - 1);
# endif
    m.word[LDBL_EXPBIT0_WORD + (LDBL_EXPBIT0_WORD < NWORDS / 2 ? 1 : - 1)]
      |= (unsigned int) 1 << LDBL_EXPBIT0_BIT;
    (void) signbit (m.value);
    #undef NWORDS
  }
#endif
}

int
main ()
{
  test_signbitf ();
  test_signbitd ();
  test_signbitl ();
  return 0;
}
