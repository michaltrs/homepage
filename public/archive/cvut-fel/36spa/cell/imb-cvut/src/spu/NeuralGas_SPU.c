#include "NeuralGas_SPU.h"
#include <stdio.h>
#include <spu_ext.h>
#include <spu_mfcio.h>
#include <float.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>



/** Internal data structure that is used during algorithm computation. */
typedef struct {
  /** Input data (got from PPU). */
  NeuralGas_InputData* input;
  /** Input data cache. */
	Vertex* inputCache;
	/** Input data cache size. */
	int inputCacheSize;
	/** Neuron cache. */
	Neuron* neuronCache;
	/** Neuron cache size. */
	int neuronCacheSize;
	
	float minX, maxX, minY, maxY, minZ, maxZ, minW, maxW;
	/** Actual iteration index. */
	int actualIteration;
	/** Actual input vertex. */
	Vertex* actualInput;
	/** Actual neuron index. */
	int actualNeuronIndex;
	float lambda_t, eps_t;

} InternalData_SPU;




//Forward declarations.

/** Read all inputs from main memory to cache and for each batch call specified handler function.
 *
 * \param internal Algorithm state information.
 * \param handler Function that is called for each batch of input data.
 */   
void ReadInputs(InternalData_SPU* internal, void (handler(InternalData_SPU*, int)));

/** Read all neurons from main memory to cache and for each batch call specified handler function. After each batch processing writes the batch back to main memory.
 *
 * \param internal Algorithm state information.
 * \overlap Specifies if overlap of one input data will be made. 
 * \param handler Function that is called for each batch of input data.
 */
void ReadAndWriteNeurons(InternalData_SPU* internal, int overlap, void (handler(InternalData_SPU*, int)));

/** Sets minimal and maximal values of inputs that are in cache.
 * 
 * \param internal Algorithm state information.
 * \param Number of inputs in cache to process.
 */  
void FindMinMax(InternalData_SPU* internal, int elements);

/** Performs one iteration for one input vertex, so computes distance of each neuron and move their.
 * 
 * \param internal Algorithm state information.
 * \param Number of inputs in cache to process.
 */
void DoIterationForInputVertex(InternalData_SPU* internal, int elements);

/** Computes distance of each neuron from actual input vertex.
 * 
 * \param internal Algorithm state information.
 * \param Number of neurons in cache to process.
 */
void ComputeDistance(InternalData_SPU* internal, int elements);


/** Sorts all neurons by their distances.
 *
 * \param internal Algorithm state information.
 */  
void SortNeurons(InternalData_SPU* internal);

/** Performs bubble sort on neurons in cache. Neuron distance is used to compare neurons.
 *
 * \param internal Algorithm state information.
 * \param Number of neurons in cache to process.
 */ 
void BubbleSort(InternalData_SPU* internal, int elements);

/** Updates positions of all neurons accoring to their position in sorted set of neurons.
 *
 * \param internal Algorithm state information.
 * \param Number of neurons in cache to process.
 */  
void UpdateNeuronsPositions(InternalData_SPU* internal, int elements);




