using System;
using System.Collections.Generic;
using System.Text;

namespace Kyble_heuristika
{
    class Heuristic
    {
        protected PQ OPEN;
        protected Dictionary<int, State> STATES = new Dictionary<int, State>();

        private int[] final_state;
        private int[] capacity;
        private int bucketsCount;
                
        protected State bestSolution = null, dqs = null;
        private int vistited_states = 0;


        public Heuristic(Input i)
        {
            this.final_state = i.final_state;
            this.capacity = i.capacity;
            bucketsCount = capacity.Length;
            State s = new State(i.init_state);

            // compute max priority
            int p = 0;
            for (int j = 0; j < bucketsCount; j++)
			{
                p += capacity[j]; 
			}

            OPEN = new PQ(p);
            STATES.Add(s.GetHashCode(), s);
            OPEN.Enqueue(s.Priority(final_state), s);
        }


        public void Fill()
        {
            for (int i = 0; i < bucketsCount; i++)
            {
                if (dqs.current_state[i] != capacity[i])
                {
                    State s = new State(dqs);
                    s.current_state[i] = capacity[i];
                    s.oper = Operation.Fill;
                    Process(s);
                }
            }
        }

        public void Empty() {
            for (int i = 0; i < bucketsCount; i++)
            {
                if (dqs.current_state[i] != 0)
                {
                    State s = new State(dqs);
                    s.current_state[i] = 0;
                    s.oper = Operation.Empty;
                    Process(s);
                }
            }
        }

        public void Pour()
        {
            for (int i = 0; i < bucketsCount; i++)
            {
                for (int j = 0; j < bucketsCount; j++)
                {
                    if (i != j && dqs.current_state[i] != 0 && dqs.current_state[j] != capacity[j])
                    {
                        State s = new State(dqs);
                        int total = dqs.current_state[i] + dqs.current_state[j];
                        s.current_state[i] = (capacity[j] > total) ? 0 : total - capacity[j];
                        s.current_state[j] = (total < capacity[j]) ? total : capacity[j];
                        s.oper = Operation.Pour;
                        Process(s);
                    }
                }
            }
        }
	

        private void Process(State s)
        {
            if (bestSolution == null || bestSolution.path > s.path)
            {
                if (s.IsSolution(final_state))
                {
                    bestSolution = s;
                    throw new Exception("Found 1.solution");
                }
                else
                {
                    if (!STATES.ContainsKey(s.GetHashCode()))
                    {
                        STATES.Add(s.GetHashCode(), s);
                        OPEN.Enqueue(s.Priority(final_state),s);
                    }
                }
            }
        }


        public void Compute()
        {
            while (!OPEN.Empty())
            {
                dqs = OPEN.Dequeue();
                vistited_states++;

                try
                {
                    Fill();
                    Empty();
                    Pour();
                }
                catch (Exception)
                {                    
                    return;
                }

            }
        }


        public override string ToString()
        {
            string str = bestSolution.ToString();
            str += String.Format("Path / States: {0}/{1} ({2})", bestSolution.path, vistited_states, STATES.Count);
            str += Environment.NewLine;            
            return str;
        }

    }
}
