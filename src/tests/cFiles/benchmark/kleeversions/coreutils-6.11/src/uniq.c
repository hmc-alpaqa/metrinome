/* uniq -- remove duplicate lines from a sorted file
   Copyright (C) 86, 91, 1995-2007 Free Software Foundation, Inc.

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

/* Written by Richard Stallman and David MacKenzie. */

#include <config.h>

#include <stdio.h>
#include <getopt.h>
#include <sys/types.h>

#include "system.h"
#include "argmatch.h"
#include "linebuffer.h"
#include "error.h"
#include "hard-locale.h"
#include "posixver.h"
#include "quote.h"
#include "xmemcoll.h"
#include "xstrtol.h"
#include "memcasecmp.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "uniq"

#define AUTHORS "Richard Stallman", "David MacKenzie"

#define SWAP_LINES(A, B)			\
  do						\
    {						\
      struct linebuffer *_tmp;			\
      _tmp = (A);				\
      (A) = (B);				\
      (B) = _tmp;				\
    }						\
  while (0)

/* The name this program was run with. */
char *program_name;

/* True if the LC_COLLATE locale is hard.  */
static bool hard_LC_COLLATE;

/* Number of fields to skip on each line when doing comparisons. */
static size_t skip_fields;

/* Number of chars to skip after skipping any fields. */
static size_t skip_chars;

/* Number of chars to compare. */
static size_t check_chars;

enum countmode
{
  count_occurrences,		/* -c Print count before output lines. */
  count_none			/* Default.  Do not print counts. */
};

/* Whether and how to precede the output lines with a count of the number of
   times they occurred in the input. */
static enum countmode countmode;

/* Which lines to output: unique lines, the first of a group of
   repeated lines, and the second and subsequented of a group of
   repeated lines.  */
static bool output_unique;
static bool output_first_repeated;
static bool output_later_repeated;

/* If true, ignore case when comparing.  */
static bool ignore_case;

enum delimit_method
{
  /* No delimiters output.  --all-repeated[=none] */
  DM_NONE,

  /* Delimiter precedes all groups.  --all-repeated=prepend */
  DM_PREPEND,

  /* Delimit all groups.  --all-repeated=separate */
  DM_SEPARATE
};

static char const *const delimit_method_string[] =
{
  "none", "prepend", "separate", NULL
};

static enum delimit_method const delimit_method_map[] =
{
  DM_NONE, DM_PREPEND, DM_SEPARATE
};

/* Select whether/how to delimit groups of duplicate lines.  */
static enum delimit_method delimit_groups;

