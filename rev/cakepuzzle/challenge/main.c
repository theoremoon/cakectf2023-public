#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int M[4][4] = {{1146640091,1277362948,2245791,1729795767,},{1817593079,2146722439,1860814889,1557802610,},{0,1770948809,870734415,1355570260,},{323584794,1405652852,629508793,1928951512,},};

int q() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (M[i][j] >= M[i][j+1]) {
                return 1;
            }
            if (M[i][j] >= M[i+1][j]) {
                return 1;
            }
        }
    }
    return 0;
}

void s(int *y, int *x) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (M[i][j] == 0) {
                *y = i;
                *x = j;
            }
        }
    }
}

void f(int *a, int *b) {
    *a ^= *b;
    *b ^= *a;
    *a ^= *b;
}

void e(char op) {
    int y, x;
    s(&y, &x);
    switch (op) {
        case 'U':
            if (y != 0) {
                f(&M[y][x], &M[y-1][x]);
            }
            break;
        case 'D':
            if (y != 3) {
                f(&M[y][x], &M[y+1][x]);
            }
            break;
        case 'L':
            if (x != 0) {
                f(&M[y][x], &M[y][x-1]);
            }
            break;
        case 'R':
            if (x != 3) {
                f(&M[y][x], &M[y][x+1]);
            }
            break;
    }
}

void win() {
    char buf[4096];
    FILE *fp = fopen("/flag.txt", "r");
    if (fp == NULL) {
        perror("fopen");
        exit(1);
    }
    fread(buf, 4096, 1, fp);

    printf("%s\n", buf);
    exit(0);
}

int main() {
alarm(1000);
    for(;;) {
        if (q() == 0) {
            win();
        }

        char buf[100];
        printf("> ");
        fflush(stdout);
        if (scanf("%s", buf) == -1) {
            exit(0);
        }
        e(buf[0]);
    }
}
