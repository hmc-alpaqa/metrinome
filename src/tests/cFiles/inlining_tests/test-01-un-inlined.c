// another inline function
int foo2(int x) 
{ 
    ++x;
    return x;
} 
 
// Inline function 
int foo(int x) 
{ 
    while (x < 23) {
        x = foo2(x);
        ++x;
    }
    return x;

}  


int main() {
    // inline function call 
    int ret = 0;
    foo(ret);

    return 0;
}