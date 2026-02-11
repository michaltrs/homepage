#include <stdio.h>
#include <spu_ext.h>
#include <spu_mfcio.h>

#include "NeuralGas_SPU.h"

#define INPUT_CACHE_SIZE 128
#define NEURON_CACHE_SIZE 128

/** Input data used to initialize NeuralGas_SPU class. */
NeuralGas_InputData input __attribute__ ((aligned (128)));
/** Input cache memory. */
Vertex inputCache[INPUT_CACHE_SIZE] __attribute__ ((aligned (128)));
/** Neuron cache memory. */
Neuron neuronCache[NEURON_CACHE_SIZE] __attribute__ ((aligned (128)));


/** Main entry point of SPU program. */
int main(unsigned long long id, addr64 argp, addr64 envp)
{
	// Load input information that will be used for computation. 	
	mfc_get(&input, argp.ull, sizeof(input), 31, 0, 0);
	mfc_write_tag_mask(1<<31);
	mfc_read_tag_status_all();
	
	#ifdef TRACE
	printf("[SPU] Iterations: %d\n[SPU] EPS_I: %f\n", input.iterations, input.eps_i);
	#endif
	
	// Run algorithm computation.
	return computeNeuralGas_PPU(&input, inputCache, INPUT_CACHE_SIZE, neuronCache, NEURON_CACHE_SIZE);
}
 
