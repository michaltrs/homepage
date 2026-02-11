#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <libspe.h>
#include <altivec.h>
#include <vec_types.h>
#include "../NeuralGas_Shared.h"
#include "NeuralGas.h"


#define INPUTS_COUNT 256
#define NEURONS_COUNT 32
#define LAMBDA_I 10
#define LAMBDA_F 0.01f
#define EPS_I 0.5f
#define EPS_F 0.005f

/** Input data. */
NeuralGas_InputData input __attribute__ ((aligned (128)));
/** Input vertices. */
Vertex inputs[INPUTS_COUNT] __attribute__ ((aligned (128)));
/** Output (neurons). */
Neuron neurons[NEURONS_COUNT] __attribute__ ((aligned (128)));


/** Main entry point of PPU program. */
int main(int argc, char **argv)
{
	#ifdef TRACE
	printf("[PPU] Input address: %llx\n", (unsigned long long)&input);
	#endif
	
	// Fill input structure.
	input.inputs.p = inputs; // input vertices
	input.inputsCount = INPUTS_COUNT;		
	input.neurons.p = neurons; // output (neurons)
	input.neuronsCount = NEURONS_COUNT;
	input.iterations = 1;
	input.lambda_i = LAMBDA_I;
	input.lambda_f = LAMBDA_F;
	input.eps_i = EPS_I;
	input.eps_f = EPS_F;
	
	speid_t handle = computeNeuralGas_PPU(&input);

	int status;
	// Wait until computing on SPU ends.
	(void)spe_wait(handle, &status, 0);

	#ifdef TRACE
    printf("\n[PPU] The program has successfully executed.\n");
	#endif

  return 0;
}
 
