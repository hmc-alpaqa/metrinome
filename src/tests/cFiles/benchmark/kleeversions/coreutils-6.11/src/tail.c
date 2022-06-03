/* tail -- output the last part of file(s)
   Copyright (C) 1989, 90, 91, 1995-2006 Free Software Foundation, Inc.

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

/* Can display any amount of data, unlike the Unix version, which uses
   a fixed size buffer and therefore can only deliver a limited number
   of lines.

   Original version by Paul Rubin <phr@ocf.berkeley.edu>.
   Extensions by David MacKenzie <djm@gnu.ai.mit.edu>.
   tail -f for multiple files by Ian Lance Taylor <ian@airs.com>.  */

#include <config.h>

#include <stdio.h>
#include <assert.h>
#include <getopt.h>
#include <sys/types.h>
#include <signal.h>

#include "system.h"
#include "argmatch.h"
#include "c-strtod.h"
#include "error.h"
#include "fcntl--.h"
#include "inttostr.h"
#include "isapipe.h"
#include "posixver.h"
#include "quote.h"
#include "safe-read.h"
#include "stat-time.h"
#include "xnanosleep.h"
#include "xstrtol.h"
#include "xstrtod.h"

/* The official name of this program (e.g., no `g' prefix).  */
#define PROGRAM_NAME "tail"

#define AUTHORS \
  "Paul Rubin", "David MacKenzie, Ian Lance Taylor", "Jim Meyering"

/* Number of items to tail.  */
#define DEFAULT_N_LINES 10

/* Special values for dump_remainder's N_BYTES parameter.  */
#define COPY_TO_EOF UINTMAX_MAX
#define COPY_A_BUFFER (UINTMAX_MAX - 1)

/* FIXME: make Follow_name the default?  */
#define DEFAULT_FOLLOW_MODE Follow_descriptor

enum Follow_mode
{
  /* Follow the name of each file: if the file is renamed, try to reopen
     that name and track the end of the new file if/when it's recreated.
     This is useful for tracking logs that are occasionally rotated.  */
  Follow_name = 1,

  /* Follow each descriptor obtained upon opening a file.
     That means we'll continue to follow the end of a file even after
     it has been renamed or unlinked.  */
  Follow_descriptor = 2
};

/* The types of files for which tail works.  */
#define IS_TAILABLE_FILE_TYPE(Mode) \
  (S_ISREG (Mode) || S_ISFIFO (Mode) || S_ISSOCK (Mode) || S_ISCHR (Mode))

static char const *const follow_mode_string[] =
{
  "descriptor", "name", NULL
};

static enum Follow_mode const follow_mode_map[] =
{
  Follow_descriptor, Follow_name,
};

struct File_spec
{
  /* The actual file name, or "-" for stdin.  */
  char *name;

  /* File descriptor on which the file is open; -1 if it's not open.  */
  int fd;

  /* Attributes of the file the last time we checked.  */
  off_t size;
  struct timespec mtime;
  dev_t dev;
  ino_t ino;
  mode_t mode;

  /* 1 if O_NONBLOCK is clear, 0 if set, -1 if not known.  */
  int blocking;

  /* The specified name initially referred to a directory or some other
     type for which tail isn't meaningful.  Unlike for a permission problem
     (tailable, below) once this is set, the name is not checked ever again.  */
  bool ignore;

  /* See description of DEFAULT_MAX_N_... below.  */
  uintmax_t n_unchanged_stats;

  /* A file is tailable if it exists, is readable, and is of type
     IS_TAILABLE_FILE_TYPE.  */
  bool tailable;

  /* The value of errno seen last time we checked this file.  */
  int errnum;

};

/* Keep trying to open a file even if it is inaccessible when tail starts
   or if it becomes inaccessible later -- useful only with -f.  */
static bool reopen_inaccessible_files;

/* If true, interpret the numeric argument as the number of lines.
   Otherwise, interpret it as the number of bytes.  */
static bool count_lines;

/* Whether we follow the name of each file or the file descriptor
   that is initially associated with each name.  */
static enum Follow_mode follow_mode = Follow_descriptor;

/* If true, read from the ends of all specified files until killed.  */
static bool forever;

/* If true, count from start of file instead of end.  */
static bool from_start;

/* If true, print filename headers.  */
static bool print_headers;

/* When to print the filename banners.  */
enum header_mode
{
  multiple_files, always, never
};

/* When tailing a file by name, if there have been this many consecutive
   iterations for which the file has not changed, then open/fstat
   the file to determine if that file name is still associated with the
   same device/inode-number pair as before.  This option is meaningful only
   when following by name.  --max-unchanged-stats=N  */
#define DEFAULT_MAX_N_UNCHANGED_STATS_BETWEEN_OPENS 5
static uintmax_t max_n_unchanged_stats_between_opens =
  DEFAULT_MAX_N_UNCHANGED_STATS_BETWEEN_OPENS;

/* The name this program was run with.  */
char *program_name;

/* The process ID of the process (presumably on the current host)
   that is writing to all followed files.  */
static pid_t pid;

/* True if we have ever read standard input.  */
static bool have_read_stdin;

/* If nonzero, skip the is-regular-file test used to determine whether
   to use the lseek optimization.  Instead, use the more general (and
   more expensive) code unconditionally. Intended solely for testing.  */
static bool presume_input_pipe;

/* For long options that have no equivalent short option, use a
   non-character as a pseudo short option, starting with CHAR_MAX + 1.  */
enum
{
  RETRY_OPTION = CHAR_MAX + 1,
  MAX_UNCHANGED_STATS_OPTION,
  PID_OPTION,
  PRESUME_INPUT_PIPE_OPTION,
  LONG_FOLLOW_OPTION
};

