/* wc - print the number of lines, words, and bytes in files
   Copyright (C) 85, 91, 1995-2007 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* Written by Paul Rubin, phr@ocf.berkeley.edu
   and David MacKenzie, djm@gnu.ai.mit.edu. */

#include <config.h>

#include <stdio.h>
#include <getopt.h>
#include <sys/types.h>
#include <wchar.h>
#include <wctype.h>

#include "system.h"
#include "error.h"
#include "inttostr.h"
#include "quote.h"
#include "readtokens0.h"
#include "safe-read.h"

#if !defined iswspace && !HAVE_ISWSPACE
# define iswspace(wc) \
    ((wc) == to_uchar (wc) && isspace (to_uchar (wc)))
#endif

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "wc"

#define AUTHORS "Paul Rubin", "David MacKenzie"

/* Size of atomic reads. */
#define BUFFER_SIZE (16 * 1024)

/* The name this program was run with. */
char *program_name;

/* Cumulative number of lines, words, chars and bytes in all files so far.
   max_line_length is the maximum over all files processed so far.  */
static uintmax_t total_lines;
static uintmax_t total_words;
static uintmax_t total_chars;
static uintmax_t total_bytes;
static uintmax_t max_line_length;

/* Which counts to print. */
static bool print_lines, print_words, print_chars, print_bytes;
static bool print_linelength;

/* The print width of each count.  */
static int number_width;

/* True if we have ever read the standard input. */
static bool have_read_stdin;

/* The result of calling fstat or stat on a file descriptor or file.  */
struct fstatus
{
  /* If positive, fstat or stat has not been called yet.  Otherwise,
     this is the value returned from fstat or stat.  */
  int failed;

  /* If FAILED is zero, this is the file's status.  */
  struct stat st;
};

/* For long options that have no equivalent short option, use a
   non-character as a pseudo short option, starting with CHAR_MAX + 1.  */
enum
{
  FILES0_FROM_OPTION = CHAR_MAX + 1
};

static struct option const longopts[] =
{
  {"bytes", no_argument, NULL, 'c'},
  {"chars", no_argument, NULL, 'm'},
  {"lines", no_argument, NULL, 'l'},
  {"words", no_argument, NULL, 'w'},
  {"files0-from", required_argument, NULL, FILES0_FROM_OPTION},
  {"max-line-length", no_argument, NULL, 'L'},
  {GETOPT_HELP_OPTION_DECL},
  {GETOPT_VERSION_OPTION_DECL},
  {NULL, 0, NULL, 0}
};

