#include <stdio.h>
/* Created a structure here. The name of the structure is
 * StudentData.
 */
struct StudentData {
  char *stu_name;
  int stu_id;
  int stu_age;
};
int main() {
  /* student is the variable of structure StudentData*/
  struct StudentData student;

  /*Assigning the values of each struct member here*/
  student.stu_name = "Steve";
  student.stu_id = 1234;
  student.stu_age = 30;

  /* Displaying the values of struct members */
  printf("Student Name is: %s", student.stu_name);
  printf("\nStudent Id is: %d", student.stu_id);
  printf("\nStudent Age is: %d", student.stu_age);
  return 0;
}