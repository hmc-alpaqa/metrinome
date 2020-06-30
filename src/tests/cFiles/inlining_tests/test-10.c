# include <stdio.h> 

int main(){
    int a;
    int b;

    for (int i = 0; i < a; ++i){
        for (int i = 0; i < a; ++i){
            ++a;
        }
        a = a + 2 ;
    }
    b = a - 2;

    return 0;
}