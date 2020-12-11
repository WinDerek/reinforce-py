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
"""Calculates the optimal v list for the DBS value iteration experiments.
"""


import math
import copy
import time
import pickle

import numpy as np

from env import GridWorldEnv
from agent import ValueIterationAgent
from dbs_experiments_config import VALUE_ITERATION_SETTINGS as config
from dbs_experiments_config import GRID_WORLD


# Create the GridWorld Environment
grid_world_env = GridWorldEnv(
    name="GirldWorldEnv of size (10, 10)",
    state_space=GRID_WORLD['state_space'],
    action_space=GRID_WORLD['action_space'],
    episode_max_length=config['episode_max_length'],
    size=(GRID_WORLD['row_count'], GRID_WORLD['column_count']),
    starting_index=GRID_WORLD['starting_index'],
    goal_index=GRID_WORLD['goal_index'],
    goal_reward=GRID_WORLD['goal_reward'],
    wall_index_list=GRID_WORLD['wall_index_list'])


# Create the value iteration agent
value_iteration_agent = ValueIterationAgent(discount=config['discount'], env=grid_world_env)


# Calculate the optimal v list
begin_time = time.time()
for step in range(1, config['optimal_step_num'] + 1):
    value_iteration_agent.take_action()

    # Print progress information
    if step % 10000 == 0:
        current_time = time.time()
        print("{:>8d}/{:<8d} iterations finished in {:>10f}s.".format(step, config['optimal_step_num'], current_time - begin_time))
optimal_v_array = value_iteration_agent.v_array


# Dump the optimal_v_list
filename = "dbs_value_iteration_optimal_v_array.pkl"
with open(filename, "wb") as f:
    pickle.dump(optimal_v_array, f)
    print("optimal_v_array has been successfully dumped to file \'{:s}\'.".format(filename))
