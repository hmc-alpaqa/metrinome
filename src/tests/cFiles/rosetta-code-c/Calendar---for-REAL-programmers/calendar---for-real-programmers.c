// /app/code/tests/cFiles/rosetta-code-c/Calendar---for-REAL-programmers/calendar---for-real-programmers.c

// /* UPPER CASE ONLY VERSION OF THE ORIGINAL CALENDAR.C, CHANGES MOSTLY TO AVOID NEEDING #INCLUDES */
// /* ERROR MESSAGES GO TO STDOUT TO SLIGHTLY SIMPLIFY THE I/O HANDLING                             */
// /* WHEN COMPILING THIS, THE COMMAND LINE SHOULD SPECIFY -D OPTIONS FOR THE FOLLOWING WORDS:      */
// /*    STRUCT, VOID, INT, CHAR, CONST, MAIN, IF, ELSE, WHILE, FOR, DO, BREAK, RETURN, PUTCHAR     */
// /* THE VALUE OF EACH MACRO SHOULD BE THE WORD IN LOWER-CASE                                      */

// INT PUTCHAR(INT);

// INT WIDTH = 80, YEAR = 1969;
// INT COLS, LEAD, GAP;

// CONST CHAR *WDAYS[] = { "SU", "MO", "TU", "WE", "TH", "FR", "SA" };
// STRUCT MONTHS {
//     CONST CHAR *NAME;
//     INT DAYS, START_WDAY, AT;
// } MONTHS[12] = {
//     { "JANUARY",    31, 0, 0 },
//     { "FEBRUARY",    28, 0, 0 },
//     { "MARCH",    31, 0, 0 },
//     { "APRIL",    30, 0, 0 },
//     { "MAY",    31, 0, 0 },
//     { "JUNE",    30, 0, 0 },
//     { "JULY",    31, 0, 0 },
//     { "AUGUST",    31, 0, 0 },
//     { "SEPTEMBER",    30, 0, 0 },
//     { "OCTOBER",    31, 0, 0 },
//     { "NOVEMBER",    30, 0, 0 },
//     { "DECEMBER",    31, 0, 0 }
// };

// VOID SPACE(INT N) { WHILE (N-- > 0) PUTCHAR(' '); }
// VOID PRINT(CONST CHAR * S){ WHILE (*S != '\0') { PUTCHAR(*S++); } }
// INT  STRLEN(CONST CHAR * S)
// {
//    INT L = 0;
//    WHILE (*S++ != '\0') { L ++; };
// RETURN L;
// }
// INT ATOI(CONST CHAR * S)
// {
//     INT I = 0;
//     INT SIGN = 1;
//     CHAR C;
//     WHILE ((C = *S++) != '\0') {
//         IF (C == '-')
//             SIGN *= -1;
//         ELSE {
//             I *= 10;
//             I += (C - '0');
//         }
//     }
// RETURN I * SIGN;
// }

// VOID INIT_MONTHS(VOID)
// {
//     INT I;

//     IF ((!(YEAR % 4) && (YEAR % 100)) || !(YEAR % 400))
//         MONTHS[1].DAYS = 29;

//     YEAR--;
//     MONTHS[0].START_WDAY
//         = (YEAR * 365 + YEAR/4 - YEAR/100 + YEAR/400 + 1) % 7;

//     FOR (I = 1; I < 12; I++)
//         MONTHS[I].START_WDAY =
//             (MONTHS[I-1].START_WDAY + MONTHS[I-1].DAYS) % 7;

//     COLS = (WIDTH + 2) / 22;
//     WHILE (12 % COLS) COLS--;
//     GAP = COLS - 1 ? (WIDTH - 20 * COLS) / (COLS - 1) : 0;
//     IF (GAP > 4) GAP = 4;
//     LEAD = (WIDTH - (20 + GAP) * COLS + GAP + 1) / 2;
//         YEAR++;
// }

