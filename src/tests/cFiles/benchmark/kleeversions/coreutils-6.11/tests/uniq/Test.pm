# Test "uniq".

# Copyright (C) 1998, 1999, 2001-2007 Free Software Foundation, Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

package Test;
require 5.002;
use strict;

$Test::input_via_stdin = 1;

my @tv = (
# test flags  input              expected output    expected return code
#
['1',  '',    '',                '',                0],
['2',  '',    "a\na\n",          "a\n",             0],
['3',  '',    "a\na",            "a\n",             0],
['4',  '',    "a\nb",            "a\nb\n",          0],
['5',  '',    "a\na\nb",         "a\nb\n",          0],
['6',  '',    "b\na\na\n",       "b\na\n",          0],
['7',  '',    "a\nb\nc\n",       "a\nb\nc\n",       0],

# Ensure that newlines are not interpreted with -z.
['2z', '-z',  "a\na\n",          "a\na\n\0",        0],
['3z', '-z',  "a\na",            "a\na\0",          0],
['4z', '-z',  "a\nb",            "a\nb\0",          0],
['5z', '-z',  "a\na\nb",         "a\na\nb\0",       0],
['20z','-dz', "a\na\n",          "",                0],

# Make sure that eight bit characters work
['8',  '',    "ö\nv\n",          "ö\nv\n",          0],
# Test output of -u option; only unique lines
['9',  '-u',  "a\na\n",          "",                0],
['10', '-u',  "a\nb\n",          "a\nb\n",          0],
['11', '-u',  "a\nb\na\n",       "a\nb\na\n",       0],
['12', '-u',  "a\na\n",          "",                0],
['13', '-u',  "a\na\n",          "",                0],
#['5',  '-u',  "a\na\n",          "",                0],
# Test output of -d option; only repeated lines
['20', '-d',  "a\na\n",          "a\n",             0],
['21', '-d',  "a\nb\n",          "",                0],
['22', '-d',  "a\nb\na\n",       "",                0],
['23', '-d',  "a\na\nb\n",       "a\n",             0],
# Check the key options
# If we skip over fields or characters, is the output deterministic?
['obs30', '-1',  "a a\nb a\n",      "a a\n",           0],
['31', '-f 1',"a a\nb a\n",      "a a\n",           0],
['32', '-f 1',"a a\nb b\n",      "a a\nb b\n",      0],
['33', '-f 1',"a a a\nb a c\n",  "a a a\nb a c\n",  0],
['34', '-f 1',"b a\na a\n",      "b a\n",           0],
['35', '-f 2',"a a c\nb a c\n",  "a a c\n",         0],
# Skip over characters.
['obs-plus40', '+1',  "aaa\naaa\n",      "aaa\n",           0],
['obs-plus41', '+1',  "baa\naaa\n",      "baa\n",           0],
['42', '-s 1',"aaa\naaa\n",      "aaa\n",           0],
['43', '-s 2',"baa\naaa\n",      "baa\n",           0],
['obs-plus44', '+1 --',  "aaa\naaa\n",   "aaa\n",           0],
['obs-plus45', '+1 --',  "baa\naaa\n",   "baa\n",           0],
# Skip over fields and characters
['50', '-f 1 -s 1',"a aaa\nb ab\n",      "a aaa\nb ab\n",       0],
['51', '-f 1 -s 1',"a aaa\nb aaa\n",     "a aaa\n",             0],
['52', '-s 1 -f 1',"a aaa\nb ab\n",      "a aaa\nb ab\n",       0],
['53', '-s 1 -f 1',"a aaa\nb aaa\n",     "a aaa\n",             0],
# Fixed in 2.0.15
['54', '-s 4',     "abc\nabcd\n",        "abc\n",               0],
# Supported in 2.0.15
['55', '-s 0',     "abc\nabcd\n",        "abc\nabcd\n",         0],
['56', '-s 0',     "abc\n",              "abc\n",               0],
['57', '-w 0',     "abc\nabcd\n",        "abc\n",               0],
# Only account for a number of characters
['60', '-w 1',"a a\nb a\n",      "a a\nb a\n",         0],
['61', '-w 3',"a a\nb a\n",      "a a\nb a\n",         0],
['62', '-w 1 -f 1',"a a a\nb a c\n",  "a a a\n",       0],
['63', '-f 1 -w 1',"a a a\nb a c\n",  "a a a\n",       0],
# The blank after field one is checked too
['64', '-f 1 -w 4',"a a a\nb a c\n",  "a a a\nb a c\n",         0],
['65', '-f 1 -w 3',"a a a\nb a c\n",  "a a a\n",                0],
# Make sure we don't break if the file contains \0
['90', '',       "a\0a\na\n",  "a\0a\na\n",                     0],
# Check fields seperated by tabs and by spaces
['91', '',       "a\ta\na a\n",  "a\ta\na a\n",                 0],
['92', '-f 1',   "a\ta\na a\n",  "a\ta\na a\n",                 0],
['93', '-f 2',   "a\ta a\na a a\n",  "a\ta a\n",                0],
['94', '-f 1',   "a\ta\na\ta\n",  "a\ta\n",                     0],
# Check the count option; add tests for other options too
['101', '-c',    "a\nb\n",          "      1 a\n      1 b\n", 0],
['102', '-c',    "a\na\n",          "      2 a\n",             0],
# Check the local -D (--all-repeated) option
['110', '-D',    "a\na\n",          "a\na\n",                   0],
['111', '-D -w1',"a a\na b\n",      "a a\na b\n",               0],
['112', '-D -c', "a a\na b\n",      "",                         1],
['113', '--all-repeated=separate',"a\na\n",          "a\na\n",           0],
['114', '--all-repeated=separate',"a\na\nb\nc\nc\n", "a\na\n\nc\nc\n",   0],
['115', '--all-repeated=separate',"a\na\nb\nb\nc\n", "a\na\n\nb\nb\n",   0],
['116', '--all-repeated=prepend', "a\na\n",          "\na\na\n",         0],
['117', '--all-repeated=prepend', "a\na\nb\nc\nc\n", "\na\na\n\nc\nc\n", 0],
['118', '--all-repeated=prepend', "a\nb\n",          "",                 0],
['119', '--all-repeated=badoption', "a\n",           "",                 1],
# Check that -d and -u suppress all output, as POSIX requires.
['120', '-d -u', "a\na\n\b",        "",                         0],
['121', '-d -u -w340282366920938463463374607431768211456',
		 "a\na\n\b",        "",                         0],
# Check that --zero-terminated is synonymous with -z.
['122', '--zero-terminated',  "a\na\nb",         "a\na\nb\0",       0],
['123', '--zero-terminated',  "a\0a\0b",         "a\0b\0",          0],
);

sub test_vector
{
  my @new;

  my $t;
  foreach $t (@tv)
    {
      my ($test_name, $flags, $in, $exp, $ret) = @$t;
      $Test::input_via{$test_name} = {REDIR => 0, PIPE => 0};

      $test_name =~ /^obs-plus/
	and $Test::env{$test_name} = ['_POSIX2_VERSION=199209'];

      $ret
	and $Test::input_via{$test_name} = {REDIR => 0};

      push @new, $t;

      ###########################################################
      # When possible, create a "-z"-testing variant of each test.

      # skip any test whose input or output already contains a NUL byte
      $in =~ /\0/ || $exp =~ /\0/
	and next;
      # skip any test that uses the -z option
      $flags =~ /z/
	and next;
      # skip the obsolete-syntax tests
      $test_name =~ /^obs-plus/
	and next;

      (my $inz = $in) =~ tr/\n/\0/;
      (my $expz = $exp) =~ tr/\n/\0/;
      my $t2 = ["$test_name-z", "-z $flags", $inz, $expz, $ret];
      push @new, $t2;
    }

  return @new;
}

1;
