#include "NeuralGas.h"
#include <stdio.h>

/**
 * SPU program handle.
 */
extern spe_program_handle_t NeuralGas_SPU;


speid_t computeNeuralGas_PPU(NeuralGas_InputData* input) {
  if (!input || !(input->inputs.p) || !(input->inputsCount) || 
      !(input->neurons.p) || !(input->neuronsCount) || 
      (input->iterations) < 1) {
		#ifdef TRACE
		printf("[PPU] computeNeuralGas_PPU function failed - invalid parameters.\n");
		#endif
		return NULL;
	}
	if (spe_count_physical_spes() < 1) {
		#ifdef TRACE
		printf("[PPU] computeNeuralGas_PPU function failed - no SPU available.\n");
		#endif
		return NULL;
	}
	#ifdef TRACE
	printf("[PPU] Executing SPU program in computeNeuralGas_PPU function.\n");
	#endif
	return spe_create_thread(SPE_DEF_GRP, &NeuralGas_SPU, 
			(unsigned long long *)input, 0, -1, 0);
}
