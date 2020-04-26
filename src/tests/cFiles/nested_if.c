int nested_if_func(int x) {
    if(x > 50) {
        if (x==64) {
            return x + 1;
        } else {
            return x;
        }
    }
    else {
        if(x == 23) {
            return x - 1;
        } else {
            return x;
        }
    }
}