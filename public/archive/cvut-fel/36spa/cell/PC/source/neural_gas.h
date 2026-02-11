#ifndef __NEURAL_GAS_H_
#define __NEURAL_GAS_H_



#define LAMBDA_I 10
#define LAMBDA_F 0.01f
#define EPS_I 0.5f
#define EPS_F 0.005f


typedef struct Vertex
{
	double x;
	double y;
	double z;
	double w;
} Vertex;

typedef struct Neuron
{
	double x;
	double y;
	double z;
	double w;
} Neuron;



int neural_gas(Vertex* input, int inputLength, Neuron* output, int outputLength, int iterations);

int neural_gas(Vertex* input, int inputLength, Neuron* output, int outputLength, int iterations, 
			   double lambda_i, double lambda_f, double eps_i, double eps_f);


#endif // ifndef  __NEURAL_GAS_H_
