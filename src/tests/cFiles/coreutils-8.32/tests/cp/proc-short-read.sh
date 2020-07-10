#!/bin/sh
# exercise cp's short-read failure when operating on >4KB files in /proc

# Copyright (C) 2009-2020 Free Software Foundation, Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

. "${srcdir=.}/tests/init.sh"; path_prepend_ ./src
print_ver_ cp

proc_large=/proc/cpuinfo  # usually > 4KiB

test -r $proc_large || skip_ "your system lacks $proc_large"

# Before coreutils-7.3, cp would copy less than 4KiB of this file.
cp $proc_large 1    || fail=1
cat $proc_large > 2 || fail=1

# adjust varying parts
sed '/MHz/d; /bogomips/d;' 1 > proc.cp || framework_failure_
sed '/MHz/d; /bogomips/d;' 2 > proc.cat || framework_failure_

compare proc.cp proc.cat || fail=1

Exit $fail