static struct option const long_options[] =
{
  {"bytes", required_argument, NULL, 'c'},
  {"follow", optional_argument, NULL, LONG_FOLLOW_OPTION},
  {"lines", required_argument, NULL, 'n'},
  {"max-unchanged-stats", required_argument, NULL, MAX_UNCHANGED_STATS_OPTION},
  {"pid", required_argument, NULL, PID_OPTION},
  {"-presume-input-pipe", no_argument, NULL,
   PRESUME_INPUT_PIPE_OPTION}, /* do not document */
  {"quiet", no_argument, NULL, 'q'},
  {"retry", no_argument, NULL, RETRY_OPTION},
  {"silent", no_argument, NULL, 'q'},
  {"sleep-interval", required_argument, NULL, 's'},
  {"verbose", no_argument, NULL, 'v'},
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
"),
	      program_name);
      printf (_("\
Print the last %d lines of each FILE to standard output.\n\
With more than one FILE, precede each with a header giving the file name.\n\
With no FILE, or when FILE is -, read standard input.\n\
\n\
"), DEFAULT_N_LINES);
     fputs (_("\
Mandatory arguments to long options are mandatory for short options too.\n\
"), stdout);
     fputs (_("\
      --retry              keep trying to open a file even if it is\n\
                           inaccessible when tail starts or if it becomes\n\
                           inaccessible later; useful when following by name,\n\
                           i.e., with --follow=name\n\
  -c, --bytes=N            output the last N bytes; alternatively, use +N to\n\
                           output bytes starting with the Nth of each file\n\
"), stdout);
     fputs (_("\
  -f, --follow[={name|descriptor}]\n\
                           output appended data as the file grows;\n\
                           -f, --follow, and --follow=descriptor are\n\
                           equivalent\n\
  -F                       same as --follow=name --retry\n\
"), stdout);
     printf (_("\
  -n, --lines=N            output the last N lines, instead of the last %d;\n\
                           or use +N to output lines starting with the Nth\n\
      --max-unchanged-stats=N\n\
                           with --follow=name, reopen a FILE which has not\n\
                           changed size after N (default %d) iterations\n\
                           to see if it has been unlinked or renamed\n\
                           (this is the usual case of rotated log files)\n\
"),
	     DEFAULT_N_LINES,
	     DEFAULT_MAX_N_UNCHANGED_STATS_BETWEEN_OPENS
	     );
     fputs (_("\
      --pid=PID            with -f, terminate after process ID, PID dies\n\
  -q, --quiet, --silent    never output headers giving file names\n\
  -s, --sleep-interval=S   with -f, sleep for approximately S seconds\n\
                           (default 1.0) between iterations.\n\
  -v, --verbose            always output headers giving file names\n\
"), stdout);
     fputs (HELP_OPTION_DESCRIPTION, stdout);
     fputs (VERSION_OPTION_DESCRIPTION, stdout);
     fputs (_("\
\n\
If the first character of N (the number of bytes or lines) is a `+',\n\
print beginning with the Nth item from the start of each file, otherwise,\n\
print the last N items in the file.  N may have a multiplier suffix:\n\
b 512, kB 1000, K 1024, MB 1000*1000, M 1024*1024,\n\
GB 1000*1000*1000, G 1024*1024*1024, and so on for T, P, E, Z, Y.\n\
\n\
"), stdout);
     fputs (_("\
With --follow (-f), tail defaults to following the file descriptor, which\n\
means that even if a tail'ed file is renamed, tail will continue to track\n\
its end.  \
"), stdout);
     fputs (_("\
This default behavior is not desirable when you really want to\n\
track the actual name of the file, not the file descriptor (e.g., log\n\
rotation).  Use --follow=name in that case.  That causes tail to track the\n\
named file by reopening it periodically to see if it has been removed and\n\
recreated by some other program.\n\
"), stdout);
      emit_bug_reporting_address ();
    }
  exit (status);
}

static bool
valid_file_spec (struct File_spec const *f)
{
  /* Exactly one of the following subexpressions must be true. */
  return ((f->fd == -1) ^ (f->errnum == 0));
}

static char const *
pretty_name (struct File_spec const *f)
{
  return (STREQ (f->name, "-") ? "standard input" : f->name);
}

static void
xwrite_stdout (char const *buffer, size_t n_bytes)
{
  if (n_bytes > 0 && fwrite (buffer, 1, n_bytes, stdout) == 0)
    error (EXIT_FAILURE, errno, _("write error"));
}

/* Record a file F with descriptor FD, size SIZE, status ST, and
   blocking status BLOCKING.  */

static void
record_open_fd (struct File_spec *f, int fd,
		off_t size, struct stat const *st,
		int blocking)
{
  f->fd = fd;
  f->size = size;
  f->mtime = get_stat_mtime (st);
  f->dev = st->st_dev;
  f->ino = st->st_ino;
  f->mode = st->st_mode;
  f->blocking = blocking;
  f->n_unchanged_stats = 0;
  f->ignore = 0;
}

/* Close the file with descriptor FD and name FILENAME.  */

static void
close_fd (int fd, const char *filename)
{
  if (fd != -1 && fd != STDIN_FILENO && close (fd))
    {
      error (0, errno, _("closing %s (fd=%d)"), filename, fd);
    }
}

static void
write_header (const char *pretty_filename)
{
  static bool first_file = true;

  printf ("%s==> %s <==\n", (first_file ? "" : "\n"), pretty_filename);
  first_file = false;
}

/* Read and output N_BYTES of file PRETTY_FILENAME starting at the current
   position in FD.  If N_BYTES is COPY_TO_EOF, then copy until end of file.
   If N_BYTES is COPY_A_BUFFER, then copy at most one buffer's worth.
   Return the number of bytes read from the file.  */

static uintmax_t
dump_remainder (const char *pretty_filename, int fd, uintmax_t n_bytes)
{
  uintmax_t n_written;
  uintmax_t n_remaining = n_bytes;

  n_written = 0;
  while (1)
    {
      char buffer[BUFSIZ];
      size_t n = MIN (n_remaining, BUFSIZ);
      size_t bytes_read = safe_read (fd, buffer, n);
      if (bytes_read == SAFE_READ_ERROR)
	{
	  if (errno != EAGAIN)
	    error (EXIT_FAILURE, errno, _("error reading %s"),
		   quote (pretty_filename));
	  break;
	}
      if (bytes_read == 0)
	break;
      xwrite_stdout (buffer, bytes_read);
      n_written += bytes_read;
      if (n_bytes != COPY_TO_EOF)
	{
	  n_remaining -= bytes_read;
	  if (n_remaining == 0 || n_bytes == COPY_A_BUFFER)
	    break;
	}
    }

  return n_written;
}

/* Call lseek with the specified arguments, where file descriptor FD
   corresponds to the file, FILENAME.
   Give a diagnostic and exit nonzero if lseek fails.
   Otherwise, return the resulting offset.  */

