#include <iostream>            

using namespace std;

// Example C++ file used for cppToDot.py 
class Cat                      
{
  public:                      
    Cat(int initialAge);       
    Cat(const Cat& copy_from); 
    Cat& operator=(const Cat& copy_from); 
    ~Cat();                    

    int GetAge() const;        
    void SetAge(int age);      
    void Meow();
 private:                      
    int itsAge;                
    char * string;
};

Cat::Cat(int initialAge)
{
  itsAge = initialAge;
  string = new char[10]();
}

Cat::Cat(const Cat& copy_from) {
   itsAge = copy_from.itsAge;
   string = new char[10]();
   std::copy(copy_from.string+0, copy_from.string+10, string);
}

Cat& Cat::operator=(const Cat& copy_from) {
   itsAge = copy_from.itsAge;
   std::copy(copy_from.string+0, copy_from.string+10, string);
}

Cat::~Cat()
{
    delete[] string;
}

int Cat::GetAge() const
{
   return itsAge;
}

 void Cat::SetAge(int age)
{
   itsAge = age;
}

void Cat::Meow()
{
   cout << "Meow.\n";
}

int main()
{
  int Age;
  cout<<"How old is Frisky? ";
  cin>>Age;
  Cat Frisky(Age);
  Frisky.Meow();
  cout << "Frisky is a cat who is " ;
  cout << Frisky.GetAge() << " years old.\n";
  Frisky.Meow();
  Age++;
  Frisky.SetAge(Age);
  cout << "Now Frisky is " ;
  cout << Frisky.GetAge() << " years old.\n";
  return 0;
}