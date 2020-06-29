# include <stdio.h> 

int __attribute__((always_inline)) inline static foo1(int a, int b) {
    for (int i = 0; a < i; ++i) {
        if (a < b) {
            return a;
        } else {
            ++a;
        }
    }
}

int main(){
    int a;
    int b;
    int c;

    c = foo1(a, b);

    return 0;
}
 