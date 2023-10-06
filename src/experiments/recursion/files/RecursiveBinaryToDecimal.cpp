#include <string>
int compute(std::string s, int number){
    if(number < 0){
        return 0;
    }
    if (s[number] == '0'){
        return 2*compute(s,number-1);
    }
    return 1+2*compute(s,number-1);
}

