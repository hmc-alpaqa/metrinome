# Test "tr".

# Copyright (C) 1996, 1997, 2000, 2002, 2004-2007 Free Software
# Foundation, Inc.

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
# test flags  1 or 2 strings   input    expected output    expected return code
#
['1',         q|'abcd' '[]*]'|,   'abcd',   ']]]]',              0],
['2',         q|'abc' '[%*]xyz'|,  'abc',    'xyz',              0],
['3',         q|'' '[.*]'|,        'abc',    'abc',              0],
# Test --truncate-set1 behavior when string1 is longer than string2
['4', '-t ' . q|'abcd' 'xy'|,     'abcde', 'xycde',            0],
# Test bsd behavior (the default) when string1 is longer than string2
['5',         q|'abcd' 'xy'|,     'abcde', 'xyyye',            0],
# Do it the posix way
['6',         q|'abcd' 'x[y*]'|,  'abcde', 'xyyye',            0],
#
['7', '-s ' . q|'a-p' '%[.*]$'|, 'abcdefghijklmnop', '%.$',       0],
['8', '-s ' . q|'a-p' '[.*]$'|, 'abcdefghijklmnop', '.$',         0],
['9', '-s ' . q|'a-p' '%[.*]'|, 'abcdefghijklmnop', '%.',         0],
['a', '-s ' . q|'[a-z]'|,        'aabbcc', 'abc',              0],
['b', '-s ' . q|'[a-c]'|,        'aabbcc', 'abc',              0],
['c', '-s ' . q|'[a-b]'|,        'aabbcc', 'abcc',             0],
['d', '-s ' . q|'[b-c]'|,        'aabbcc', 'aabc',             0],
['e', '-s ' . q|'[\0-\5]'|,
 "\0\0a\1\1b\2\2\2c\3\3\3d\4\4\4\4e\5\5",
 "\0a\1b\2c\3d\4e\5",  0],
