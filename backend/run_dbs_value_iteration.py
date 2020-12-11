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
The experiments for value iteration with the DBS operator in the GridWorld environment.
"""


import math
import copy
import time
import pickle

import numpy as np

from env import GridWorldEnv
from agent import ValueIterationAgent, DbsValueIterationAgent
from util import infinity_norm


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
