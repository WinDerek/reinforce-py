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
The experiments for value iteration with the DBS operator on the GridWorld environment.
"""


import math
import copy
import time
import pickle

import numpy as np

from env import GridWorldEnv
from agent import ValueIterationAgent, DbsValueIterationAgent


# RL Algorithm settings
DISCOUNT = 0.9
EPISODE_NUM = 500
EPISODE_MAX_LENGTH = 300
OPTIMAL_STEP_NUM = 100 * 10000


# Environment settings
ROW_COUNT = 10
COLUMN_COUNT = 10
WALL_INDEX_LIST = [ 1, 7, 11, 17, 21, 27, 31, 37, 41, 47, 51, 57, 61, 67, 81, 87, 88, 91, 97 ]
STATE_SPACE = [ grid_index for grid_index in range(ROW_COUNT * COLUMN_COUNT) ] # The state is the grid index and state 0 is at the top left corner
ACTION_SPACE = [ 0, 1, 2, 3 ] # 0 for UP, 1 for RIGHT, 2 for DOWN, and 3 for LEFT
STARTING_INDEX = 0
GOAL_INDEX = 98
GOAL_REWARD = 1.0


def infinity_norm(x_list):
    return max([ abs(x) for x in x_list ])


def value_loss(v_list, optimal_v_list):
    return infinity_norm([ abs(v - optimal_v) for v, optimal_v in zip(v_list, optimal_v_list) ])


# Create the GridWorld Environment
grid_world_env = GridWorldEnv(
    name="GirldWorldEnv of size (10, 10)",
    state_space=STATE_SPACE,
    action_space=ACTION_SPACE,
    episode_max_length=EPISODE_MAX_LENGTH,
    size=(ROW_COUNT, COLUMN_COUNT),
    starting_index=STARTING_INDEX,
    goal_index=GOAL_INDEX,
    goal_reward=GOAL_REWARD,
    wall_index_list=WALL_INDEX_LIST)
# print(grid_world_env.print_info())


# Calculate the optimal v list
value_iteration_agent = ValueIterationAgent(discount=DISCOUNT, env=copy.deepcopy(grid_world_env))
begin_time = time.time()
for step in range(1, OPTIMAL_STEP_NUM + 1):
    value_iteration_agent.take_action()

    if step % 10000 == 0:
        current_time = time.time()
        print("{:>8d}/{:>8d} iterations finished in {:>10f}s.".format(step, OPTIMAL_STEP_NUM, current_time - begin_time))
optimal_v_list = copy.deepcopy(value_iteration_agent.v)


# Create the agent
agent = DbsValueIterationAgent(discount=DISCOUNT, env=copy.deepcopy(grid_world_env), beta_function=lambda t: 0.1)


# Start value iteration
value_loss_array = np.zeros(EPISODE_MAX_LENGTH * EPISODE_NUM, dtype=float)
for episode_index in range(EPISODE_NUM):
    for step_index in range(EPISODE_MAX_LENGTH):
        agent.take_action()

        step_index = EPISODE_MAX_LENGTH * episode_index + step_index
        value_loss_array[step_index] = value_loss(agent.v, optimal_v_list)


# Dump the value loss array
filename = "dbs_value_iteration_value_loss_array.pkl"
with open(filename, "wb") as f:
    pickle.dump(value_loss_array, f)
    print("value_loss_array has been successfully dumped to file \'{:s}\'.".format(filename))
