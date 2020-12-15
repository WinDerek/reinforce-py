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

from openenv.env import GridWorldEnv
from openenv.agent import ValueIterationAgent, DbsValueIterationAgent
from util import infinity_norm, format_time
from dbs.config import VALUE_ITERATION_CONFIG as config
from dbs.config import GRID_WORLD


total_begin_time = time.time()


def value_loss(v_list, optimal_v_list):
    return infinity_norm([ abs(v - optimal_v) for v, optimal_v in zip(v_list, optimal_v_list) ])


def run_agent(agent):
    # Start value iteration
    value_loss_array = np.zeros(config['episode_max_length'] * config['episode_num'], dtype=float)
    for episode_index in range(config['episode_num']):
        for step_index in range(config['episode_max_length']):
            agent.take_action()

            step_index = config['episode_max_length'] * episode_index + step_index
            value_loss_array[step_index] = value_loss(agent.v_array, optimal_v_array)
    
    return value_loss_array


# Load the optimal v
filename = "dbs_value_iteration_optimal_v_array.pkl"
with open(filename, "rb") as f:
    optimal_v_array = pickle.load(f)


# Create the GridWorld Environment
grid_world_env = GridWorldEnv(
    name="GirldWorldEnv of size ({:d}, {:d})".format(GRID_WORLD['row_count'], GRID_WORLD['column_count']),
    state_space=GRID_WORLD['state_space'],
    action_space=GRID_WORLD['action_space'],
    episode_max_length=config['episode_max_length'],
    size=(GRID_WORLD['row_count'], GRID_WORLD['column_count']),
    starting_index=GRID_WORLD['starting_index'],
    goal_index=GRID_WORLD['goal_index'],
    goal_reward=GRID_WORLD['goal_reward'],
    wall_index_list=GRID_WORLD['wall_index_list'])
print(grid_world_env.print_info())


# Create the DBS value iteration agents
agent_list = []
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = 0.1$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: 0.1, in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = 1$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: 1, in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = 10$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: 10, in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = 100$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: 100, in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = 1000$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: 1000, in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = t$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: t, in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = t^2$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: math.pow(t, 2), in_place=False))
agent_list.append(DbsValueIterationAgent(name=r"$\beta_t = t^3$", discount=config['discount'], env=copy.deepcopy(grid_world_env), beta_function=lambda t: math.pow(t, 3), in_place=False))


# Run the agents one by one
value_loss_2darray = np.zeros((len(agent_list), config['episode_max_length'] * config['episode_num']), dtype=float)
for agent_index, agent in enumerate(agent_list):
    begin_time = time.time()

    value_loss_array = run_agent(agent)
    value_loss_2darray[agent_index] = value_loss_array

    end_time = time.time()
    print("Agent {:s} finished in {:s}.".format(agent.name, format_time(end_time - begin_time)))


# Dump the experiments result
experiments_results = {
    'value_loss_2darray': value_loss_2darray,
    'agent_name_list': [ agent.name for agent in agent_list ]
}
filename = "dbs_value_iteration_experiments_results.pkl"
with open(filename, "wb") as f:
    pickle.dump(experiments_results, f)
    print("experiments_results has been successfully dumped to file \'{:s}\'.".format(filename))


total_end_time = time.time()
print("DBS value iteration experiments conducted in {:s}.".format(format_time(total_end_time - total_begin_time)))
