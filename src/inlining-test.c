// Inline function 
static void foo(int x) { 
    ++x;

}  

int main() {
    // inline function call 
    int a = 0;
    foo(a);

    return 0;
}