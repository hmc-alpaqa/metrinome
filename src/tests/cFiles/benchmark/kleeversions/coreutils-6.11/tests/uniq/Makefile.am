# Make coreutils tests.					-*-Makefile-*-

# Copyright (C) 1997, 1998, 2000, 2003, 2004, 2006 Free Software
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

##test-files-begin
x = uniq
explicit =
maint_gen = 1.I 1.X 1-z.I 1-z.X 2.I 2.X 2-z.I 2-z.X 3.I 3.X 3-z.I 3-z.X 4.I \
4.X 4-z.I 4-z.X 5.I 5.X 5-z.I 5-z.X 6.I 6.X 6-z.I 6-z.X 7.I 7.X 7-z.I 7-z.X \
2z.I 2z.X 3z.I 3z.X 4z.I 4z.X 5z.I 5z.X 20z.I 20z.X 8.I 8.X 8-z.I 8-z.X 9.I \
9.X 9-z.I 9-z.X 10.I 10.X 10-z.I 10-z.X 11.I 11.X 11-z.I 11-z.X 12.I 12.X \
12-z.I 12-z.X 13.I 13.X 13-z.I 13-z.X 20.I 20.X 20-z.I 20-z.X 21.I 21.X \
21-z.I 21-z.X 22.I 22.X 22-z.I 22-z.X 23.I 23.X 23-z.I 23-z.X obs30.I obs30.X \
obs30-z.I obs30-z.X 31.I 31.X 31-z.I 31-z.X 32.I 32.X 32-z.I 32-z.X 33.I 33.X \
33-z.I 33-z.X 34.I 34.X 34-z.I 34-z.X 35.I 35.X 35-z.I 35-z.X obs-plus40.I \
obs-plus40.X obs-plus41.I obs-plus41.X 42.I 42.X 42-z.I 42-z.X 43.I 43.X \
43-z.I 43-z.X obs-plus44.I obs-plus44.X obs-plus45.I obs-plus45.X 50.I 50.X \
50-z.I 50-z.X 51.I 51.X 51-z.I 51-z.X 52.I 52.X 52-z.I 52-z.X 53.I 53.X \
53-z.I 53-z.X 54.I 54.X 54-z.I 54-z.X 55.I 55.X 55-z.I 55-z.X 56.I 56.X \
56-z.I 56-z.X 57.I 57.X 57-z.I 57-z.X 60.I 60.X 60-z.I 60-z.X 61.I 61.X \
61-z.I 61-z.X 62.I 62.X 62-z.I 62-z.X 63.I 63.X 63-z.I 63-z.X 64.I 64.X \
64-z.I 64-z.X 65.I 65.X 65-z.I 65-z.X 90.I 90.X 91.I 91.X 91-z.I 91-z.X 92.I \
92.X 92-z.I 92-z.X 93.I 93.X 93-z.I 93-z.X 94.I 94.X 94-z.I 94-z.X 101.I \
101.X 101-z.I 101-z.X 102.I 102.X 102-z.I 102-z.X 110.I 110.X 110-z.I 110-z.X \
111.I 111.X 111-z.I 111-z.X 112.I 112.X 112-z.I 112-z.X 113.I 113.X 113-z.I \
113-z.X 114.I 114.X 114-z.I 114-z.X 115.I 115.X 115-z.I 115-z.X 116.I 116.X \
116-z.I 116-z.X 117.I 117.X 117-z.I 117-z.X 118.I 118.X 118-z.I 118-z.X 119.I \
119.X 119-z.I 119-z.X 120.I 120.X 120-z.I 120-z.X 121.I 121.X 121-z.I 121-z.X \
122.I 122.X 123.I 123.X
run_gen = 1.O 1.E 1-z.O 1-z.E 2.O 2.E 2-z.O 2-z.E 3.O 3.E 3-z.O 3-z.E 4.O 4.E \
4-z.O 4-z.E 5.O 5.E 5-z.O 5-z.E 6.O 6.E 6-z.O 6-z.E 7.O 7.E 7-z.O 7-z.E 2z.O \
2z.E 3z.O 3z.E 4z.O 4z.E 5z.O 5z.E 20z.O 20z.E 8.O 8.E 8-z.O 8-z.E 9.O 9.E \
9-z.O 9-z.E 10.O 10.E 10-z.O 10-z.E 11.O 11.E 11-z.O 11-z.E 12.O 12.E 12-z.O \
12-z.E 13.O 13.E 13-z.O 13-z.E 20.O 20.E 20-z.O 20-z.E 21.O 21.E 21-z.O \
21-z.E 22.O 22.E 22-z.O 22-z.E 23.O 23.E 23-z.O 23-z.E obs30.O obs30.E \
obs30-z.O obs30-z.E 31.O 31.E 31-z.O 31-z.E 32.O 32.E 32-z.O 32-z.E 33.O 33.E \
33-z.O 33-z.E 34.O 34.E 34-z.O 34-z.E 35.O 35.E 35-z.O 35-z.E obs-plus40.O \
obs-plus40.E obs-plus41.O obs-plus41.E 42.O 42.E 42-z.O 42-z.E 43.O 43.E \
43-z.O 43-z.E obs-plus44.O obs-plus44.E obs-plus45.O obs-plus45.E 50.O 50.E \
50-z.O 50-z.E 51.O 51.E 51-z.O 51-z.E 52.O 52.E 52-z.O 52-z.E 53.O 53.E \
53-z.O 53-z.E 54.O 54.E 54-z.O 54-z.E 55.O 55.E 55-z.O 55-z.E 56.O 56.E \
56-z.O 56-z.E 57.O 57.E 57-z.O 57-z.E 60.O 60.E 60-z.O 60-z.E 61.O 61.E \
61-z.O 61-z.E 62.O 62.E 62-z.O 62-z.E 63.O 63.E 63-z.O 63-z.E 64.O 64.E \
64-z.O 64-z.E 65.O 65.E 65-z.O 65-z.E 90.O 90.E 91.O 91.E 91-z.O 91-z.E 92.O \
92.E 92-z.O 92-z.E 93.O 93.E 93-z.O 93-z.E 94.O 94.E 94-z.O 94-z.E 101.O \
101.E 101-z.O 101-z.E 102.O 102.E 102-z.O 102-z.E 110.O 110.E 110-z.O 110-z.E \
111.O 111.E 111-z.O 111-z.E 112.O 112.E 112-z.O 112-z.E 113.O 113.E 113-z.O \
113-z.E 114.O 114.E 114-z.O 114-z.E 115.O 115.E 115-z.O 115-z.E 116.O 116.E \
116-z.O 116-z.E 117.O 117.E 117-z.O 117-z.E 118.O 118.E 118-z.O 118-z.E 119.O \
119.E 119-z.O 119-z.E 120.O 120.E 120-z.O 120-z.E 121.O 121.E 121-z.O 121-z.E \
122.O 122.E 123.O 123.E
##test-files-end

