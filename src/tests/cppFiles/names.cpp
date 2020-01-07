#include <iostream>
#include <string>


class Jar {
    
    public:
    
    int nameCount = 5;
    
    const std::string names[5]={"josh", "gabe", "sofia", "lucas", "ishaan"};
    
    std::string pull(int x) {
        const int y = x%5;
        if (y != 1) {   
            return names[y];
        }
        return "sorry gabe";
    }
    
};
    

int main()
{
    Jar j;
    std::cout << j.pull(1) << std::endl;
    return 4;
    
}