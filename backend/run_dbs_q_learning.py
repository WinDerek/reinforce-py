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
The experiments for DBS Q-learning in the GridWorld environment.
"""

import math
import copy
import time
import pickle

import numpy as np

from openenv.env import GridWorldEnv
from openenv.util.math_utils import infinity_norm
from openenv.util.time_utils import format_time

from reinforcepy.agent import QLearningAgent
from dbs.config import Q_LEARNING_CONFIG as config
from dbs.config import GRID_WORLD

total_begin_time = time.time()

def run_agent(agent):
    number_of_step_to_goal_array = np.zeros(config['episode_num'], dtype=int)
    for episode_index in range(config['episode_num']):
        for step_index in range(config['episode_max_length']):
            done = agent.take_action()

            if done:
                break
        
        # Record the number of steps from the starting to the goal in this episode
        number_of_step_to_goal_array[episode_index] = agent.current_step

        # Set the agent to a new episode
        agent.new_episode()
    
    return number_of_step_to_goal_array

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

# Create the agents
agent_list = []
agent_list.append(QLearningAgent(name=r"Q-learning", discount=config['discount'], env=copy.deepcopy(grid_world_env), epsilon=0.01, alpha=0.01))

# Run the agents one by one
number_of_step_to_goal_2darray = np.zeros((len(agent_list), config['episode_num']), dtype=int)
for agent_index, agent in enumerate(agent_list):
    begin_time = time.time()

    number_of_step_to_goal_array = run_agent(agent)
    number_of_step_to_goal_2darray[agent_index] = number_of_step_to_goal_array

    end_time = time.time()
    print("Agent {:s} finished in {:s}.".format(agent.name, format_time(end_time - begin_time)))

# Dump the experiments result
experiments_results = {
    'number_of_step_to_goal_2darray': number_of_step_to_goal_2darray,
    'agent_name_list': [ agent.name for agent in agent_list ]
}
filename = "dbs_q_learning_experiments_results.pkl"
with open(filename, "wb") as f:
    pickle.dump(experiments_results, f)
    print("Experiments_results successfully dumped to file \'{:s}\'.".format(filename))

total_end_time = time.time()
print("DBS Q-learning experiments conducted in {:s}.".format(format_time(total_end_time - total_begin_time)))
