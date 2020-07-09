int __attribute__((always_inline)) inline foo3(int x){
    if (x > 0) {
        return x + 5;
    } else {
        return x + 3;
    }
}

int __attribute__((always_inline)) inline foo2(int b){
    while (b< 10) {
        ++b;
    }
    return foo3(b);
}

int __attribute__((always_inline)) inline foo(int a, int b){
    if (a < b){
        a++;
    } 
    else if (a < b){
        b++; 
    }
    return foo3(a);
}

int main(){
    int a;
    int b;

    int c = foo(a, b);
    int d = foo2(b);

    return 0;
}
 