static off_t
xlseek (int fd, off_t offset, int whence, char const *filename)
{
  off_t new_offset = lseek (fd, offset, whence);
  char buf[INT_BUFSIZE_BOUND (off_t)];
  char *s;

  if (0 <= new_offset)
    return new_offset;

  s = offtostr (offset, buf);
  switch (whence)
    {
    case SEEK_SET:
      error (0, errno, _("%s: cannot seek to offset %s"),
	     filename, s);
      break;
    case SEEK_CUR:
      error (0, errno, _("%s: cannot seek to relative offset %s"),
	     filename, s);
      break;
    case SEEK_END:
      error (0, errno, _("%s: cannot seek to end-relative offset %s"),
	     filename, s);
      break;
    default:
      abort ();
    }

  exit (EXIT_FAILURE);
}

/* Print the last N_LINES lines from the end of file FD.
   Go backward through the file, reading `BUFSIZ' bytes at a time (except
   probably the first), until we hit the start of the file or have
   read NUMBER newlines.
   START_POS is the starting position of the read pointer for the file
   associated with FD (may be nonzero).
   END_POS is the file offset of EOF (one larger than offset of last byte).
   Return true if successful.  */

static bool
file_lines (const char *pretty_filename, int fd, uintmax_t n_lines,
	    off_t start_pos, off_t end_pos, uintmax_t *read_pos)
{
  char buffer[BUFSIZ];
  size_t bytes_read;
  off_t pos = end_pos;

  if (n_lines == 0)
    return true;

  /* Set `bytes_read' to the size of the last, probably partial, buffer;
     0 < `bytes_read' <= `BUFSIZ'.  */
  bytes_read = (pos - start_pos) % BUFSIZ;
  if (bytes_read == 0)
    bytes_read = BUFSIZ;
  /* Make `pos' a multiple of `BUFSIZ' (0 if the file is short), so that all
     reads will be on block boundaries, which might increase efficiency.  */
  pos -= bytes_read;
  xlseek (fd, pos, SEEK_SET, pretty_filename);
  bytes_read = safe_read (fd, buffer, bytes_read);
  if (bytes_read == SAFE_READ_ERROR)
    {
      error (0, errno, _("error reading %s"), quote (pretty_filename));
      return false;
    }
  *read_pos = pos + bytes_read;

  /* Count the incomplete line on files that don't end with a newline.  */
  if (bytes_read && buffer[bytes_read - 1] != '\n')
    --n_lines;

  do
    {
      /* Scan backward, counting the newlines in this bufferfull.  */

      size_t n = bytes_read;
      while (n)
	{
	  char const *nl;
	  nl = memrchr (buffer, '\n', n);
	  if (nl == NULL)
	    break;
	  n = nl - buffer;
	  if (n_lines-- == 0)
	    {
	      /* If this newline isn't the last character in the buffer,
	         output the part that is after it.  */
	      if (n != bytes_read - 1)
		xwrite_stdout (nl + 1, bytes_read - (n + 1));
	      *read_pos += dump_remainder (pretty_filename, fd,
					   end_pos - (pos + bytes_read));
	      return true;
	    }
	}

      /* Not enough newlines in that bufferfull.  */
      if (pos == start_pos)
	{
	  /* Not enough lines in the file; print everything from
	     start_pos to the end.  */
	  xlseek (fd, start_pos, SEEK_SET, pretty_filename);
	  *read_pos = start_pos + dump_remainder (pretty_filename, fd,
						  end_pos);
	  return true;
	}
      pos -= BUFSIZ;
      xlseek (fd, pos, SEEK_SET, pretty_filename);

      bytes_read = safe_read (fd, buffer, BUFSIZ);
      if (bytes_read == SAFE_READ_ERROR)
	{
	  error (0, errno, _("error reading %s"), quote (pretty_filename));
	  return false;
	}

      *read_pos = pos + bytes_read;
    }
  while (bytes_read > 0);

  return true;
}

/* Print the last N_LINES lines from the end of the standard input,
   open for reading as pipe FD.
   Buffer the text as a linked list of LBUFFERs, adding them as needed.
   Return true if successful.  */

static bool
pipe_lines (const char *pretty_filename, int fd, uintmax_t n_lines,
	    uintmax_t *read_pos)
{
  struct linebuffer
  {
    char buffer[BUFSIZ];
    size_t nbytes;
    size_t nlines;
    struct linebuffer *next;
  };
  typedef struct linebuffer LBUFFER;
  LBUFFER *first, *last, *tmp;
  size_t total_lines = 0;	/* Total number of newlines in all buffers.  */
  bool ok = true;
  size_t n_read;		/* Size in bytes of most recent read */

  first = last = xmalloc (sizeof (LBUFFER));
  first->nbytes = first->nlines = 0;
  first->next = NULL;
  tmp = xmalloc (sizeof (LBUFFER));

  /* Input is always read into a fresh buffer.  */
  while (1)
    {
      n_read = safe_read (fd, tmp->buffer, BUFSIZ);
      if (n_read == 0 || n_read == SAFE_READ_ERROR)
	break;
      tmp->nbytes = n_read;
      *read_pos += n_read;
      tmp->nlines = 0;
      tmp->next = NULL;

      /* Count the number of newlines just read.  */
      {
	char const *buffer_end = tmp->buffer + n_read;
	char const *p = tmp->buffer;
	while ((p = memchr (p, '\n', buffer_end - p)))
	  {
	    ++p;
	    ++tmp->nlines;
	  }
      }
      total_lines += tmp->nlines;

      /* If there is enough room in the last buffer read, just append the new
         one to it.  This is because when reading from a pipe, `n_read' can
         often be very small.  */
      if (tmp->nbytes + last->nbytes < BUFSIZ)
	{
	  memcpy (&last->buffer[last->nbytes], tmp->buffer, tmp->nbytes);
	  last->nbytes += tmp->nbytes;
	  last->nlines += tmp->nlines;
	}
      else
	{
	  /* If there's not enough room, link the new buffer onto the end of
	     the list, then either free up the oldest buffer for the next
	     read if that would leave enough lines, or else malloc a new one.
	     Some compaction mechanism is possible but probably not
	     worthwhile.  */
	  last = last->next = tmp;
	  if (total_lines - first->nlines > n_lines)
	    {
	      tmp = first;
	      total_lines -= first->nlines;
	      first = first->next;
	    }
	  else
	    tmp = xmalloc (sizeof (LBUFFER));
	}
    }

  free (tmp);

  if (n_read == SAFE_READ_ERROR)
    {
      error (0, errno, _("error reading %s"), quote (pretty_filename));
      ok = false;
      goto free_lbuffers;
    }

  /* If the file is empty, then bail out.  */
  if (last->nbytes == 0)
    goto free_lbuffers;

  /* This prevents a core dump when the pipe contains no newlines.  */
  if (n_lines == 0)
    goto free_lbuffers;

  /* Count the incomplete line on files that don't end with a newline.  */
  if (last->buffer[last->nbytes - 1] != '\n')
    {
      ++last->nlines;
      ++total_lines;
    }

  /* Run through the list, printing lines.  First, skip over unneeded
     buffers.  */
  for (tmp = first; total_lines - tmp->nlines > n_lines; tmp = tmp->next)
    total_lines -= tmp->nlines;

  /* Find the correct beginning, then print the rest of the file.  */
  {
    char const *beg = tmp->buffer;
    char const *buffer_end = tmp->buffer + tmp->nbytes;
    if (total_lines > n_lines)
      {
	/* Skip `total_lines' - `n_lines' newlines.  We made sure that
	   `total_lines' - `n_lines' <= `tmp->nlines'.  */
	size_t j;
	for (j = total_lines - n_lines; j; --j)
	  {
	    beg = memchr (beg, '\n', buffer_end - beg);
	    assert (beg);
	    ++beg;
	  }
      }

    xwrite_stdout (beg, buffer_end - beg);
  }

  for (tmp = tmp->next; tmp; tmp = tmp->next)
    xwrite_stdout (tmp->buffer, tmp->nbytes);

free_lbuffers:
  while (first)
    {
      tmp = first->next;
      free (first);
      first = tmp;
    }
  return ok;
}

