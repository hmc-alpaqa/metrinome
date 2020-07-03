// another inline function
void foo2(int x) 
{ 
    ++x;
} 
 
// Inline function 
void foo(int x) 
{ 
    while (x < 23) {
        foo2(x);
        ++x;
    }

}  

int main() {
    // inline function call 
    int a = 0;
    foo(a);

    return 0;
}