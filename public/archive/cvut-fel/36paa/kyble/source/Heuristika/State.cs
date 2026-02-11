using System;
using System.Collections.Generic;
using System.Text;

namespace Kyble_heuristika
{
    public enum Operation { Fill, Empty, Pour, None }

    class State
    {
        public int[] current_state;
        private State parent;
        public int path = 0;
        public Operation oper = Operation.None;



        public State(State parent)
        {
            this.current_state = (int[])parent.current_state.Clone();
            this.parent = parent;
            this.path = parent.path + 1;
        }

        public State(int[] init_state)
        {
            this.current_state = init_state;
            this.parent = null;
            this.path = 0;
        }


        public bool IsSolution(int[] final_state)
        {
            for (int i = 0; i < current_state.Length; i++)
            {
                if (current_state[i] != final_state[i])
                {
                    return false;
                }
            }
            return true;
        }


        public override int GetHashCode()
        {
            int shift = sizeof(int) * 8 / current_state.Length;
            int res = 0;

            for (int i = 0; i < current_state.Length; i++)
            {
                res |= (current_state[i] << (shift * i));
            }
            return res;

        }

        public int Priority(int[] final_state)
        {
            int res = 0;
            for (int i = 0; i < current_state.Length; i++)
            {
                res += Math.Abs(final_state[i] - current_state[i]);
            }
            return res;
        }


        public override string ToString()
        {
            string str = "";

            if (parent != null)
            {
                str += this.parent.ToString();
            }

            for (int i = 0; i < current_state.Length; i++)
            {
                str += String.Format("{0},\t", current_state[i]); 
            }

            str += "\t";

            switch (oper)
            {
                case Operation.Empty:
                    str += "Empty";
                    break;
                case Operation.Fill:
                    str += "Fill";
                    break;
                case Operation.None:
                    str += "None";
                    break;
                case Operation.Pour:
                    str += "Pour";
                    break;
            }


            str += Environment.NewLine;

            return str;
        }
    }
}