/* Print the last N_BYTES characters from the end of pipe FD.
   This is a stripped down version of pipe_lines.
   Return true if successful.  */

static bool
pipe_bytes (const char *pretty_filename, int fd, uintmax_t n_bytes,
	    uintmax_t *read_pos)
{
  struct charbuffer
  {
    char buffer[BUFSIZ];
    size_t nbytes;
    struct charbuffer *next;
  };
  typedef struct charbuffer CBUFFER;
  CBUFFER *first, *last, *tmp;
  size_t i;			/* Index into buffers.  */
  size_t total_bytes = 0;	/* Total characters in all buffers.  */
  bool ok = true;
  size_t n_read;

  first = last = xmalloc (sizeof (CBUFFER));
  first->nbytes = 0;
  first->next = NULL;
  tmp = xmalloc (sizeof (CBUFFER));

  /* Input is always read into a fresh buffer.  */
  while (1)
    {
      n_read = safe_read (fd, tmp->buffer, BUFSIZ);
      if (n_read == 0 || n_read == SAFE_READ_ERROR)
	break;
      *read_pos += n_read;
      tmp->nbytes = n_read;
      tmp->next = NULL;

      total_bytes += tmp->nbytes;
      /* If there is enough room in the last buffer read, just append the new
         one to it.  This is because when reading from a pipe, `nbytes' can
         often be very small.  */
      if (tmp->nbytes + last->nbytes < BUFSIZ)
	{
	  memcpy (&last->buffer[last->nbytes], tmp->buffer, tmp->nbytes);
	  last->nbytes += tmp->nbytes;
	}
      else
	{
	  /* If there's not enough room, link the new buffer onto the end of
	     the list, then either free up the oldest buffer for the next
	     read if that would leave enough characters, or else malloc a new
	     one.  Some compaction mechanism is possible but probably not
	     worthwhile.  */
	  last = last->next = tmp;
	  if (total_bytes - first->nbytes > n_bytes)
	    {
	      tmp = first;
	      total_bytes -= first->nbytes;
	      first = first->next;
	    }
	  else
	    {
	      tmp = xmalloc (sizeof (CBUFFER));
	    }
	}
    }

  free (tmp);

  if (n_read == SAFE_READ_ERROR)
    {
      error (0, errno, _("error reading %s"), quote (pretty_filename));
      ok = false;
      goto free_cbuffers;
    }

  /* Run through the list, printing characters.  First, skip over unneeded
     buffers.  */
  for (tmp = first; total_bytes - tmp->nbytes > n_bytes; tmp = tmp->next)
    total_bytes -= tmp->nbytes;

  /* Find the correct beginning, then print the rest of the file.
     We made sure that `total_bytes' - `n_bytes' <= `tmp->nbytes'.  */
  if (total_bytes > n_bytes)
    i = total_bytes - n_bytes;
  else
    i = 0;
  xwrite_stdout (&tmp->buffer[i], tmp->nbytes - i);

  for (tmp = tmp->next; tmp; tmp = tmp->next)
    xwrite_stdout (tmp->buffer, tmp->nbytes);

free_cbuffers:
  while (first)
    {
      tmp = first->next;
      free (first);
      first = tmp;
    }
  return ok;
}

/* Skip N_BYTES characters from the start of pipe FD, and print
   any extra characters that were read beyond that.
   Return 1 on error, 0 if ok, -1 if EOF.  */

static int
start_bytes (const char *pretty_filename, int fd, uintmax_t n_bytes,
	     uintmax_t *read_pos)
{
  char buffer[BUFSIZ];

  while (0 < n_bytes)
    {
      size_t bytes_read = safe_read (fd, buffer, BUFSIZ);
      if (bytes_read == 0)
	return -1;
      if (bytes_read == SAFE_READ_ERROR)
	{
	  error (0, errno, _("error reading %s"), quote (pretty_filename));
	  return 1;
	}
      read_pos += bytes_read;
      if (bytes_read <= n_bytes)
	n_bytes -= bytes_read;
      else
	{
	  size_t n_remaining = bytes_read - n_bytes;
	  if (n_remaining)
	    xwrite_stdout (&buffer[n_bytes], n_remaining);
	  break;
	}
    }

  return 0;
}

/* Skip N_LINES lines at the start of file or pipe FD, and print
   any extra characters that were read beyond that.
   Return 1 on error, 0 if ok, -1 if EOF.  */

static int
start_lines (const char *pretty_filename, int fd, uintmax_t n_lines,
	     uintmax_t *read_pos)
{
  if (n_lines == 0)
    return 0;

  while (1)
    {
      char buffer[BUFSIZ];
      char *p = buffer;
      size_t bytes_read = safe_read (fd, buffer, BUFSIZ);
      char *buffer_end = buffer + bytes_read;
      if (bytes_read == 0) /* EOF */
	return -1;
      if (bytes_read == SAFE_READ_ERROR) /* error */
	{
	  error (0, errno, _("error reading %s"), quote (pretty_filename));
	  return 1;
	}

      *read_pos += bytes_read;

      while ((p = memchr (p, '\n', buffer_end - p)))
	{
	  ++p;
	  if (--n_lines == 0)
	    {
	      if (p < buffer_end)
		xwrite_stdout (p, buffer_end - p);
	      return 0;
	    }
	}
    }
}

