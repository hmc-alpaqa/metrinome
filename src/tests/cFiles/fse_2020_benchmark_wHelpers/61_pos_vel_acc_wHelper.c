#include <stdio.h>

#define MAXSIZE 100

void setVelocity(double pos[], int num_samples, double delta_t, double vel[]);
void setAcceleration(double pos[], int num_samples, double delta_t, double vel[], double acc[]);
void printLoop(double pos[], int num_samples, double delta_t, double vel[], double acc[]);

void motion(double pos[], int num_samples, double delta_t) {

    double vel[MAXSIZE];
    double acc[MAXSIZE];

    setVelocity(pos, num_samples, delta_t, vel);
    setAcceleration(pos, num_samples, delta_t, vel, acc);
    
    printLoop(pos, num_samples, delta_t, vel, acc);

}

void setVelocity(double pos[], int num_samples, double delta_t, double vel[]){
    int i;
    double t;
    for(i = 0, t = 0; i < num_samples - 1; ++i, t += delta_t){
        vel[i] = (pos[i+1] - pos[i]) / delta_t;
    }
}

void setAcceleration(double pos[], int num_samples, double delta_t, double vel[], double acc[]){
    int i;
    double t;
    for(i = 0, t = 0; i < num_samples - 2; ++i, t += delta_t){
        acc[i] = (vel[i+1] - vel[i]) / delta_t;
    }
}

void printLoop(double pos[], int num_samples, double delta_t, double vel[], double acc[]){
    int i;
    double t;
    for(i = 0, t = 0; i < num_samples - 2; ++i, t += delta_t){
        printf("t = %f\tx = %f\tv =%f\ta = %f\n", t, pos[i], vel[i], acc[i]);        
    }
}