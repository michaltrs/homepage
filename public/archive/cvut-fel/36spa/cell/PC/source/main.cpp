#include <stdio.h>

#include "neural_gas.h"

int main(int argc, char* argv[])
{
	Vertex vertices[1024];
	Neuron neurons[16];

	printf("%d\n", neural_gas(vertices, 1024, neurons, 16, 256));
	//getchar();

	return 0;
}