/* FIXME: describe */

static void
recheck (struct File_spec *f, bool blocking)
{
  /* open/fstat the file and announce if dev/ino have changed */
  struct stat new_stats;
  bool ok = true;
  bool is_stdin = (STREQ (f->name, "-"));
  bool was_tailable = f->tailable;
  int prev_errnum = f->errnum;
  bool new_file;
  int fd = (is_stdin
	    ? STDIN_FILENO
	    : open (f->name, O_RDONLY | (blocking ? 0 : O_NONBLOCK)));

  assert (valid_file_spec (f));

  /* If the open fails because the file doesn't exist,
     then mark the file as not tailable.  */
  f->tailable = !(reopen_inaccessible_files && fd == -1);

  if (fd == -1 || fstat (fd, &new_stats) < 0)
    {
      ok = false;
      f->errnum = errno;
      if (!f->tailable)
	{
	  if (was_tailable)
	    {
	      /* FIXME-maybe: detect the case in which the file first becomes
		 unreadable (perms), and later becomes readable again and can
		 be seen to be the same file (dev/ino).  Otherwise, tail prints
		 the entire contents of the file when it becomes readable.  */
	      error (0, f->errnum, _("%s has become inaccessible"),
		     quote (pretty_name (f)));
	    }
	  else
	    {
	      /* say nothing... it's still not tailable */
	    }
	}
      else if (prev_errnum != errno)
	{
	  error (0, errno, "%s", pretty_name (f));
	}
    }
  else if (!IS_TAILABLE_FILE_TYPE (new_stats.st_mode))
    {
      ok = false;
      f->errnum = -1;
      error (0, 0, _("%s has been replaced with an untailable file;\
 giving up on this name"),
	     quote (pretty_name (f)));
      f->ignore = true;
    }
  else
    {
      f->errnum = 0;
    }

  new_file = false;
  if (!ok)
    {
      close_fd (fd, pretty_name (f));
      close_fd (f->fd, pretty_name (f));
      f->fd = -1;
    }
  else if (prev_errnum && prev_errnum != ENOENT)
    {
      new_file = true;
      assert (f->fd == -1);
      error (0, 0, _("%s has become accessible"), quote (pretty_name (f)));
    }
  else if (f->ino != new_stats.st_ino || f->dev != new_stats.st_dev)
    {
      new_file = true;
      if (f->fd == -1)
	{
	  error (0, 0,
		 _("%s has appeared;  following end of new file"),
		 quote (pretty_name (f)));
	}
      else
	{
	  /* Close the old one.  */
	  close_fd (f->fd, pretty_name (f));

	  /* File has been replaced (e.g., via log rotation) --
	     tail the new one.  */
	  error (0, 0,
		 _("%s has been replaced;  following end of new file"),
		 quote (pretty_name (f)));
	}
    }
  else
    {
      if (f->fd == -1)
	{
	  /* This happens when one iteration finds the file missing,
	     then the preceding <dev,inode> pair is reused as the
	     file is recreated.  */
	  new_file = true;
	}
      else
	{
	  close_fd (fd, pretty_name (f));
	}
    }

  if (new_file)
    {
      /* Start at the beginning of the file.  */
      record_open_fd (f, fd, 0, &new_stats, (is_stdin ? -1 : blocking));
      xlseek (fd, 0, SEEK_SET, pretty_name (f));
    }
}

/* Return true if any of the N_FILES files in F are live, i.e., have
   open file descriptors.  */

static bool
any_live_files (const struct File_spec *f, int n_files)
{
  int i;

  for (i = 0; i < n_files; i++)
    if (0 <= f[i].fd)
      return true;
  return false;
}

/* Tail NFILES files forever, or until killed.
   The pertinent information for each file is stored in an entry of F.
   Loop over each of them, doing an fstat to see if they have changed size,
   and an occasional open/fstat to see if any dev/ino pair has changed.
   If none of them have changed size in one iteration, sleep for a
   while and try again.  Continue until the user interrupts us.  */

static void
tail_forever (struct File_spec *f, int nfiles, double sleep_interval)
{
  /* Use blocking I/O as an optimization, when it's easy.  */
  bool blocking = (pid == 0 && follow_mode == Follow_descriptor
		   && nfiles == 1 && ! S_ISREG (f[0].mode));
  int last;
  bool writer_is_dead = false;

  last = nfiles - 1;

  while (1)
    {
      int i;
      bool any_input = false;

      for (i = 0; i < nfiles; i++)
	{
	  int fd;
	  char const *name;
	  mode_t mode;
	  struct stat stats;
	  uintmax_t bytes_read;

	  if (f[i].ignore)
	    continue;

	  if (f[i].fd < 0)
	    {
	      recheck (&f[i], blocking);
	      continue;
	    }

	  fd = f[i].fd;
	  name = pretty_name (&f[i]);
	  mode = f[i].mode;

	  if (f[i].blocking != blocking)
	    {
	      int old_flags = fcntl (fd, F_GETFL);
	      int new_flags = old_flags | (blocking ? 0 : O_NONBLOCK);
	      if (old_flags < 0
		  || (new_flags != old_flags
		      && fcntl (fd, F_SETFL, new_flags) == -1))
		{
		  /* Don't update f[i].blocking if fcntl fails.  */
		  if (S_ISREG (f[i].mode) && errno == EPERM)
		    {
		      /* This happens when using tail -f on a file with
			 the append-only attribute.  */
		    }
		  else
		    error (EXIT_FAILURE, errno,
			   _("%s: cannot change nonblocking mode"), name);
		}
	      else
		f[i].blocking = blocking;
	    }

	  if (!f[i].blocking)
	    {
	      if (fstat (fd, &stats) != 0)
		{
		  f[i].fd = -1;
		  f[i].errnum = errno;
		  error (0, errno, "%s", name);
		  continue;
		}

	      if (f[i].mode == stats.st_mode
		  && (! S_ISREG (stats.st_mode) || f[i].size == stats.st_size)
		  && timespec_cmp (f[i].mtime, get_stat_mtime (&stats)) == 0)
		{
		  if ((max_n_unchanged_stats_between_opens
		       <= f[i].n_unchanged_stats++)
		      && follow_mode == Follow_name)
		    {
		      recheck (&f[i], f[i].blocking);
		      f[i].n_unchanged_stats = 0;
		    }
		  continue;
		}

	      /* This file has changed.  Print out what we can, and
		 then keep looping.  */

	      f[i].mtime = get_stat_mtime (&stats);
	      f[i].mode = stats.st_mode;

	      /* reset counter */
	      f[i].n_unchanged_stats = 0;

	      if (S_ISREG (mode) && stats.st_size < f[i].size)
		{
		  error (0, 0, _("%s: file truncated"), name);
		  last = i;
		  xlseek (fd, stats.st_size, SEEK_SET, name);
		  f[i].size = stats.st_size;
		  continue;
		}

	      if (i != last)
		{
		  if (print_headers)
		    write_header (name);
		  last = i;
		}
	    }

	  bytes_read = dump_remainder (name, fd,
				       (f[i].blocking
					? COPY_A_BUFFER : COPY_TO_EOF));
	  any_input |= (bytes_read != 0);
	  f[i].size += bytes_read;
	}

      if (! any_live_files (f, nfiles) && ! reopen_inaccessible_files)
	{
	  error (0, 0, _("no files remaining"));
	  break;
	}

      if ((!any_input | blocking) && fflush (stdout) != 0)
	error (EXIT_FAILURE, errno, _("write error"));

      /* If nothing was read, sleep and/or check for dead writers.  */
      if (!any_input)
	{
	  if (writer_is_dead)
	    break;

	  if (xnanosleep (sleep_interval))
	    error (EXIT_FAILURE, errno, _("cannot read realtime clock"));

	  /* Once the writer is dead, read the files once more to
	     avoid a race condition.  */
	  writer_is_dead = (pid != 0
			    && kill (pid, 0) != 0
			    /* Handle the case in which you cannot send a
			       signal to the writer, so kill fails and sets
			       errno to EPERM.  */
			    && errno != EPERM);
	}
    }
}

