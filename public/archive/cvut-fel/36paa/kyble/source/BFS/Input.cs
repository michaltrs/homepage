using System;
using System.Collections.Generic;
using System.Text;

namespace Kyble_BFS
{
    class Input
    {
        public int[] capacity;
        public int[] init_state;        
        public int[] final_state;

        // capacity, init_state, final_state
        public Input(int[] capacity, int[] init_state, int[] final_state)
        {
            this.capacity = capacity;
            this.init_state = init_state;
            this.final_state = final_state;
        }

    }
}
