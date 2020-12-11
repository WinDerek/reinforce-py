# Copyright 2020 Jianfeng Hou <frankderekdick@gmail.com>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Agents using the value iteration algorithm.
"""


import math

import numpy as np

from .agent import Agent


class GviAgent(Agent):
    """Generialized value iteration.
    """


    def __init__(self, name="GviAgent", **kwds):
        super().__init__(name=name, **kwds)

        self.reset()
    

    def reset(self):
        self.q_2darray = np.zeros((len(self.env.state_space), 4), dtype=float)
        self.v_array = np.zeros(len(self.env.state_space), dtype=float)

        super().reset()


    def take_action(self):
        for state_index, state in enumerate(self.env.state_space):
            # Update q(s, a) for all a
            for action_index, action in enumerate(self.env.actions_given_state(state)):
                state_to = self.env.state_transition(action, state)
                # print(state_to)
                state_to_index = self.env.state_space.index(state_to)
                self.q_2darray[state_index][action_index] = self.env.reward(state, action) + self.discount * self.v_array[state_to_index]

            # Update v(s)
            self.v_array[state_index] = self.operator(self.q_2darray[state_index])
        
        # Increment the current step
        self.current_step += 1
    

    def operator(self, q_array):
        raise NotImplementedError


class ValueIterationAgent(GviAgent):
    def __init__(self, name="ValueIterationAgent", **kwds):
        super().__init__(name=name, **kwds)
    

    def operator(self, q_array):
        return max(q_array)


class DbsValueIterationAgent(GviAgent):
    def __init__(self, beta_function, name="DbsValueIterationAgent", **kwds):
        super().__init__(name=name, **kwds)

        self.beta_function = beta_function

    
    def operator(self, q_array):
        def boltzmann_softmax(x_list, beta):
            numerator = sum([ math.exp(beta * x) * x for x in x_list ])
            denominator = sum([ math.exp(beta * x) for x in x_list ])

            return numerator / denominator

        beta = self.beta_function(self.current_step)
        
        return boltzmann_softmax(q_array, beta)