/* Output the last N_BYTES bytes of file FILENAME open for reading in FD.
   Return true if successful.  */

static bool
tail_bytes (const char *pretty_filename, int fd, uintmax_t n_bytes,
	    uintmax_t *read_pos)
{
  struct stat stats;

  if (fstat (fd, &stats))
    {
      error (0, errno, _("cannot fstat %s"), quote (pretty_filename));
      return false;
    }

  if (from_start)
    {
      if ( ! presume_input_pipe
	   && S_ISREG (stats.st_mode) && n_bytes <= OFF_T_MAX)
	{
	  xlseek (fd, n_bytes, SEEK_CUR, pretty_filename);
	  *read_pos += n_bytes;
	}
      else
	{
	  int t = start_bytes (pretty_filename, fd, n_bytes, read_pos);
	  if (t)
	    return t < 0;
	}
      *read_pos += dump_remainder (pretty_filename, fd, COPY_TO_EOF);
    }
  else
    {
      if ( ! presume_input_pipe
	   && S_ISREG (stats.st_mode) && n_bytes <= OFF_T_MAX)
	{
	  off_t current_pos = xlseek (fd, 0, SEEK_CUR, pretty_filename);
	  off_t end_pos = xlseek (fd, 0, SEEK_END, pretty_filename);
	  off_t diff = end_pos - current_pos;
	  /* Be careful here.  The current position may actually be
	     beyond the end of the file.  */
	  off_t bytes_remaining = (diff = end_pos - current_pos) < 0 ? 0 : diff;
	  off_t nb = n_bytes;

	  if (bytes_remaining <= nb)
	    {
	      /* From the current position to end of file, there are no
		 more bytes than have been requested.  So reposition the
		 file pointer to the incoming current position and print
		 everything after that.  */
	      *read_pos = xlseek (fd, current_pos, SEEK_SET, pretty_filename);
	    }
	  else
	    {
	      /* There are more bytes remaining than were requested.
		 Back up.  */
	      *read_pos = xlseek (fd, -nb, SEEK_END, pretty_filename);
	    }
	  *read_pos += dump_remainder (pretty_filename, fd, n_bytes);
	}
      else
	return pipe_bytes (pretty_filename, fd, n_bytes, read_pos);
    }
  return true;
}

/* Output the last N_LINES lines of file FILENAME open for reading in FD.
   Return true if successful.  */

static bool
tail_lines (const char *pretty_filename, int fd, uintmax_t n_lines,
	    uintmax_t *read_pos)
{
  struct stat stats;

  if (fstat (fd, &stats))
    {
      error (0, errno, _("cannot fstat %s"), quote (pretty_filename));
      return false;
    }

  if (from_start)
    {
      int t = start_lines (pretty_filename, fd, n_lines, read_pos);
      if (t)
	return t < 0;
      *read_pos += dump_remainder (pretty_filename, fd, COPY_TO_EOF);
    }
  else
    {
      off_t start_pos = -1;
      off_t end_pos;

      /* Use file_lines only if FD refers to a regular file for
	 which lseek (... SEEK_END) works.  */
      if ( ! presume_input_pipe
	   && S_ISREG (stats.st_mode)
	   && (start_pos = lseek (fd, 0, SEEK_CUR)) != -1
	   && start_pos < (end_pos = lseek (fd, 0, SEEK_END)))
	{
	  *read_pos = end_pos;
	  if (end_pos != 0
	      && ! file_lines (pretty_filename, fd, n_lines,
			       start_pos, end_pos, read_pos))
	    return false;
	}
      else
	{
	  /* Under very unlikely circumstances, it is possible to reach
	     this point after positioning the file pointer to end of file
	     via the `lseek (...SEEK_END)' above.  In that case, reposition
	     the file pointer back to start_pos before calling pipe_lines.  */
	  if (start_pos != -1)
	    xlseek (fd, start_pos, SEEK_SET, pretty_filename);

	  return pipe_lines (pretty_filename, fd, n_lines, read_pos);
	}
    }
  return true;
}

/* Display the last N_UNITS units of file FILENAME, open for reading
   via FD.  Set *READ_POS to the position of the input stream pointer.
   *READ_POS is usually the number of bytes read and corresponds to an
   offset from the beginning of a file.  However, it may be larger than
   OFF_T_MAX (as for an input pipe), and may also be larger than the
   number of bytes read (when an input pointer is initially not at
   beginning of file), and may be far greater than the number of bytes
   actually read for an input file that is seekable.
   Return true if successful.  */

static bool
tail (const char *filename, int fd, uintmax_t n_units,
      uintmax_t *read_pos)
{
  *read_pos = 0;
  if (count_lines)
    return tail_lines (filename, fd, n_units, read_pos);
  else
    return tail_bytes (filename, fd, n_units, read_pos);
}