// VOID PRINT_ROW(INT ROW)
// {
//     INT C, I, FROM = ROW * COLS, TO = FROM + COLS;
//     SPACE(LEAD);
//     FOR (C = FROM; C < TO; C++) {
//         I = STRLEN(MONTHS[C].NAME);
//         SPACE((20 - I)/2);
//         PRINT(MONTHS[C].NAME);
//         SPACE(20 - I - (20 - I)/2 + ((C == TO - 1) ? 0 : GAP));
//     }
//     PUTCHAR('\012');

//     SPACE(LEAD);
//     FOR (C = FROM; C < TO; C++) {
//         FOR (I = 0; I < 7; I++) {
//             PRINT(WDAYS[I]);
//             PRINT(I == 6 ? "" : " ");
//         }
//         IF (C < TO - 1) SPACE(GAP);
//         ELSE PUTCHAR('\012');
//     }

//     WHILE (1) {
//         FOR (C = FROM; C < TO; C++)
//             IF (MONTHS[C].AT < MONTHS[C].DAYS) BREAK;
//         IF (C == TO) BREAK;

//         SPACE(LEAD);
//         FOR (C = FROM; C < TO; C++) {
//             FOR (I = 0; I < MONTHS[C].START_WDAY; I++) SPACE(3);
//             WHILE(I++ < 7 && MONTHS[C].AT < MONTHS[C].DAYS) {
//                 INT MM = ++MONTHS[C].AT;
//                 PUTCHAR((MM < 10) ? ' ' : '0' + (MM /10));
//                 PUTCHAR('0' + (MM %10));
//                 IF (I < 7 || C < TO - 1) PUTCHAR(' ');
//             }
//             WHILE (I++ <= 7 && C < TO - 1) SPACE(3);
//             IF (C < TO - 1) SPACE(GAP - 1);
//             MONTHS[C].START_WDAY = 0;
//         }
//         PUTCHAR('\012');
//     }
//     PUTCHAR('\012');
// }

// VOID PRINT_YEAR(VOID)
// {
//     INT Y = YEAR;
//     INT ROW;
//     CHAR BUF[32];
//     CHAR * B = &(BUF[31]);
//     *B-- = '\0';
//     DO {
//         *B-- = '0' + (Y % 10);
//         Y /= 10;
//     } WHILE (Y > 0);
//     B++;
//     SPACE((WIDTH - STRLEN(B)) / 2);
//     PRINT(B);PUTCHAR('\012');PUTCHAR('\012');
//     FOR (ROW = 0; ROW * COLS < 12; ROW++)
//         PRINT_ROW(ROW);
// }

// INT MAIN(INT C, CHAR **V)
// {
//     INT I, YEAR_SET = 0, RESULT = 0;
//     FOR (I = 1; I < C && RESULT == 0; I++) {
//         IF (V[I][0] == '-' && V[I][1] == 'W' && V[I][2] == '\0') {
//             IF (++I == C || (WIDTH = ATOI(V[I])) < 20)
//                 RESULT = 1;
//         } ELSE IF (!YEAR_SET) {
//             YEAR = ATOI(V[I]);
//             IF (YEAR <= 0)
//                 YEAR = 1969;
//             YEAR_SET = 1;
//         } ELSE
//             RESULT = 1;
//     }

//     IF (RESULT == 0) {
//         INIT_MONTHS();
//         PRINT_YEAR();
//     } ELSE {
//         PRINT("BAD ARGS\012USAGE: ");
//         PRINT(V[0]);
//         PRINT(" YEAR [-W WIDTH (>= 20)]\012");
//     }
// RETURN RESULT;
// }

#include <stdio.h>

// int putchar(int);

int width = 80, year = 1969;
int cols, lead, gap;

const char *wdays[] = { "su", "mo", "tu", "we", "th", "fr", "sa" };