static struct option const longopts[] =
{
  {"count", no_argument, NULL, 'c'},
  {"repeated", no_argument, NULL, 'd'},
  {"all-repeated", optional_argument, NULL, 'D'},
  {"ignore-case", no_argument, NULL, 'i'},
  {"unique", no_argument, NULL, 'u'},
  {"skip-fields", required_argument, NULL, 'f'},
  {"skip-chars", required_argument, NULL, 's'},
  {"check-chars", required_argument, NULL, 'w'},
  {"zero-terminated", no_argument, NULL, 'z'},
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
Usage: %s [OPTION]... [INPUT [OUTPUT]]\n\
"),
	      program_name);
      fputs (_("\
Discard all but one of successive identical lines from INPUT (or\n\
standard input), writing to OUTPUT (or standard output).\n\
\n\
"), stdout);
     fputs (_("\
Mandatory arguments to long options are mandatory for short options too.\n\
"), stdout);
     fputs (_("\
  -c, --count           prefix lines by the number of occurrences\n\
  -d, --repeated        only print duplicate lines\n\
"), stdout);
     fputs (_("\
  -D, --all-repeated[=delimit-method]  print all duplicate lines\n\
                        delimit-method={none(default),prepend,separate}\n\
                        Delimiting is done with blank lines.\n\
  -f, --skip-fields=N   avoid comparing the first N fields\n\
  -i, --ignore-case     ignore differences in case when comparing\n\
  -s, --skip-chars=N    avoid comparing the first N characters\n\
  -u, --unique          only print unique lines\n\
  -z, --zero-terminated  end lines with 0 byte, not newline\n\
"), stdout);
     fputs (_("\
  -w, --check-chars=N   compare no more than N characters in lines\n\
"), stdout);
     fputs (HELP_OPTION_DESCRIPTION, stdout);
     fputs (VERSION_OPTION_DESCRIPTION, stdout);
     fputs (_("\
\n\
A field is a run of whitespace, then non-whitespace characters.\n\
Fields are skipped before chars.\n\
"), stdout);
     fputs (_("\
\n\
Note: 'uniq' does not detect repeated lines unless they are adjacent.\n\
You may want to sort the input first, or use `sort -u' without `uniq'.\n\
"), stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

/* Convert OPT to size_t, reporting an error using MSGID if OPT is
   invalid.  Silently convert too-large values to SIZE_MAX.  */

static size_t
size_opt (char const *opt, char const *msgid)
{
  unsigned long int size;
  verify (SIZE_MAX <= ULONG_MAX);

  switch (xstrtoul (opt, NULL, 10, &size, ""))
    {
    case LONGINT_OK:
    case LONGINT_OVERFLOW:
      break;

    default:
      error (EXIT_FAILURE, 0, "%s: %s", opt, _(msgid));
    }

  return MIN (size, SIZE_MAX);
}

/* Given a linebuffer LINE,
   return a pointer to the beginning of the line's field to be compared. */

static char *
find_field (const struct linebuffer *line)
{
  size_t count;
  char *lp = line->buffer;
  size_t size = line->length - 1;
  size_t i = 0;

  for (count = 0; count < skip_fields && i < size; count++)
    {
      while (i < size && isblank (lp[i]))
	i++;
      while (i < size && !isblank (lp[i]))
	i++;
    }

  for (count = 0; count < skip_chars && i < size; count++)
    i++;

  return lp + i;
}

/* Return false if two strings OLD and NEW match, true if not.
   OLD and NEW point not to the beginnings of the lines
   but rather to the beginnings of the fields to compare.
   OLDLEN and NEWLEN are their lengths. */

static bool
different (char *old, char *new, size_t oldlen, size_t newlen)
{
  if (check_chars < oldlen)
    oldlen = check_chars;
  if (check_chars < newlen)
    newlen = check_chars;

  if (ignore_case)
    {
      /* FIXME: This should invoke strcoll somehow.  */
      return oldlen != newlen || memcasecmp (old, new, oldlen);
    }
  else if (hard_LC_COLLATE)
    return xmemcoll (old, oldlen, new, newlen) != 0;
  else
    return oldlen != newlen || memcmp (old, new, oldlen);
}

/* Output the line in linebuffer LINE to standard output
   provided that the switches say it should be output.
   MATCH is true if the line matches the previous line.
   If requested, print the number of times it occurred, as well;
   LINECOUNT + 1 is the number of times that the line occurred. */

static void
writeline (struct linebuffer const *line,
	   bool match, uintmax_t linecount)
{
  if (! (linecount == 0 ? output_unique
	 : !match ? output_first_repeated
	 : output_later_repeated))
    return;

  if (countmode == count_occurrences)
    printf ("%7" PRIuMAX " ", linecount + 1);

  fwrite (line->buffer, sizeof (char), line->length, stdout);
}

/* Process input file INFILE with output to OUTFILE.
   If either is "-", use the standard I/O stream for it instead. */

static void
check_file (const char *infile, const char *outfile, char delimiter)
{
  struct linebuffer lb1, lb2;
  struct linebuffer *thisline, *prevline;

  if (! (STREQ (infile, "-") || freopen (infile, "r", stdin)))
    error (EXIT_FAILURE, errno, "%s", infile);
  if (! (STREQ (outfile, "-") || freopen (outfile, "w", stdout)))
    error (EXIT_FAILURE, errno, "%s", outfile);

  thisline = &lb1;
  prevline = &lb2;

  initbuffer (thisline);
  initbuffer (prevline);

  /* The duplication in the following `if' and `else' blocks is an
     optimization to distinguish the common case (in which none of
     the following options has been specified: --count, -repeated,
     --all-repeated, --unique) from the others.  In the common case,
     this optimization lets uniq output each different line right away,
     without waiting to see if the next one is different.  */

  if (output_unique && output_first_repeated && countmode == count_none)
    {
      char *prevfield IF_LINT (= NULL);
      size_t prevlen IF_LINT (= 0);

      while (!feof (stdin))
	{
	  char *thisfield;
	  size_t thislen;
	  if (readlinebuffer_delim (thisline, stdin, delimiter) == 0)
	    break;
	  thisfield = find_field (thisline);
	  thislen = thisline->length - 1 - (thisfield - thisline->buffer);
	  if (prevline->length == 0
	      || different (thisfield, prevfield, thislen, prevlen))
	    {
	      fwrite (thisline->buffer, sizeof (char),
		      thisline->length, stdout);

	      SWAP_LINES (prevline, thisline);
	      prevfield = thisfield;
	      prevlen = thislen;
	    }
	}
    }
  else
    {
      char *prevfield;
      size_t prevlen;
      uintmax_t match_count = 0;
      bool first_delimiter = true;

      if (readlinebuffer_delim (prevline, stdin, delimiter) == 0)
	goto closefiles;
      prevfield = find_field (prevline);
      prevlen = prevline->length - 1 - (prevfield - prevline->buffer);

      while (!feof (stdin))
	{
	  bool match;
	  char *thisfield;
	  size_t thislen;
	  if (readlinebuffer_delim (thisline, stdin, delimiter) == 0)
	    {
	      if (ferror (stdin))
		goto closefiles;
	      break;
	    }
	  thisfield = find_field (thisline);
	  thislen = thisline->length - 1 - (thisfield - thisline->buffer);
	  match = !different (thisfield, prevfield, thislen, prevlen);
	  match_count += match;

	  if (match_count == UINTMAX_MAX)
	    {
	      if (count_occurrences)
		error (EXIT_FAILURE, 0, _("too many repeated lines"));
	      match_count--;
	    }

          if (delimit_groups != DM_NONE)
	    {
	      if (!match)
		{
		  if (match_count) /* a previous match */
		    first_delimiter = false; /* Only used when DM_SEPARATE */
		}
	      else if (match_count == 1)
		{
		  if ((delimit_groups == DM_PREPEND)
		      || (delimit_groups == DM_SEPARATE
			  && !first_delimiter))
		    putchar (delimiter);
		}
	    }

	  if (!match || output_later_repeated)
	    {
	      writeline (prevline, match, match_count);
	      SWAP_LINES (prevline, thisline);
	      prevfield = thisfield;
	      prevlen = thislen;
	      if (!match)
		match_count = 0;
	    }
	}

      writeline (prevline, false, match_count);
    }

 closefiles:
  if (ferror (stdin) || fclose (stdin) != 0)
    error (EXIT_FAILURE, 0, _("error reading %s"), infile);

  /* stdout is handled via the atexit-invoked close_stdout function.  */

  free (lb1.buffer);
  free (lb2.buffer);
}

enum Skip_field_option_type
  {
    SFO_NONE,
    SFO_OBSOLETE,
    SFO_NEW
  };

int
main (int argc, char **argv)
{
  int optc = 0;
  bool posixly_correct = (getenv ("POSIXLY_CORRECT") != NULL);
  enum Skip_field_option_type skip_field_option_type = SFO_NONE;
  int nfiles = 0;
  char const *file[2];
  char delimiter = '\n';	/* change with --zero-terminated, -z */

  file[0] = file[1] = "-";
  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);
  hard_LC_COLLATE = hard_locale (LC_COLLATE);

  atexit (close_stdout);

  skip_chars = 0;
  skip_fields = 0;
  check_chars = SIZE_MAX;
  output_unique = output_first_repeated = true;
  output_later_repeated = false;
  countmode = count_none;
  delimit_groups = DM_NONE;

  for (;;)
    {
      /* Parse an operand with leading "+" as a file after "--" was
         seen; or if pedantic and a file was seen; or if not
         obsolete.  */

      if (optc == -1
	  || (posixly_correct && nfiles != 0)
	  || ((optc = getopt_long (argc, argv,
				   "-0123456789Dcdf:is:uw:z", longopts, NULL))
	      == -1))
	{
	  if (argc <= optind)
	    break;
	  if (nfiles == 2)
	    {
	      error (0, 0, _("extra operand %s"), quote (argv[optind]));
	      usage (EXIT_FAILURE);
	    }
	  file[nfiles++] = argv[optind++];
	}
      else switch (optc)
	{
	case 1:
	  {
	    unsigned long int size;
	    if (optarg[0] == '+'
		&& posix2_version () < 200112
		&& xstrtoul (optarg, NULL, 10, &size, "") == LONGINT_OK
		&& size <= SIZE_MAX)
	      skip_chars = size;
	    else if (nfiles == 2)
	      {
		error (0, 0, _("extra operand %s"), quote (optarg));
		usage (EXIT_FAILURE);
	      }
	    else
	      file[nfiles++] = optarg;
	  }
	  break;

	case '0':
	case '1':
	case '2':
	case '3':
	case '4':
	case '5':
	case '6':
	case '7':
	case '8':
	case '9':
	  {
	    if (skip_field_option_type == SFO_NEW)
	      skip_fields = 0;

	    if (!DECIMAL_DIGIT_ACCUMULATE (skip_fields, optc - '0', size_t))
	      skip_fields = SIZE_MAX;

	    skip_field_option_type = SFO_OBSOLETE;
	  }
	  break;

	case 'c':
	  countmode = count_occurrences;
	  break;

	case 'd':
	  output_unique = false;
	  break;

	case 'D':
	  output_unique = false;
	  output_later_repeated = true;
	  if (optarg == NULL)
	    delimit_groups = DM_NONE;
	  else
	    delimit_groups = XARGMATCH ("--all-repeated", optarg,
					delimit_method_string,
					delimit_method_map);
	  break;

	case 'f':
	  skip_field_option_type = SFO_NEW;
	  skip_fields = size_opt (optarg,
				  N_("invalid number of fields to skip"));
	  break;

	case 'i':
	  ignore_case = true;
	  break;

	case 's':
	  skip_chars = size_opt (optarg,
				 N_("invalid number of bytes to skip"));
	  break;

	case 'u':
	  output_first_repeated = false;
	  break;

	case 'w':
	  check_chars = size_opt (optarg,
				  N_("invalid number of bytes to compare"));
	  break;

	case 'z':
	  delimiter = '\0';
	  break;

	case_GETOPT_HELP_CHAR;

	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);

	default:
	  usage (EXIT_FAILURE);
	}
    }

  if (countmode == count_occurrences && output_later_repeated)
    {
      error (0, 0,
	   _("printing all duplicated lines and repeat counts is meaningless"));
      usage (EXIT_FAILURE);
    }

  check_file (file[0], file[1], delimiter);

  exit (EXIT_SUCCESS);
}