/* Display the last N_UNITS units of the file described by F.
   Return true if successful.  */

static bool
tail_file (struct File_spec *f, uintmax_t n_units)
{
  int fd;
  bool ok;

  bool is_stdin = (STREQ (f->name, "-"));

  if (is_stdin)
    {
      have_read_stdin = true;
      fd = STDIN_FILENO;
      if (O_BINARY && ! isatty (STDIN_FILENO))
	freopen (NULL, "rb", stdin);
    }
  else
    fd = open (f->name, O_RDONLY | O_BINARY);

  f->tailable = !(reopen_inaccessible_files && fd == -1);

  if (fd == -1)
    {
      if (forever)
	{
	  f->fd = -1;
	  f->errnum = errno;
	  f->ignore = false;
	  f->ino = 0;
	  f->dev = 0;
	}
      error (0, errno, _("cannot open %s for reading"),
	     quote (pretty_name (f)));
      ok = false;
    }
  else
    {
      uintmax_t read_pos;

      if (print_headers)
	write_header (pretty_name (f));
      ok = tail (pretty_name (f), fd, n_units, &read_pos);
      if (forever)
	{
	  struct stat stats;

#if TEST_RACE_BETWEEN_FINAL_READ_AND_INITIAL_FSTAT
	  /* Before the tail function provided `read_pos', there was
	     a race condition described in the URL below.  This sleep
	     call made the window big enough to exercise the problem.  */
	  sleep (1);
#endif
	  f->errnum = ok - 1;
	  if (fstat (fd, &stats) < 0)
	    {
	      ok = false;
	      f->errnum = errno;
	      error (0, errno, _("error reading %s"), quote (pretty_name (f)));
	    }
	  else if (!IS_TAILABLE_FILE_TYPE (stats.st_mode))
	    {
	      error (0, 0, _("%s: cannot follow end of this type of file;\
 giving up on this name"),
		     pretty_name (f));
	      ok = false;
	      f->errnum = -1;
	      f->ignore = true;
	    }

	  if (!ok)
	    {
	      close_fd (fd, pretty_name (f));
	      f->fd = -1;
	    }
	  else
	    {
	      /* Note: we must use read_pos here, not stats.st_size,
		 to avoid a race condition described by Ken Raeburn:
	http://mail.gnu.org/archive/html/bug-textutils/2003-05/msg00007.html */
	      record_open_fd (f, fd, read_pos, &stats, (is_stdin ? -1 : 1));
	    }
	}
      else
	{
	  if (!is_stdin && close (fd))
	    {
	      error (0, errno, _("error reading %s"), quote (pretty_name (f)));
	      ok = false;
	    }
	}
    }

  return ok;
}

/* If obsolete usage is allowed, and the command line arguments are of
   the obsolete form and the option string is well-formed, set
   *N_UNITS, the globals COUNT_LINES, FOREVER, and FROM_START, and
   return true.  If the command line arguments are obviously incorrect
   (e.g., because obsolete usage is not allowed and the arguments are
   incorrect for non-obsolete usage), report an error and exit.
   Otherwise, return false and don't modify any parameter or global
   variable.  */

static bool
parse_obsolete_option (int argc, char * const *argv, uintmax_t *n_units)
{
  const char *p;
  const char *n_string;
  const char *n_string_end;
  bool obsolete_usage;
  int default_count = DEFAULT_N_LINES;
  bool t_from_start;
  bool t_count_lines = true;
  bool t_forever = false;

  /* With the obsolete form, there is one option string and at most
     one file argument.  Watch out for "-" and "--", though.  */
  if (! (argc == 2
	 || (argc == 3 && ! (argv[2][0] == '-' && argv[2][1]))
	 || (3 <= argc && argc <= 4 && STREQ (argv[2], "--"))))
    return false;

  obsolete_usage = (posix2_version () < 200112);
  p = argv[1];

  switch (*p++)
    {
    default:
      return false;

    case '+':
      /* Leading "+" is a file name in the non-obsolete form.  */
      if (!obsolete_usage)
	return false;

      t_from_start = true;
      break;

    case '-':
      /* In the non-obsolete form, "-" is standard input and "-c"
	 requires an option-argument.  The obsolete multidigit options
	 are supported as a GNU extension even when conforming to
	 POSIX 1003.1-2001, so don't complain about them.  */
      if (!obsolete_usage && !p[p[0] == 'c'])
	return false;

      t_from_start = false;
      break;
    }

  n_string = p;
  while (ISDIGIT (*p))
    p++;
  n_string_end = p;

  switch (*p)
    {
    case 'b': default_count *= 512;	/* Fall through.  */
    case 'c': t_count_lines = false;	/* Fall through.  */
    case 'l': p++; break;
    }

  if (*p == 'f')
    {
      t_forever = true;
      ++p;
    }

  if (*p)
    return false;

  if (n_string == n_string_end)
    *n_units = default_count;
  else if ((xstrtoumax (n_string, NULL, 10, n_units, "b")
	    & ~LONGINT_INVALID_SUFFIX_CHAR)
	   != LONGINT_OK)
    error (EXIT_FAILURE, 0, _("number in %s is too large"), quote (argv[1]));

  /* Set globals.  */
  from_start = t_from_start;
  count_lines = t_count_lines;
  forever = t_forever;

  return true;
}

