__attribute__((always_inline)) inline int foo(int a, int b, int c){
    while (a < 10) {
        while (b < 10) {
            ++c;
        }
    }
    return a+b;
}

int main(){
    int a;
    int b;
    int c;
    int d;

    d = foo(a, b,c);

    return 0;
}
 