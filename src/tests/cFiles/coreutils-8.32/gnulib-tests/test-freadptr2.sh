#!/bin/sh

${CHECKER} ./test-freadptr2${EXEEXT} 0 < "$srcdir/test-freadptr2.sh" || exit 1
${CHECKER} ./test-freadptr2${EXEEXT} 5 < "$srcdir/test-freadptr2.sh" || exit 1
exit 0
