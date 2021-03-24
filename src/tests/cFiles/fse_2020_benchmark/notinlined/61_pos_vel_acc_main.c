#include<stdio.h>
#include "61_pos_vel_acc.c"

#define NUM_SAMPLES 10

int main(){
	double pos[NUM_SAMPLES] = {0.1, 0.2, 0.4, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1};
	motion(pos, NUM_SAMPLES, 0.5);
}
