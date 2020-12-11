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
The Env class represents the environment in reinforcement learning.

The API design is partly inspired by the Env class from `OpenAI Gym <https://github.com/openai/gym/blob/master/gym/core.py>`_
"""


class Env:
    def __init__(self, name="Env", state_space=None, action_space=None, episode_max_length=300):
        self.name = name
        self.state_space = state_space
        self.action_space = action_space
        self.episode_max_length = episode_max_length


class GridWorldEnv(Env):
    """Grid World, the famous toy environment in reinforcement learning.

    Specification:
    - Borders block actions. For example, if the agent is now at the top of the grid world, then it is not allowed to move up.
    - Walking into a wall grid will only make the agent stay its original position. The action towards a wall grid is allowed.
    """

    def __init__(
        self,
        size,
        starting_index,
        goal_index,
        goal_reward,
        wall_index_list,
        name="GridWorldEnv",
        **kwds):
        super().__init__(name=name, **kwds)

        self.size = size
        self.starting_index = starting_index
        self.goal_index = goal_index
        self.goal_reward = goal_reward
        self.wall_index_list = wall_index_list
    

    def print_info(self):
        print("size: ", self.size)
        print("starting_index: ", self.starting_index)
        print("goal_index: ", self.goal_index)
        print("goal_reward: ", self.goal_reward)
        print("wall_index_list: ", self.wall_index_list)
        print("name: ", self.name)
        print("state_space: ", self.state_space)
        print("action_space: ", self.action_space)
    

    def step(action):
        # TODO
        observation = None

        reward = None

        done = False

        info = None

        return observation, reward, done, info
    

    def reward(self, state, action):
        state_to = self.state_transition(action, state)

        if state_to == self.goal_index:
            return self.goal_reward
        else:
            return 0.0
    

    def actions_given_state(self, state):
        """
        Returns: a list of int. The elements of the list represent the indices of all the legal actions given the state.
        
        Args:
        - state: int. The index of the state.
        """

        # If the state is the terminal state (goal)
        if state == self.goal_index:
            return [ 0, 1, 2, 3 ]

        row_count = self.size[0]
        column_count = self.size[1]
        row_index = state // column_count
        column_index = state % column_count
        
        action_list = []
        if row_index != 0:
            action_list.append(0)
        if column_index != column_count - 1:
            action_list.append(1)
        if row_index != row_count - 1:
            action_list.append(2)
        if column_index != 0:
            action_list.append(3)

        return action_list


    def state_transition(self, action, state_from):
        """
        Args:
        - action: int. The index of the action. Must be legal! (Not checked here for better performance.)
        - state_from: int. The index of the current state.
        """

        # According to the current design of the GridWorld environment, the current state argument should not be the goal state! Here we skip the exception check for better performance.
        # # If the current state is the goal state
        # if state_from == self.goal_index:
        #     return self.starting_index

        # If the current state is the terminal state (goal)
        if state_from == self.goal_index:
            # Go to the starting point
            return self.starting_index
        
        column_count = self.size[1]
        row_index = state_from // column_count
        column_index = state_from % column_count

        # Up
        if action == 0:
            row_index -= 1
        # Right
        elif action == 1:
            column_index += 1
        # Down
        elif action == 2:
            row_index += 1
        # Left
        elif action == 3:
            column_index -= 1
        else:
            raise ValueError("Illegal action: {:d}".format(action))

        # Check if the state_to is a wall
        state_to = row_index * column_count + column_index
        if state_to in self.wall_index_list:
            return state_from
        else:
            return state_to
