#include <float.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "neural_gas.h"


typedef struct NeuronDistance
{
	Neuron* neuron;
	double distance;
}
NeuronDistance;



double compute_distance(Neuron* neuron, Vertex* vertex)
{
	return (neuron->x - vertex->x) * (neuron->x - vertex->x) +
		(neuron->y - vertex->y) * (neuron->y - vertex->y) +
		(neuron->z - vertex->z) * (neuron->z - vertex->z) +
		(neuron->w - vertex->w) * (neuron->w - vertex->w);
}


int compare_neurons_distances(const void *arg1, const void *arg2)
{
	if (((NeuronDistance*)arg1)->distance < ((NeuronDistance*)arg2)->distance)
	{
		return -1;
	}
	else if (((NeuronDistance*)arg1)->distance > ((NeuronDistance*)arg2)->distance)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}



int neural_gas(Vertex* input, int inputLength, Neuron* output, int outputLength, int iterations)
{
	return neural_gas(input, inputLength, output, outputLength, iterations, LAMBDA_I, LAMBDA_F, EPS_I, EPS_F);
}



int neural_gas(Vertex* input, int inputLength, Neuron* output, int outputLength, int iterations, 
			   double lambda_i, double lambda_f, double eps_i, double eps_f)
{
	
	if (!input || inputLength < 1 || !output || outputLength < 1 || !iterations || !lambda_i || !eps_i)
	{
		return 1;
	}
	
	// check minimal and maximal values of input data
	double minX = DBL_MAX, maxX = DBL_MIN, 
		minY = DBL_MAX, maxY = DBL_MIN, 
		minZ = DBL_MAX, maxZ = DBL_MIN, 
		minW = DBL_MAX, maxW = DBL_MIN;

	for(int i = 0; i < inputLength; i++)
	{
		minX = input[i].x < minX ? input[i].x : minX;	maxX = input[i].x > maxX ? input[i].x : maxX;
		minY = input[i].y < minY ? input[i].y : minY;	maxY = input[i].y > maxY ? input[i].y : maxY;
		minZ = input[i].z < minZ ? input[i].z : minZ;	maxZ = input[i].z > maxZ ? input[i].z : maxZ;
		minW = input[i].w < minW ? input[i].w : minW;	maxW = input[i].w > maxW ? input[i].w : maxW;
	}

	// Neurons distances.
	NeuronDistance* neuronsDistances = new NeuronDistance[outputLength];

	// generate initial positions of neurons
	srand((unsigned int)time(NULL));
	for(int i = 0; i < outputLength; i++)
	{
		output[i].x = ((double)rand() / RAND_MAX) * (maxX - minX) + minX;
		output[i].y = ((double)rand() / RAND_MAX) * (maxY - minY) + minY;
		output[i].z = ((double)rand() / RAND_MAX) * (maxZ - minZ) + minZ;
		output[i].w = ((double)rand() / RAND_MAX) * (maxW - minW) + minW;
		neuronsDistances[i].neuron = &(output[i]);
		neuronsDistances[i].distance = DBL_MAX;
	}


	for(int iteration = 0; iteration < iterations; iteration++)
	{
		for(int inputIndex = 0; inputIndex < inputLength; inputIndex++)
		{
			Vertex* actualInput = &(input[inputIndex]);

			// compute distance between actual input and each neuron
			for(int neuronIndex = 0; neuronIndex < outputLength; neuronIndex++)
			{
				neuronsDistances[neuronIndex].distance = compute_distance(neuronsDistances[neuronIndex].neuron, 
					actualInput);
			}

			// sort neurons by distance from actual distance
			qsort(neuronsDistances, outputLength, sizeof(NeuronDistance), compare_neurons_distances);
			
			// move each neuron
			double lambda_t = LAMBDA_I * pow(lambda_f / lambda_i, iteration / iterations);
			double eps_t = EPS_I * pow(eps_f / eps_i, iteration / iterations);
			for(int neuronIndex = 0; neuronIndex < outputLength; neuronIndex++)
			{
				Neuron* actualNeuron = neuronsDistances[neuronIndex].neuron;

				double h_lambda_k = exp(-neuronIndex / lambda_t);

				double delta_weight = eps_t * h_lambda_k * (actualNeuron->x - actualInput->x);
				neuronsDistances[neuronIndex].neuron->x -= delta_weight;

				delta_weight = eps_t * h_lambda_k * (actualNeuron->y - actualInput->y);
				neuronsDistances[neuronIndex].neuron->y -= delta_weight;

				delta_weight = eps_t * h_lambda_k * (actualNeuron->z - actualInput->z);
				neuronsDistances[neuronIndex].neuron->z -= delta_weight;

				delta_weight = eps_t * h_lambda_k * (actualNeuron->w - actualInput->w);
				neuronsDistances[neuronIndex].neuron->w -= delta_weight;
			}
		}
	}


	delete neuronsDistances;

	return 0;
}

