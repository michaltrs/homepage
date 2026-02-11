using System;
using System.Collections.Generic;
using System.Text;

namespace Kyble_heuristika
{
    class PQ
    {
        private Queue<State>[] queues;

        public PQ(int priority_count)
        {
            queues = new Queue<State>[priority_count];
            for (int i = 0; i < priority_count; i++)
            {
                queues[i] = new Queue<State>();
            }
        }

        public void Enqueue(int priority, State value) {
            queues[priority].Enqueue(value);
        }

        public State Dequeue() {
            for (int i = 0; i < queues.Length; i++)
			{
                if (queues[i].Count != 0)
	            {
		            return queues[i].Dequeue();
                }
			}
            return null;
        }

        public bool Empty()
        {
            for (int i = 0; i < queues.Length; i++)
            {
                if (queues[i].Count != 0)
                {
                    return false;
                }
            }
            return true;
        }
    }
}
