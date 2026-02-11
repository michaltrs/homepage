#ifndef NEURALGAS_SPU_H_
#define NEURALGAS_SPU_H_

#include "../NeuralGas_Shared.h"

/** Runs neural gas algorithm computation. 
 *
 * \param input NeuralGas_InputData structure.
 * \param inputCache Pointer to array that will be used as cache for input vertices.
 * \param inputCacheSize Input cache size.
 * \paran neuronCache Pointer to array that will be used as cache for neurons.
 * \param neuronCacheSize Neuron cache size.
 */
int computeNeuralGas_PPU(NeuralGas_InputData* input, Vertex* inputCache, int inputCacheSize, Neuron* neuronCache, int neuronCacheSize);

#endif /*NEURALGAS_SPU_H_*/