void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, _("Try `%s --help' for more information.\n"),
	     program_name);
  else
    {
      printf (_("\
Usage: %s [OPTION]... [FILE]...\n\
  or:  %s [OPTION]... --files0-from=F\n\
"),
	      program_name, program_name);
      fputs (_("\
Print newline, word, and byte counts for each FILE, and a total line if\n\
more than one FILE is specified.  With no FILE, or when FILE is -,\n\
read standard input.\n\
  -c, --bytes            print the byte counts\n\
  -m, --chars            print the character counts\n\
  -l, --lines            print the newline counts\n\
"), stdout);
      fputs (_("\
      --files0-from=F    read input from the files specified by\n\
                           NUL-terminated names in file F\n\
  -L, --max-line-length  print the length of the longest line\n\
  -w, --words            print the word counts\n\
"), stdout);
      fputs (HELP_OPTION_DESCRIPTION, stdout);
      fputs (VERSION_OPTION_DESCRIPTION, stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

/* FILE is the name of the file (or NULL for standard input)
   associated with the specified counters.  */
static void
write_counts (uintmax_t lines,
	      uintmax_t words,
	      uintmax_t chars,
	      uintmax_t bytes,
	      uintmax_t linelength,
	      const char *file)
{
  static char const format_sp_int[] = " %*s";
  char const *format_int = format_sp_int + 1;
  char buf[INT_BUFSIZE_BOUND (uintmax_t)];

  if (print_lines)
    {
      printf (format_int, number_width, umaxtostr (lines, buf));
      format_int = format_sp_int;
    }
  if (print_words)
    {
      printf (format_int, number_width, umaxtostr (words, buf));
      format_int = format_sp_int;
    }
  if (print_chars)
    {
      printf (format_int, number_width, umaxtostr (chars, buf));
      format_int = format_sp_int;
    }
  if (print_bytes)
    {
      printf (format_int, number_width, umaxtostr (bytes, buf));
      format_int = format_sp_int;
    }
  if (print_linelength)
    {
      printf (format_int, number_width, umaxtostr (linelength, buf));
    }
  if (file)
    printf (" %s", file);
  putchar ('\n');
}

/* Count words.  FILE_X is the name of the file (or NULL for standard
   input) that is open on descriptor FD.  *FSTATUS is its status.
   Return true if successful.  */
static bool
wc (int fd, char const *file_x, struct fstatus *fstatus)
{
  bool ok = true;
  char buf[BUFFER_SIZE + 1];
  size_t bytes_read;
  uintmax_t lines, words, chars, bytes, linelength;
  bool count_bytes, count_chars, count_complicated;
  char const *file = file_x ? file_x : _("standard input");

  lines = words = chars = bytes = linelength = 0;

  /* If in the current locale, chars are equivalent to bytes, we prefer
     counting bytes, because that's easier.  */
#if HAVE_MBRTOWC && (MB_LEN_MAX > 1)
  if (MB_CUR_MAX > 1)
    {
      count_bytes = print_bytes;
      count_chars = print_chars;
    }
  else
#endif
    {
      count_bytes = print_bytes | print_chars;
      count_chars = false;
    }
  count_complicated = print_words | print_linelength;

  /* When counting only bytes, save some line- and word-counting
     overhead.  If FD is a `regular' Unix file, using lseek is enough
     to get its `size' in bytes.  Otherwise, read blocks of BUFFER_SIZE
     bytes at a time until EOF.  Note that the `size' (number of bytes)
     that wc reports is smaller than stats.st_size when the file is not
     positioned at its beginning.  That's why the lseek calls below are
     necessary.  For example the command
     `(dd ibs=99k skip=1 count=0; ./wc -c) < /etc/group'
     should make wc report `0' bytes.  */

  if (count_bytes & !count_chars & !print_lines & !count_complicated)
    {
      off_t current_pos, end_pos;

      if (0 < fstatus->failed)
	fstatus->failed = fstat (fd, &fstatus->st);

      if (! fstatus->failed && S_ISREG (fstatus->st.st_mode)
	  && (current_pos = lseek (fd, (off_t) 0, SEEK_CUR)) != -1
	  && (end_pos = lseek (fd, (off_t) 0, SEEK_END)) != -1)
	{
	  /* Be careful here.  The current position may actually be
	     beyond the end of the file.  As in the example above.  */
	  bytes = end_pos < current_pos ? 0 : end_pos - current_pos;
	}
      else
	{
	  while ((bytes_read = safe_read (fd, buf, BUFFER_SIZE)) > 0)
	    {
	      if (bytes_read == SAFE_READ_ERROR)
		{
		  error (0, errno, "%s", file);
		  ok = false;
		  break;
		}
	      bytes += bytes_read;
	    }
	}
    }
  else if (!count_chars & !count_complicated)
    {
      /* Use a separate loop when counting only lines or lines and bytes --
	 but not chars or words.  */
      while ((bytes_read = safe_read (fd, buf, BUFFER_SIZE)) > 0)
	{
	  char *p = buf;

	  if (bytes_read == SAFE_READ_ERROR)
	    {
	      error (0, errno, "%s", file);
	      ok = false;
	      break;
	    }

	  while ((p = memchr (p, '\n', (buf + bytes_read) - p)))
	    {
	      ++p;
	      ++lines;
	    }
	  bytes += bytes_read;
	}
    }
#if HAVE_MBRTOWC && (MB_LEN_MAX > 1)
# define SUPPORT_OLD_MBRTOWC 1
  else if (MB_CUR_MAX > 1)
    {
      bool in_word = false;
      uintmax_t linepos = 0;
      mbstate_t state = { 0, };
# if SUPPORT_OLD_MBRTOWC
      /* Back-up the state before each multibyte character conversion and
	 move the last incomplete character of the buffer to the front
	 of the buffer.  This is needed because we don't know whether
	 the `mbrtowc' function updates the state when it returns -2, -
	 this is the ISO C 99 and glibc-2.2 behaviour - or not - amended
	 ANSI C, glibc-2.1 and Solaris 5.7 behaviour.  We don't have an
	 autoconf test for this, yet.  */
      size_t prev = 0; /* number of bytes carried over from previous round */
# else
      const size_t prev = 0;
# endif

      while ((bytes_read = safe_read (fd, buf + prev, BUFFER_SIZE - prev)) > 0)
	{
	  const char *p;
# if SUPPORT_OLD_MBRTOWC
	  mbstate_t backup_state;
# endif
	  if (bytes_read == SAFE_READ_ERROR)
	    {
	      error (0, errno, "%s", file);
	      ok = false;
	      break;
	    }

	  bytes += bytes_read;
	  p = buf;
	  bytes_read += prev;
	  do
	    {
	      wchar_t wide_char;
	      size_t n;

# if SUPPORT_OLD_MBRTOWC
	      backup_state = state;
# endif
	      n = mbrtowc (&wide_char, p, bytes_read, &state);
	      if (n == (size_t) -2)
		{
# if SUPPORT_OLD_MBRTOWC
		  state = backup_state;
# endif
		  break;
		}
	      if (n == (size_t) -1)
		{
		  /* Remember that we read a byte, but don't complain
		     about the error.  Because of the decoding error,
		     this is a considered to be byte but not a
		     character (that is, chars is not incremented).  */
		  p++;
		  bytes_read--;
		}
	      else
		{
		  if (n == 0)
		    {
		      wide_char = 0;
		      n = 1;
		    }
		  p += n;
		  bytes_read -= n;
		  chars++;
		  switch (wide_char)
		    {
		    case '\n':
		      lines++;
		      /* Fall through. */
		    case '\r':
		    case '\f':
		      if (linepos > linelength)
			linelength = linepos;
		      linepos = 0;
		      goto mb_word_separator;
		    case '\t':
		      linepos += 8 - (linepos % 8);
		      goto mb_word_separator;
		    case ' ':
		      linepos++;
		      /* Fall through. */
		    case '\v':
		    mb_word_separator:
		      words += in_word;
		      in_word = false;
		      break;
		    default:
		      if (iswprint (wide_char))
			{
			  int width = wcwidth (wide_char);
			  if (width > 0)
			    linepos += width;
			  if (iswspace (wide_char))
			    goto mb_word_separator;
			  in_word = true;
			}
		      break;
		    }
		}
	    }
	  while (bytes_read > 0);

# if SUPPORT_OLD_MBRTOWC
	  if (bytes_read > 0)
	    {
	      if (bytes_read == BUFFER_SIZE)
		{
		  /* Encountered a very long redundant shift sequence.  */
		  p++;
		  bytes_read--;
		}
	      memmove (buf, p, bytes_read);
	    }
	  prev = bytes_read;
# endif
	}
      if (linepos > linelength)
	linelength = linepos;
      words += in_word;
    }
#endif
  else
    {
      bool in_word = false;
      uintmax_t linepos = 0;

      while ((bytes_read = safe_read (fd, buf, BUFFER_SIZE)) > 0)
	{
	  const char *p = buf;
	  if (bytes_read == SAFE_READ_ERROR)
	    {
	      error (0, errno, "%s", file);
	      ok = false;
	      break;
	    }

	  bytes += bytes_read;
	  do
	    {
	      switch (*p++)
		{
		case '\n':
		  lines++;
		  /* Fall through. */
		case '\r':
		case '\f':
		  if (linepos > linelength)
		    linelength = linepos;
		  linepos = 0;
		  goto word_separator;
		case '\t':
		  linepos += 8 - (linepos % 8);
		  goto word_separator;
		case ' ':
		  linepos++;
		  /* Fall through. */
		case '\v':
		word_separator:
		  words += in_word;
		  in_word = false;
		  break;
		default:
		  if (isprint (to_uchar (p[-1])))
		    {
		      linepos++;
		      if (isspace (to_uchar (p[-1])))
			goto word_separator;
		      in_word = true;
		    }
		  break;
		}
	    }
	  while (--bytes_read);
	}
      if (linepos > linelength)
	linelength = linepos;
      words += in_word;
    }

  if (count_chars < print_chars)
    chars = bytes;

  write_counts (lines, words, chars, bytes, linelength, file_x);
  total_lines += lines;
  total_words += words;
  total_chars += chars;
  total_bytes += bytes;
  if (linelength > max_line_length)
    max_line_length = linelength;

  return ok;
}

static bool
wc_file (char const *file, struct fstatus *fstatus)
{
  if (! file || STREQ (file, "-"))
    {
      have_read_stdin = true;
      if (O_BINARY && ! isatty (STDIN_FILENO))
	freopen (NULL, "rb", stdin);
      return wc (STDIN_FILENO, file, fstatus);
    }
  else
    {
      int fd = open (file, O_RDONLY | O_BINARY);
      if (fd == -1)
	{
	  error (0, errno, "%s", file);
	  return false;
	}
      else
	{
	  bool ok = wc (fd, file, fstatus);
	  if (close (fd) != 0)
	    {
	      error (0, errno, "%s", file);
	      return false;
	    }
	  return ok;
	}
    }
}

/* Return the file status for the NFILES files addressed by FILE.
   Optimize the case where only one number is printed, for just one
   file; in that case we can use a print width of 1, so we don't need
   to stat the file.  */

static struct fstatus *
get_input_fstatus (int nfiles, char * const *file)
{
  struct fstatus *fstatus = xnmalloc (nfiles, sizeof *fstatus);

  if (nfiles == 1
      && ((print_lines + print_words + print_chars
	   + print_bytes + print_linelength)
	  == 1))
    fstatus[0].failed = 1;
  else
    {
      int i;

      for (i = 0; i < nfiles; i++)
	fstatus[i].failed = (! file[i] || STREQ (file[i], "-")
			     ? fstat (STDIN_FILENO, &fstatus[i].st)
			     : stat (file[i], &fstatus[i].st));
    }

  return fstatus;
}

/* Return a print width suitable for the NFILES files whose status is
   recorded in FSTATUS.  Optimize the same special case that
   get_input_fstatus optimizes.  */

static int
compute_number_width (int nfiles, struct fstatus const *fstatus)
{
  int width = 1;

  if (0 < nfiles && fstatus[0].failed <= 0)
    {
      int minimum_width = 1;
      uintmax_t regular_total = 0;
      int i;

      for (i = 0; i < nfiles; i++)
	if (! fstatus[i].failed)
	  {
	    if (S_ISREG (fstatus[i].st.st_mode))
	      regular_total += fstatus[i].st.st_size;
	    else
	      minimum_width = 7;
	  }

      for (; 10 <= regular_total; regular_total /= 10)
	width++;
      if (width < minimum_width)
	width = minimum_width;
    }

  return width;
}


int
main (int argc, char **argv)
{
  int i;
  bool ok;
  int optc;
  int nfiles;
  char **files;
  char *files_from = NULL;
  struct fstatus *fstatus;
  struct Tokens tok;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  print_lines = print_words = print_chars = print_bytes = false;
  print_linelength = false;
  total_lines = total_words = total_chars = total_bytes = max_line_length = 0;

  while ((optc = getopt_long (argc, argv, "clLmw", longopts, NULL)) != -1)
    switch (optc)
      {
      case 'c':
	print_bytes = true;
	break;

      case 'm':
	print_chars = true;
	break;

      case 'l':
	print_lines = true;
	break;

      case 'w':
	print_words = true;
	break;

      case 'L':
	print_linelength = true;
	break;

      case FILES0_FROM_OPTION:
	files_from = optarg;
	break;

      case_GETOPT_HELP_CHAR;

      case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);

      default:
	usage (EXIT_FAILURE);
      }

  if (! (print_lines | print_words | print_chars | print_bytes
	 | print_linelength))
    print_lines = print_words = print_bytes = true;

  if (files_from)
    {
      FILE *stream;

      /* When using --files0-from=F, you may not specify any files
	 on the command-line.  */
      if (optind < argc)
	{
	  error (0, 0, _("extra operand %s"), quote (argv[optind]));
	  fprintf (stderr, "%s\n",
		   _("File operands cannot be combined with --files0-from."));
	  usage (EXIT_FAILURE);
	}

      if (STREQ (files_from, "-"))
	stream = stdin;
      else
	{
	  stream = fopen (files_from, "r");
	  if (stream == NULL)
	    error (EXIT_FAILURE, errno, _("cannot open %s for reading"),
		   quote (files_from));
	}

      readtokens0_init (&tok);

      if (! readtokens0 (stream, &tok) || fclose (stream) != 0)
	error (EXIT_FAILURE, 0, _("cannot read file names from %s"),
	       quote (files_from));

      files = tok.tok;
      nfiles = tok.n_tok;
    }
  else
    {
      static char *stdin_only[2];
      files = (optind < argc ? argv + optind : stdin_only);
      nfiles = (optind < argc ? argc - optind : 1);
      stdin_only[0] = NULL;
    }

  fstatus = get_input_fstatus (nfiles, files);
  number_width = compute_number_width (nfiles, fstatus);

  ok = true;
  for (i = 0; i < nfiles; i++)
    {
      if (files_from && STREQ (files_from, "-") && STREQ (files[i], "-"))
	{
	  ok = false;
	  error (0, 0,
		 _("when reading file names from stdin, "
		   "no file name of %s allowed"),
		 quote ("-"));
	  continue;
	}
      ok &= wc_file (files[i], &fstatus[i]);
    }

  if (1 < nfiles)
    write_counts (total_lines, total_words, total_chars, total_bytes,
		  max_line_length, _("total"));

  free (fstatus);

  if (have_read_stdin && close (STDIN_FILENO) != 0)
    error (EXIT_FAILURE, errno, "-");

  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}