int computeNeuralGas_PPU(NeuralGas_InputData* input, Vertex* inputCache, int inputCacheSize, Neuron* neuronCache, int neuronCacheSize) {
  
  #ifdef TRACE
	printf("[SPU] computeNeuralGas_PPU function called.\n");
	#endif
  
  if (!input || !inputCache || !inputCacheSize || !neuronCache || !neuronCacheSize || 
      !(input->inputs.p) || !(input->inputsCount) || 
      !(input->neurons.p) || !(input->neuronsCount) || (input->iterations) < 1) {
    #ifdef TRACE
  	printf("[SPU] Invalid parameters.\n");
  	#endif
    return -1;
  }

  #ifdef TRACE
	printf("[SPU] \tIterations: %d\n", input->iterations);
	printf("[SPU] \tInputs: %d\n", input->inputsCount);
	printf("[SPU] \tNeurons: %d\n", input->neuronsCount);
	#endif
	
  InternalData_SPU* internal = (InternalData_SPU*)malloc(sizeof(InternalData_SPU));;
  internal->input = input;
  internal->inputCache = inputCache;
  internal->inputCacheSize = inputCacheSize;
  internal->neuronCache = neuronCache;
  internal->neuronCacheSize = neuronCacheSize;


  //Sets minimal and maximal values of space.
	#ifdef TRACE
	printf("[SPU] Computing of maximal and minimal values.\n");
	#endif
	internal->minX = FLT_MAX;
	internal->maxX = FLT_MIN;
	internal->minY = FLT_MAX;
	internal->maxY = FLT_MIN;
	internal->minZ = FLT_MAX;
	internal->maxZ = FLT_MIN;
	internal->minW = FLT_MAX;
	internal->maxW = FLT_MIN;
	ReadInputs(internal, FindMinMax);


  // Initialize neurons positions.
  #ifdef TRACE
	printf("[SPU] Initializing neurons.\n");
	#endif
  srand((unsigned int)time(NULL));
	int remaining = input->neuronsCount;
	unsigned int offset = 0;
	while(remaining > 0) {
		int batch = remaining > neuronCacheSize ? neuronCacheSize : remaining;
		for(int i = 0; i < batch; i++) {
			neuronCache[i].position.s.x = ((float)rand() / RAND_MAX) *
				(internal->maxX - internal->minX) + internal->minX;
			neuronCache[i].position.s.y = ((float)rand() / RAND_MAX) *
				(internal->maxY - internal->minY) + internal->minY;
			neuronCache[i].position.s.z = ((float)rand() / RAND_MAX) *
				(internal->maxZ - internal->minZ) + internal->minZ;
			neuronCache[i].position.s.w = ((float)rand() / RAND_MAX) *
				(internal->maxW - internal->minW) + internal->minW;			
		}
		
		mfc_put(neuronCache, input->neurons.ui[0] + offset, sizeof(Neuron) * batch, 31, 0, 0);
		//mfc_write_tag_mask(1<<31);
		mfc_read_tag_status_all();
		
		remaining -= batch;
		offset += batch * sizeof(Neuron);
	}


  for(int iteration = 0; iteration < input->iterations; iteration++) {
		#ifdef TRACE
		printf("[SPU] Starting iteration %d/%d\n", iteration, input->iterations);
		#endif
		// Pre-compute some parameters.
		internal->lambda_t = input->lambda_i * 
							pow(input->lambda_f / input->lambda_i, 
							iteration / input->iterations);
		internal->eps_t = input->eps_i * 
						pow(input->eps_f / input->eps_i, 
						iteration / input->iterations);
						
	  // Perform iteration for each input vertex.
		internal->actualIteration = iteration;
	  ReadInputs(internal, DoIterationForInputVertex);
	}


  free(internal);
  return 0;
}








/** Reads input vertices. */ 
void ReadInputs(InternalData_SPU* internal, void (handler(InternalData_SPU*, int))) {
	#ifdef TRACE
	//printf("[SPU] Entering ReadInputs function.\n");
	#endif
	int remaining = internal->input->inputsCount;
	unsigned int offset = 0;
	while(remaining > 0) {
		int transfer = remaining > internal->inputCacheSize ? internal->inputCacheSize : remaining;
		mfc_get(internal->inputCache, internal->input->inputs.ui[0] + offset, sizeof(Vertex) * transfer, 31, 0, 0);
		//mfc_write_tag_mask(1<<31);
		mfc_read_tag_status_all();
		handler(internal, transfer);
		remaining -= transfer;
		offset += transfer * sizeof(Vertex);
	}
}


/**
 * Reads and saves neurons.
 * \param overlap Specifies if batches will be overlapped.
 */
void ReadAndWriteNeurons(InternalData_SPU* internal, int overlap, void (handler(InternalData_SPU*, int))) {
	#ifdef TRACE
	//printf("[SPU] Entering ReadAndWriteNeurons function.\n");
	#endif
	int remaining = internal->input->neuronsCount;
	unsigned int offset = 0;
	while(remaining > 0) {
		int transfer = remaining > internal->neuronCacheSize ? internal->neuronCacheSize : remaining;
		
		mfc_get(internal->neuronCache, internal->input->neurons.ui[0] + offset, sizeof(Neuron) * transfer, 31, 0, 0);
		//mfc_write_tag_mask(1<<31);
		mfc_read_tag_status_all();
		
		handler(internal, transfer);
		
		mfc_put(internal->neuronCache, internal->input->neurons.ui[0] + offset, sizeof(Neuron) * transfer, 31, 0, 0);
		//mfc_write_tag_mask(1<<31);
		mfc_read_tag_status_all();
		
		
		remaining -= transfer;
		if (overlap && remaining > 0) {
			remaining++;
			transfer--;
		}
		offset += transfer * sizeof(Neuron); 
	}
}



