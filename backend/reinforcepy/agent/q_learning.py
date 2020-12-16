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
Agents using the Q-learning algorithm.
"""

from .agent import Agent
from reinforcepy.util.random_utils import sample_from_distribution

class QLearningAgent(Agent):
    def __init__(self, name="QLearningAgent", alpha=0.1, epsilon=0.1, **kwds):
        super().__init__(name=name, **kwds)

        self.alpha = alpha
        self.epsilon = epsilon

        self.reset()

    def reset(self):
        super().reset()

        self.current_state = self.env.starting_index
        self.q_2darray = np.zeros((len(self.env.state_space), len(self.env.action_space)), dtype=float) # The q(s, a) can be retrieved by calling self.q_2darray[state_index][action_index]
        self.policy_2darray = np.zeros((len(self.env.state_space), len(self.env.action_space)), dtype=float) # The policy \pi(a|s) can be retrieved by calling self.policy_2darray[state_index][action_index]
    
    def take_action(self):
        # Get the index of the current state in the state space
        current_state_index = self.env.state_space.index(self.current_state)

        # Update the policy for the current state from q(current_state, .)
        self.__update_policy(current_state_index)

        # Sample the action from the latest policy
        sampled_action = sample_from_distribution({ action: self.policy_2darray[current_state_index][self.env.action_space.index(action)] for action in actions})
        sampled_action_index = self.env.action_space.index(sampled_action)

        # Take the action by interacting with the environment and observe the reward and the next state
        observation, reward, done, info = self.env.step(sampled_action)
        state_to = observation
        state_to_index = self.env.state_space.index(state_to)

        # Update the q value
        old_q = self.q_2darray[current_state_index][sampled_action_index]
        new_q = old_q + self.alpha * (reward + self.discount * max([ self.q_2darray[state_to_index][self.env.action_space.index(a)] for a in actions_given_state(state_to) ]) - old_q)
        self.q_2darray[current_state_index][sampled_action_index] = new_q

        # # Calculate the two new state values
        # newStateValue = sum([grid_data_list[current_state]['policy'][action] * grid_data_list[current_state]['q'][action] for action in self.env.actions_given_state(current_state)])

        # Move on to the next state
        self.current_state = state_to

        return done
    
    def __update_policy(self, current_state_index):
        # Get the optimal q value
        q_list = []
        actions = self.env.actions_given_state(current_state)
        for action in actions:
            action_index = self.env.action_space.index(action)
            q_list.append(self.q_2darray[current_state_index][action_index])
        optimal_q = max(q_list)
        
        # Count the number of actions with the optimal q value
        count = 0
        for action in actions:
            action_index = self.env.action_space.index(action)
            if self.q_2darray[current_state_index][action_index] == optimal_q:
                count += 1

        # Update the policy distribution
        for action in actions:
            action_index = self.env.action_space.index(action)
            if self.q_2darray[current_state_index][action_index] == optimal_q:
                self.policy_2darray[current_state_index][action] = self.epsilon / len(actions) + (1 - self.epsilon) / count
            else:
                self.policy_2darray[current_state_index][action_index] = self.epsilon / len(actions)
                # print(grid_data_list[current_state]['policy'][action])