static void
parse_options (int argc, char **argv,
	       uintmax_t *n_units, enum header_mode *header_mode,
	       double *sleep_interval)
{
  int c;

  while ((c = getopt_long (argc, argv, "c:n:fFqs:v0123456789",
			   long_options, NULL))
	 != -1)
    {
      switch (c)
	{
	case 'F':
	  forever = true;
	  follow_mode = Follow_name;
	  reopen_inaccessible_files = true;
	  break;

	case 'c':
	case 'n':
	  count_lines = (c == 'n');
	  if (*optarg == '+')
	    from_start = true;
	  else if (*optarg == '-')
	    ++optarg;

	  {
	    strtol_error s_err;
	    s_err = xstrtoumax (optarg, NULL, 10, n_units, "bkKmMGTPEZY0");
	    if (s_err != LONGINT_OK)
	      {
		error (EXIT_FAILURE, 0, "%s: %s", optarg,
		       (c == 'n'
			? _("invalid number of lines")
			: _("invalid number of bytes")));
	      }
	  }
	  break;

	case 'f':
	case LONG_FOLLOW_OPTION:
	  forever = true;
	  if (optarg == NULL)
	    follow_mode = DEFAULT_FOLLOW_MODE;
	  else
	    follow_mode = XARGMATCH ("--follow", optarg,
				     follow_mode_string, follow_mode_map);
	  break;

	case RETRY_OPTION:
	  reopen_inaccessible_files = true;
	  break;

	case MAX_UNCHANGED_STATS_OPTION:
	  /* --max-unchanged-stats=N */
	  if (xstrtoumax (optarg, NULL, 10,
			  &max_n_unchanged_stats_between_opens,
			  "")
	      != LONGINT_OK)
	    {
	      error (EXIT_FAILURE, 0,
	       _("%s: invalid maximum number of unchanged stats between opens"),
		     optarg);
	    }
	  break;

	case PID_OPTION:
	  {
	    strtol_error s_err;
	    unsigned long int tmp_ulong;
	    s_err = xstrtoul (optarg, NULL, 10, &tmp_ulong, "");
	    if (s_err != LONGINT_OK || tmp_ulong > PID_T_MAX)
	      {
		error (EXIT_FAILURE, 0, _("%s: invalid PID"), optarg);
	      }
	    pid = tmp_ulong;
	  }
	  break;

	case PRESUME_INPUT_PIPE_OPTION:
	  presume_input_pipe = true;
	  break;

	case 'q':
	  *header_mode = never;
	  break;

	case 's':
	  {
	    double s;
	    if (! (xstrtod (optarg, NULL, &s, c_strtod) && 0 <= s))
	      error (EXIT_FAILURE, 0,
		     _("%s: invalid number of seconds"), optarg);
	    *sleep_interval = s;
	  }
	  break;

	case 'v':
	  *header_mode = always;
	  break;

	case_GETOPT_HELP_CHAR;

	case_GETOPT_VERSION_CHAR (PROGRAM_NAME, AUTHORS);

	case '0': case '1': case '2': case '3': case '4':
	case '5': case '6': case '7': case '8': case '9':
	  error (EXIT_FAILURE, 0,
		 _("option used in invalid context -- %c"), c);

	default:
	  usage (EXIT_FAILURE);
	}
    }

  if (reopen_inaccessible_files && follow_mode != Follow_name)
    error (0, 0, _("warning: --retry is useful mainly when following by name"));

  if (pid && !forever)
    error (0, 0,
	   _("warning: PID ignored; --pid=PID is useful only when following"));
  else if (pid && kill (pid, 0) != 0 && errno == ENOSYS)
    {
      error (0, 0, _("warning: --pid=PID is not supported on this system"));
      pid = 0;
    }
}

int
main (int argc, char **argv)
{
  enum header_mode header_mode = multiple_files;
  bool ok = true;
  /* If from_start, the number of items to skip before printing; otherwise,
     the number of items at the end of the file to print.  Although the type
     is signed, the value is never negative.  */
  uintmax_t n_units = DEFAULT_N_LINES;
  int n_files;
  char **file;
  struct File_spec *F;
  int i;
  bool obsolete_option;

  /* The number of seconds to sleep between iterations.
     During one iteration, every file name or descriptor is checked to
     see if it has changed.  */
  double sleep_interval = 1.0;

  initialize_main (&argc, &argv);
  program_name = argv[0];
  setlocale (LC_ALL, "");
  bindtextdomain (PACKAGE, LOCALEDIR);
  textdomain (PACKAGE);

  atexit (close_stdout);

  have_read_stdin = false;

  count_lines = true;
  forever = from_start = print_headers = false;
  obsolete_option = parse_obsolete_option (argc, argv, &n_units);
  argc -= obsolete_option;
  argv += obsolete_option;
  parse_options (argc, argv, &n_units, &header_mode, &sleep_interval);

  /* To start printing with item N_UNITS from the start of the file, skip
     N_UNITS - 1 items.  `tail -n +0' is actually meaningless, but for Unix
     compatibility it's treated the same as `tail -n +1'.  */
  if (from_start)
    {
      if (n_units)
	--n_units;
    }

  if (optind < argc)
    {
      n_files = argc - optind;
      file = argv + optind;
    }
  else
    {
      static char *dummy_stdin = "-";
      n_files = 1;
      file = &dummy_stdin;

      /* POSIX says that -f is ignored if no file operand is specified
	 and standard input is a pipe.  However, the GNU coding
	 standards say that program behavior should not depend on
	 device type, because device independence is an important
	 principle of the system's design.

	 Follow the POSIX requirement only if POSIXLY_CORRECT is set.  */

      if (forever && getenv ("POSIXLY_CORRECT"))
	{
	  struct stat st;
	  int is_a_fifo_or_pipe =
	    (fstat (STDIN_FILENO, &st) != 0 ? -1
	     : S_ISFIFO (st.st_mode) ? 1
	     : HAVE_FIFO_PIPES == 1 ? 0
	     : isapipe (STDIN_FILENO));
	  if (is_a_fifo_or_pipe < 0)
	    error (EXIT_FAILURE, errno, _("standard input"));
	  if (is_a_fifo_or_pipe)
	    forever = false;
	}
    }

  {
    bool found_hyphen = false;

    for (i = 0; i < n_files; i++)
      if (STREQ (file[i], "-"))
	found_hyphen = true;

    /* When following by name, there must be a name.  */
    if (found_hyphen && follow_mode == Follow_name)
      error (EXIT_FAILURE, 0, _("cannot follow %s by name"), quote ("-"));

    /* When following forever, warn if any file is `-'.
       This is only a warning, since tail's output (before a failing seek,
       and that from any non-stdin files) might still be useful.  */
    if (forever && found_hyphen && isatty (STDIN_FILENO))
      error (0, 0, _("warning: following standard input"
		     " indefinitely is ineffective"));
  }

  F = xnmalloc (n_files, sizeof *F);
  for (i = 0; i < n_files; i++)
    F[i].name = file[i];

  if (header_mode == always
      || (header_mode == multiple_files && n_files > 1))
    print_headers = true;

  if (O_BINARY && ! isatty (STDOUT_FILENO))
    freopen (NULL, "wb", stdout);

  for (i = 0; i < n_files; i++)
    ok &= tail_file (&F[i], n_units);

  if (forever)
    tail_forever (F, n_files, sleep_interval);

  if (have_read_stdin && close (STDIN_FILENO) < 0)
    error (EXIT_FAILURE, errno, "-");
  exit (ok ? EXIT_SUCCESS : EXIT_FAILURE);
}