EXTRA_DIST = Test.pm $x-tests $(explicit) $(maint_gen)
noinst_SCRIPTS = $x-tests

editpl = sed -e 's,@''PERL''@,$(PERL),g' -e 's,@''srcdir''@,$(srcdir),g'

TESTS = $x-tests

mk_script = $(srcdir)/../mk-script
$(srcdir)/$x-tests: $(mk_script) Test.pm Makefile.am
	test '$x' = test && prog=../../src/$x || prog=$x; \
	$(PERL) -I$(srcdir) -w -- $(mk_script) $(srcdir) $$prog > $@.n
	mv $@.n $@
	chmod 755 $@

MAINTAINERCLEANFILES = $x-tests $(maint_gen)
CLEANFILES = $(run_gen)

check: $(maint_gen)

$(srcdir)/Makefile.am: ../Makefile.am.in Test.pm $(mk_script)
	rm -f $@ $@t
	sed -n '1,/^##test-files-begin/p' $(srcdir)/../Makefile.am.in > $@t
	tool=`echo $(subdir)|sed 's/^tests.//;s/-test//'`; \
	  echo "x = $$tool" >> $@t
	$(PERL) -I$(srcdir) -w -- $(mk_script) $(srcdir) --list >> $@t
	sed -n '/^##test-files-end/,$$p' $(srcdir)/../Makefile.am.in >> $@t
	chmod -w $@t
	mv $@t $@

include $(top_srcdir)/tests/check.mk
