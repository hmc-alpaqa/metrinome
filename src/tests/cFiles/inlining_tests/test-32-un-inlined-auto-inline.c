#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MIN_ELEMENT 1
#define MAX_ELEMENT 1000000
__attribute__((always_inline)) inline int sum(int count, ...) {
  int sum = 0;

  // define a pointer to the variable list
  va_list ptr;
  // start the pointer to the list
  va_start(ptr, count);
  // access the argument pointed to in the list and increment position
  for (int i = 0; i < count; i++) {
    sum += va_arg(ptr, int);
  }
  va_end(ptr);
  return sum;
}

__attribute__((always_inline)) inline int min(int count, ...) {
  va_list ptr;
  va_start(ptr, count);

  int min = va_arg(ptr, int);
  int tmp;
  for (int i = 1; i < count; i++) {
    if ((tmp = va_arg(ptr, int)) < min) {
      min = tmp;
    }
  }
  va_end(ptr);
  return min;
}

__attribute__((always_inline)) inline int max(int count, ...) {
  va_list ptr;
  va_start(ptr, count);

  int max = va_arg(ptr, int);
  int tmp;
  for (int i = 1; i < count; i++) {
    if ((tmp = va_arg(ptr, int)) > max) {
      max = tmp;
    }
  }
  va_end(ptr);
  return max;
}

__attribute__((always_inline)) inline int test_implementations_by_sending_three_elements() {
  srand(time(NULL));

  int elements[3];

  elements[0] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[1] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[2] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;

  fprintf(stderr, "Sending following three elements:\n");
  for (int i = 0; i < 3; i++) {
    fprintf(stderr, "%d\n", elements[i]);
  }

  int elements_sum = sum(3, elements[0], elements[1], elements[2]);
  int minimum_element = min(3, elements[0], elements[1], elements[2]);
  int maximum_element = max(3, elements[0], elements[1], elements[2]);

  fprintf(stderr, "Your output is:\n");
  fprintf(stderr, "Elements sum is %d\n", elements_sum);
  fprintf(stderr, "Minimum element is %d\n", minimum_element);
  fprintf(stderr, "Maximum element is %d\n\n", maximum_element);

  int expected_elements_sum = 0;
  for (int i = 0; i < 3; i++) {
    if (elements[i] < minimum_element) {
      return 0;
    }

    if (elements[i] > maximum_element) {
      return 0;
    }

    expected_elements_sum += elements[i];
  }

  return elements_sum == expected_elements_sum;
}

__attribute__((always_inline)) inline int test_implementations_by_sending_five_elements() {
  srand(time(NULL));

  int elements[5];

  elements[0] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[1] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[2] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[3] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[4] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;

  fprintf(stderr, "Sending following five elements:\n");
  for (int i = 0; i < 5; i++) {
    fprintf(stderr, "%d\n", elements[i]);
  }

  int elements_sum =
      sum(5, elements[0], elements[1], elements[2], elements[3], elements[4]);
  int minimum_element =
      min(5, elements[0], elements[1], elements[2], elements[3], elements[4]);
  int maximum_element =
      max(5, elements[0], elements[1], elements[2], elements[3], elements[4]);

  fprintf(stderr, "Your output is:\n");
  fprintf(stderr, "Elements sum is %d\n", elements_sum);
  fprintf(stderr, "Minimum element is %d\n", minimum_element);
  fprintf(stderr, "Maximum element is %d\n\n", maximum_element);

  int expected_elements_sum = 0;
  for (int i = 0; i < 5; i++) {
    if (elements[i] < minimum_element) {
      return 0;
    }

    if (elements[i] > maximum_element) {
      return 0;
    }

    expected_elements_sum += elements[i];
  }

  return elements_sum == expected_elements_sum;
}

__attribute__((always_inline)) inline int test_implementations_by_sending_ten_elements() {
  srand(time(NULL));

  int elements[10];

  elements[0] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[1] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[2] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[3] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[4] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[5] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[6] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[7] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[8] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;
  elements[9] = rand() % (MAX_ELEMENT - MIN_ELEMENT + 1) + MIN_ELEMENT;

  fprintf(stderr, "Sending following ten elements:\n");
  for (int i = 0; i < 10; i++) {
    fprintf(stderr, "%d\n", elements[i]);
  }

  int elements_sum =
      sum(10, elements[0], elements[1], elements[2], elements[3], elements[4],
          elements[5], elements[6], elements[7], elements[8], elements[9]);
  int minimum_element =
      min(10, elements[0], elements[1], elements[2], elements[3], elements[4],
          elements[5], elements[6], elements[7], elements[8], elements[9]);
  int maximum_element =
      max(10, elements[0], elements[1], elements[2], elements[3], elements[4],
          elements[5], elements[6], elements[7], elements[8], elements[9]);

  fprintf(stderr, "Your output is:\n");
  fprintf(stderr, "Elements sum is %d\n", elements_sum);
  fprintf(stderr, "Minimum element is %d\n", minimum_element);
  fprintf(stderr, "Maximum element is %d\n\n", maximum_element);

  int expected_elements_sum = 0;
  for (int i = 0; i < 10; i++) {
    if (elements[i] < minimum_element) {
      return 0;
    }

    if (elements[i] > maximum_element) {
      return 0;
    }

    expected_elements_sum += elements[i];
  }

  return elements_sum == expected_elements_sum;
}

int main() {
  int number_of_test_cases;
  scanf("%d", &number_of_test_cases);

  while (number_of_test_cases--) {
    if (test_implementations_by_sending_three_elements()) {
      printf("Correct Answer\n");
    } else {
      printf("Wrong Answer\n");
    }

    if (test_implementations_by_sending_five_elements()) {
      printf("Correct Answer\n");
    } else {
      printf("Wrong Answer\n");
    }

    if (test_implementations_by_sending_ten_elements()) {
      printf("Correct Answer\n");
    } else {
      printf("Wrong Answer\n");
    }
  }

  return 0;
}