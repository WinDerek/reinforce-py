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
"""The configurations of the DBS experiments.
"""


# The Grid World settings
wall_index_list = [ 1, 7, 11, 17, 21, 27, 31, 37, 41, 47, 51, 57, 61, 67, 81, 87, 88, 91, 97 ]
GRID_WORLD = {
    'row_count': 10,
    'column_count': 10,
    'wall_index_list': wall_index_list,
    'state_space': [ grid_index for grid_index in range(10 * 10) if grid_index not in wall_index_list ], # The state is the grid index and state 0 is at the top left corner
    'action_space': [ 0, 1, 2, 3 ], # 0 for UP, 1 for RIGHT, 2 for DOWN, and 3 for LEFT
    'starting_index': 0,
    'goal_index': 98,
    'goal_reward': 1.0
}


# DBS value iteration settings
VALUE_ITERATION_CONFIG = {
    'discount': 0.9,
    'episode_num': 500,
    'episode_max_length': 1, #300,
    'optimal_step_num': 100 * 10000
}


# DBS Q-learning settings
# TODO


# DBS DQN settings
# TODO
