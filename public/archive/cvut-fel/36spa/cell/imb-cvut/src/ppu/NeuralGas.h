#ifndef NEURALGAS_H_
#define NEURALGAS_H_

#include <libspe.h>
#include "../NeuralGas_Shared.h"

/**
 * Runs neural gas algorithm on one SPU.
 * 
 * \param input Neural gas algorithm input data.
 * \return Returns speid_t handle of executed SPU program.
 */ 
speid_t computeNeuralGas_PPU(NeuralGas_InputData* input);


#endif /*NEURALGAS_H_*/
