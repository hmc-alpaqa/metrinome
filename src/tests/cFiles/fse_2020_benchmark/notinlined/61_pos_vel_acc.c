#include <stdio.h>

#define MAXSIZE 100

void motion(double pos[], int num_samples, double delta_t) {

    double vel[MAXSIZE];
    double acc[MAXSIZE];

    int i;
    double t;

    for(i = 0, t = 0; i < num_samples - 1; ++i, t += delta_t){
        vel[i] = (pos[i+1] - pos[i]) / delta_t;
    }

    for(i = 0, t = 0; i < num_samples - 2; ++i, t += delta_t){
        acc[i] = (vel[i+1] - vel[i]) / delta_t;
    }

    for(i = 0, t = 0; i < num_samples - 2; ++i, t += delta_t){
        printf("t = %f\tx = %f\tv =%f\ta = %f\n", t, pos[i], vel[i], acc[i]);
    }

}