struct months {
    const char *name;
    int days, start_wday, at;
} months[12] = {
    { "january", 31, 0, 0 },
    { "february", 28, 0, 0 },
    { "march", 31, 0, 0 },
    { "april", 30, 0, 0 },
    { "may", 31, 0, 0 },
    { "june", 30, 0, 0 },
    { "july", 31, 0, 0 },
    { "august", 31, 0, 0 },
    { "september", 30, 0, 0 },
    { "october", 31, 0, 0 },
    { "november", 30, 0, 0 },
    { "december", 31, 0, 0 }
};

void space(int n) { while (n-- > 0) putchar(' '); }

void print(const char *s) { while (*s != '\0') { putchar(*s++); } }

int strlen(const char *s) {
    int l = 0;
    while (*s++ != '\0') { l++; }
    return l;
}

int atoi(const char *s) {
    int i = 0;
    int sign = 1;
    char c;
    while ((c = *s++) != '\0') {
        if (c == '-')
            sign *= -1;
        else {
            i *= 10;
            i += (c - '0');
        }
    }
    return i * sign;
}

void init_months(void) {
    int i;

    if ((!(year % 4) && (year % 100)) || !(year % 400))
        months[1].days = 29;

    year--;
    months[0].start_wday = (year * 365 + year / 4 - year / 100 + year / 400 + 1) % 7;

    for (i = 1; i < 12; i++)
        months[i].start_wday = (months[i - 1].start_wday + months[i - 1].days) % 7;

    cols = (width + 2) / 22;
    while (12 % cols) cols--;
    gap = cols - 1 ? (width - 20 * cols) / (cols - 1) : 0;
    if (gap > 4) gap = 4;
    lead = (width - (20 + gap) * cols + gap + 1) / 2;
    year++;
}

void print_row(int row) {
    int c, i, from = row * cols, to = from + cols;
    space(lead);
    for (c = from; c < to; c++) {
        i = strlen(months[c].name);
        space((20 - i) / 2);
        print(months[c].name);
        space(20 - i - (20 - i) / 2 + ((c == to - 1) ? 0 : gap));
    }
    putchar('\012');

    space(lead);
    for (c = from; c < to; c++) {
        for (i = 0; i < 7; i++) {
            print(wdays[i]);
            print(i == 6 ? "" : " ");
        }
        if (c < to - 1) space(gap);
        else putchar('\012');
    }

    while (1) {
        for (c = from; c < to; c++)
            if (months[c].at < months[c].days) break;
        if (c == to) break;

        space(lead);
        for (c = from; c < to; c++) {
            for (i = 0; i < months[c].start_wday; i++) space(3);
            while (i++ < 7 && months[c].at < months[c].days) {
                int mm = ++months[c].at;
                putchar((mm < 10) ? ' ' : '0' + (mm / 10));
                putchar('0' + (mm % 10));
                if (i < 7 || c < to - 1) putchar(' ');
            }
            while (i++ <= 7 && c < to - 1) space(3);
            if (c < to - 1) space(gap - 1);
            months[c].start_wday = 0;
        }
        putchar('\012');
    }
    putchar('\012');
}

void print_year(void) {
    int y = year;
    int row;
    char buf[32];
    char *b = &(buf[31]);
    *b-- = '\0';
    do {
        *b-- = '0' + (y % 10);
        y /= 10;
    } while (y > 0);
    b++;
    space((width - strlen(b)) / 2);
    print(b);
    putchar('\012');
    putchar('\012');
    for (row = 0; row * cols < 12; row++)
        print_row(row);
}

int main(int c, char **v) {
    int i, year_set = 0, result = 0;
    for (i = 1; i < c && result == 0; i++) {
        if (v[i][0] == '-' && v[i][1] == 'w' && v[i][2] == '\0') {
            if (++i == c || (width = atoi(v[i])) < 20)
                result = 1;
        } else if (!year_set) {
            year = atoi(v[i]);
            if (year <= 0)
                year = 1969;
            year_set = 1;
        } else
            result = 1;
    }

    if (result == 0) {
        init_months();
        print_year();
    } else {
        print("bad args\012usage: ");
        print(v[0]);
        print(" year [-w width (>= 20)]\012");
    }
    return result;
}