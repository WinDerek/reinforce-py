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
import copy

import numpy as np

from .agent import Agent
from reinforcepy.util.math_utils import boltzmann_softmax

class GviAgent(Agent):
    """Generialized value iteration.
    """

    def __init__(self, name="GviAgent", in_place=False, random_initialization=False, **kwds):
        super().__init__(name=name, **kwds)

        self.in_place = in_place
        self.random_initialization = random_initialization

        self.reset()
    
    def reset(self):
        # If random initialization
        if self.random_initialization:
            self.q_2darray = np.random.rand(len(self.env.state_space), 4)
            self.v_array = np.random.rand(len(self.env.state_space))
            self.v_array[self.env.state_space.index(self.env.goal_index)] = 0.0 # v(terminal) = 0
        # Else, all zero initialization
        else:
            self.q_2darray = np.zeros((len(self.env.state_space), 4), dtype=float)
            self.v_array = np.zeros(len(self.env.state_space), dtype=float)

        super().reset()

    def take_action(self):
        for state_index, state in enumerate(self.env.state_space):
            old_v_array = copy.deepcopy(self.v_array)

            # Update q(s, a) for all a
            # for action_index, action in enumerate(self.env.state_space): # TODO: Check this difference with that in the pseudocode
            for action in self.env.actions_given_state(state):
                state_to = self.env.state_transition(action, state)
                state_to_index = self.env.state_space.index(state_to)
                action_index = self.env.action_space.index(action)
                
                # If the in-place update mechanism is used
                if self.in_place:
                    self.q_2darray[state_index][action_index] = self.env.reward(state, action) + self.discount * self.v_array[state_to_index]
                else:
                    self.q_2darray[state_index][action_index] = self.env.reward(state, action) + self.discount * old_v_array[state_to_index]

                # # TODO: Debugging...
                # print("action = {:d}, (from, to) = ({:d}, {:d})".format(action, state, state_to))
                # print("update q(s, a) = q({:d}, {:d}) = {:.4f} + {:.4f} * {:.4f} = {:.4f}".format(state, action, self.env.reward(state, action), self.discount, self.v_array[state_to_index], self.q_2darray[state_index][action_index]))

            # Update v(s)
            # self.v_array[state_index] = self.operator(self.q_2darray[state_index]) # TODO: Check this difference with that in the pseudocode
            self.v_array[state_index] = self.operator(self.q_2darray[state_index][self.env.actions_given_state(state)])

            # TODO: Debugging...
            # print(self.q_2darray[state_index])
            # print("s = ", state, ", actions = ", self.env.actions_given_state(state))
            # print("q(s, .) = ", self.q_2darray[state_index][self.env.actions_given_state(state)])
            # print("v(s) = operator(q(s, .)) = ", self.v_array[state_index])
        
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
        beta = self.beta_function(self.current_step)
        
        return boltzmann_softmax(q_array, beta)
