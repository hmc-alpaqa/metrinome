#include "32_newtons_method.c"

int main(){
    int itr, maxmitr;
    float abs_h;
    float h, x0, x1, allerr;
    
    x0 = 1;
    allerr = 0.00001;
    maxmitr = 10000;

    float rt = newton_root(x0, allerr, maxmitr);
    return 0;
}
