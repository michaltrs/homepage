#ifndef NEURALGAS_SHARED_H_
#define NEURALGAS_SHARED_H_

/** 64-bit address. */ 
typedef union
{
  unsigned long long ull;
  unsigned int ui[2];
  void *p;
} addr64;


/** 4-dimensional vertex. */ 
typedef union
{
	vector float v;
	float f[4];
	struct
	{
		float x;
		float y;
		float z;
		float w;
	} s;
} Vertex;


/** Neuron that contains position (Vertex structure) and distance (working variable). */ 
typedef struct
{
  /** Neuron position. */
	Vertex position;
	/** Neuron distance from acctualy processing input vertex. */
	float distance;
} Neuron;


/** Input data for neural gas algorithm. */ 
typedef struct
{
  /** Input data address. */
	addr64 inputs;
	/** Inputs count. */
	int inputsCount;
	/** Neurons address. */
	addr64 neurons;
	/** Neurouns count. */
	int neuronsCount;
	/** Number of iteration of algorithm. */
	int iterations;
	/** LambdaF parameter of algorithm. */
	float lambda_f;
	/** LambdaI parameter of algorithm. */
	float lambda_i;
	/** EpsF parameter of algorithm. */
	float eps_f;
	/** EpsI parameter of algorithm. */
	float eps_i;
} NeuralGas_InputData;


#endif /*NEURALGAS_SHARED_H_*/ 