void FindMinMax(InternalData_SPU* internal, int elements) {
	#ifdef TRACE
	printf("[SPU] Entering FindMinMax function.\n");
	#endif
	for(int i = 0; i < elements; i++)	{
    Vertex v = (internal->inputCache)[i];
    internal->minX = v.s.x < internal->minX ? v.s.x : internal->minX;
  	internal->maxX = v.s.x > internal->maxX ? v.s.x : internal->maxX;
  	internal->minY = v.s.y < internal->minY ? v.s.y : internal->minY;	
  	internal->maxY = v.s.y > internal->maxY ? v.s.y : internal->maxY;
  	internal->minZ = v.s.z < internal->minZ ? v.s.z : internal->minZ;	
  	internal->maxZ = v.s.z > internal->maxZ ? v.s.z : internal->maxZ;
  	internal->minW = v.s.w < internal->minW ? v.s.w : internal->minW;	
  	internal->maxW = v.s.w > internal->maxW ? v.s.w : internal->maxW;
	}
}

void DoIterationForInputVertex(InternalData_SPU* internal, int elements) {
	#ifdef TRACE
	printf("[SPU] Entering DoIterationForInputVertex function.\n");
	#endif
	for(int i = 0; i < elements; i++)	{
		internal->actualInput = &((internal->inputCache)[i]);
	
  	#ifdef TRACE
  	printf("[SPU] Computing distance of neurons.\n");
  	#endif
  	ReadAndWriteNeurons(internal, 0, ComputeDistance);
  			
  	SortNeurons(internal);
  	
  	#ifdef TRACE
  	printf("[SPU] Updating positions of neurons.\n");
  	#endif
  	internal->actualNeuronIndex = 0;
  	ReadAndWriteNeurons(internal, 0, UpdateNeuronsPositions);
	}
}



void ComputeDistance(InternalData_SPU* internal, int elements) {
	#ifdef TRACE
	printf("[SPU] Entering ComputeDistance function.\n");
	#endif
	for(int i = 0; i < elements; i++)	{
		Neuron* neuron = &(internal->neuronCache[i]);
    Vertex v;
    v.v = spu_sub(neuron->position.v, internal->actualInput->v);
    v.v = spu_mul(v.v, v.v);
    neuron->distance = v.s.x + v.s.y + v.s.z + v.s.w;
	}
}


void UpdateNeuronsPositions(InternalData_SPU* internal, int elements) {
	#ifdef TRACE
	printf("[SPU] Entering UpdateNeuronPositions function.\n");
	#endif
	for(int i = 0; i < elements; i++)	{
		Neuron* neuron =&(internal->neuronCache[i]);
		
		double h_lambda_k = exp(-internal->actualNeuronIndex / internal->lambda_t);

  	double delta_weight = internal->eps_t * h_lambda_k * 
  							(neuron->position.s.x - internal->actualInput->s.x);
  	neuron->position.s.x -= delta_weight;
  
  	delta_weight = internal->eps_t * h_lambda_k *
  	 				(neuron->position.s.y - internal->actualInput->s.y);
  	neuron->position.s.y -= delta_weight;
  
  	delta_weight = internal->eps_t * h_lambda_k * 
  					(neuron->position.s.z - internal->actualInput->s.z);
  	neuron->position.s.z -= delta_weight;
  
  	delta_weight = internal->eps_t * h_lambda_k * 
  					(neuron->position.s.w - internal->actualInput->s.w);
  	neuron->position.s.w -= delta_weight;
  				
  	internal->actualNeuronIndex++;
	}
}


void SortNeurons(InternalData_SPU* internal) {
	#ifdef TRACE
	printf("[SPU] Entering SortNeurons function.\n");
	#endif
	for(int startIndex = 0; startIndex < internal->input->neuronsCount -1; startIndex++)
	{
		ReadAndWriteNeurons(internal, 1, BubbleSort);
	}
}



void BubbleSort(InternalData_SPU* internal, int elements) {
	#ifdef TRACE
	printf("[SPU] Entering BubbleSort function.\n");
	#endif
	for(int i = 1; i < elements; i++)	{
		if (internal->neuronCache[i].distance < internal->neuronCache[i-1].distance) {
			Neuron n = internal->neuronCache[i];
			internal->neuronCache[i] = internal->neuronCache[i-1];
			internal->neuronCache[i-1] = n;
		}
	}
}
