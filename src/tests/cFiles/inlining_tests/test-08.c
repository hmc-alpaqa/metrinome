# include <stdio.h> 

int __attribute__((always_inline)) inline static foo1(int a, int b) {

}

int main(){
    int a;
    int b;
    int c;

    for (int i = 0; a < i; ++i) {
        if (a < b) {
            c = a;
            break;
        } else {
            ++a;
        }
    }

    return 0;
}
 