# tests of delete
['f', '-d ' . q|'[=[=]'|, '[[[[[[[]]]]]]]]', ']]]]]]]]', 0],
['g', '-d ' . q|'[=]=]'|, '[[[[[[[]]]]]]]]', '[[[[[[[', 0],
['h', '-d ' . q|'[:xdigit:]'|, '0123456789acbdefABCDEF', '', 0],
['i', '-d ' . q|'[:xdigit:]'|, 'w0x1y2z3456789acbdefABCDEFz', 'wxyzz', 0],
['j', '-d ' . q|'[:digit:]'|, '0123456789', '', 0],
['k', '-d ' . q|'[:digit:]'|, 'a0b1c2d3e4f5g6h7i8j9k', 'abcdefghijk', 0],
['l', '-d ' . q|'[:lower:]'|, 'abcdefghijklmnopqrstuvwxyz', '', 0],
['m', '-d ' . q|'[:upper:]'|, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '', 0],
['n', '-d ' . q|'[:lower:][:upper:]'|,
 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', '', 0],
['o', '-d ' . q|'[:alpha:]'|,
 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', '', 0],
['p', '-d ' . q|'[:alnum:]'|,
 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', '', 0],
['q', '-d ' . q|'[:alnum:]'|,
 '.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.', '..', 0],
['r', '-ds ' . q|'[:alnum:]' '.'|,
 '.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.', '.', 0],

# The classic example, with string2 BSD-style
['s', '-cs ' . q|'[:alnum:]' '\n'|,
 'The big black fox jumped over the fence.',
 "The\nbig\nblack\nfox\njumped\nover\nthe\nfence\n", 0],

# The classic example, POSIX-style
['t', '-cs ' . q|'[:alnum:]' '[\n*]'|,
 'The big black fox jumped over the fence.',
 "The\nbig\nblack\nfox\njumped\nover\nthe\nfence\n", 0],
['u', '-ds ' . q|'b' 'a'|,          'aabbaa', 'a',             0],
['v', '-ds ' . q|'[:xdigit:]' 'Z'|,
 'ZZ0123456789acbdefABCDEFZZ', 'Z', 0],

# Try some data with 8th bit set in case something is mistakenly sign-extended.
['w', '-ds ' . q|'\350' '\345'|,
 "\300\301\377\345\345\350\345",
 "\300\301\377\345", 0],
['x', '-s ' . q|'abcdefghijklmn' '[:*016]'|, 'abcdefghijklmnop', ':op', 0],
['y', '-d ' . q|'a-z'|, 'abc $code', ' $', 0],
['z', '-ds ' . q|'a-z' '$.'|, 'a.b.c $$$$code\\', '. $\\', 0],

# Make sure that a-a is accepted.
['range-a-a', q|'a-a' 'z'|,         'abc',    'zbc',               0],
#
['null', q|'a' ''''|,          '',       '',                  1],
['upcase',q|'[:lower:]' '[:upper:]'|,	'abcxyzABCXYZ', 'ABCXYZABCXYZ', 0],
['dncase', q|'[:upper:]' '[:lower:]'|,	'abcxyzABCXYZ', 'abcxyzabcxyz', 0],
#
['rep-cclass',   q|'a[=*2][=c=]' 'xyyz'|,	'a=c', 'xyz', 0],
['rep-1',   q|'[:*3][:digit:]' 'a-m'|,	':1239', 'cefgm', 0],
['rep-2',   q|'a[b*512]c' '1[x*]2'|,	'abc', '1x2', 0],
['rep-3',   q|'a[b*513]c' '1[x*]2'|,	'abc', '1x2', 0],
# Another couple octal repeat count tests.
['o-rep-1',   q|'[b*08]' '[x*]'|,	'', '', 1],
['o-rep-2',   q|'[b*010]cd' '[a*7]BC[x*]'|, 'bcd', 'BCx', 0],

['esc',     q|'a\-z' 'A-Z'|,		'abc-z', 'AbcBC', 0],
['bs-055', q|'a\055b' def|,		"a\055b", 'def', 0],
['bs-at-end', q|'\' x|,		        "\\", 'x', 0],

#
# From Ross
['ross-0a', '-cs ' . q|'[:upper:]' 'X[Y*]'|,	'', '', 1],
['ross-0b', '-cs ' . q|'[:cntrl:]' 'X[Y*]'|,	'', '', 1],
['ross-1a', '-cs ' . q|'[:upper:]' '[X*]'|, 'AMZamz123.-+AMZ', 'AMZXAMZ', 0],
['ross-1b', '-cs ' . q|'[:upper:][:digit:]' '[Z*]'|, '', '', 0],
['ross-2', '-dcs ' . q|'[:lower:]' 'n-rs-z'|, 'amzAMZ123.-+amz', 'amzamz', 0],
['ross-3', '-ds ' . q|'[:xdigit:]' '[:alnum:]'|,
 '.ZABCDEFGzabcdefg.0123456788899.GG', '.ZGzg..G', 0],
['ross-4', '-dcs ' . q|'[:alnum:]' '[:digit:]'|,	'', '', 0],
['ross-5', '-dc ' . q|'[:lower:]'|,		'', '', 0],
['ross-6', '-dc ' . q|'[:upper:]'|,		'', '', 0],

# Ensure that these fail.
# Prior to 2.0.20, each would evoke a failed assertion.
['empty-eq', q|'[==]' x|,		'', '', 1],
['empty-cc', q|'[::]' x|,		'', '', 1],

# Weird repeat counts.
['repeat-bs-9',          q|abc '[b*\9]'|, 'abcd', '[b*d', 0],
['repeat-0',             q|abc '[b*0]'|, 'abcd', 'bbbd', 0],
['repeat-zeros',         q|abc '[b*00000000000000000000]'|, 'abcd', 'bbbd', 0],
['repeat-compl', '-c ' . q|'[a*65536]\n' '[b*]'|, 'abcd', 'abbb', 0],
['repeat-xC',    '-C ' . q|'[a*65536]\n' '[b*]'|, 'abcd', 'abbb', 0],

# From Glenn Fowler.
['fowler-1', q|ah -H|, 'aha', '-H-', 0],

# Up to coreutils-6.9, this would provoke a failed assertion.
['no-abort-1', '-c ' . q|a '[b*256]'|, 'abc', 'abb', 0],

# Up to coreutils-6.9, tr rejected an unmatched [:lower:] or [:upper:] in SET1.
['s1-lower', q|'[:lower:]' '[.*]'|, '#$%123abcABC', '#$%123...ABC', 0],
['s1-upper', q|'[:upper:]' '[.*]'|, '#$%123abcABC', '#$%123abc...', 0],

# Up to coreutils-6.9.91, this would fail with the diagnostic:
# tr: misaligned [:upper:] and/or [:lower:] construct
# with LC_CTYPE=en_US.ISO-8859-1.
['tolower-F',q|'[:upper:]' '[:lower:]'|, 'A', 'a', 0],

# When doing a case-converting translation with something after the
# [:upper:] and [:lower:] elements, ensure that tr honors the following byte.
['upcase-xtra',q|'[:lower:].' '[:upper:]x'|,	'abc.', 'ABCx', 0],
['dncase-xtra',q|'[:upper:].' '[:lower:]x'|,	'ABC.', 'abcx', 0],
);

$Test::env{'tolower-F'} = ['LC_CTYPE=en_US.ISO-8859-1'];

sub test_vector
{
  my $t;
  foreach $t (@tv)
    {
      my ($test_name, $flags, $in, $exp, $ret) = @$t;
      $Test::input_via{$test_name} = {REDIR => 0, PIPE => 0};
    }

  return @tv;
}

1;
