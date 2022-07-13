#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <stdbool.h>

#define N_COLS 15
#define N_ROWS 15

// Probability granularity 0.0, 0.1, ... 1.0
#define N_STEPS 11

// Simulation tries
#define N_TRIES 100

typedef unsigned char Cell;
enum { EMPTY_CELL   = ' ',
       FILLED_CELL  = '#',
       VISITED_CELL = '.' };
typedef Cell Grid[N_ROWS][N_COLS];

void initialize(Grid grid, const double probability) {
    for (size_t r = 0; r < N_ROWS; r++)
        for (size_t c = 0; c < N_COLS; c++) {
            const double rnd = rand() / (double)RAND_MAX;
            grid[r][c] = (rnd < probability) ? EMPTY_CELL : FILLED_CELL;
        }
}

void show(Grid grid) {
    char line[N_COLS + 3];
    memset(&line[0], '-', N_COLS + 2);
    line[0] = '+';
    line[N_COLS + 1] = '+';
    line[N_COLS + 2] = '\0';

    printf("%s\n", line);
    for (size_t r = 0; r < N_ROWS; r++) {
        putchar('|');
        for (size_t c = 0; c < N_COLS; c++)
            putchar(grid[r][c]);
        puts("|");
    }
    printf("%s\n", line);
}

bool walk(Grid grid, const size_t r, const size_t c) {
    const size_t bottom = N_ROWS - 1;
    grid[r][c] = VISITED_CELL;

    if (r < bottom && grid[r + 1][c] == EMPTY_CELL) { // Down.
        if (walk(grid, r + 1, c))
            return true;
    } else if (r == bottom)
        return true;

    if (c && grid[r][c - 1] == EMPTY_CELL) // Left.
        if (walk(grid, r, c - 1))
            return true;

    if (c < N_COLS - 1 && grid[r][c + 1] == EMPTY_CELL) // Right.
        if (walk(grid, r, c + 1))
            return true;

    if (r && grid[r - 1][c] == EMPTY_CELL) // Up.
        if (walk(grid, r - 1, c))
            return true;

    return false;
}

bool percolate(Grid grid) {
    const size_t startR = 0;
    for (size_t c = 0; c < N_COLS; c++)
        if (grid[startR][c] == EMPTY_CELL)
            if (walk(grid, startR, c))
                return true;
    return false;
}

typedef struct {
    double prob;
    size_t count;
} Counter;
