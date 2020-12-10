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


from .env import GridWorldEnv
from .agent import DbsValueIterationAgent


# Create the GridWorld Environment
gridWorldEnv = GridWorldEnv(
    name="GirldWorldEnv of size (10, 10)",
    episode_max_length=300,
    size=(10, 10),
    starting_index=0,
    goal_index=98,
    goal_reward=1.0,
    wall_index_list=[ 1, 7, 11, 17, 21, 27, 31, 37, 41, 47, 51, 57, 61, 67, 81, 87, 88, 91, 97 ])


# Create the agent
agent = DbsValueIterationAgent(discount=0.9, )
