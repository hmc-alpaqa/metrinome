int main(){
    int x;
    int y;

    if(x < y){
        x++;
    }
    else if (2 * y < x + 19){
        y *= 3;
    }
    else if(x * y == 122){
        x = x + y;
    }

    int z = x + y; 

    return 0;
}