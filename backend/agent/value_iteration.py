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


class GviAgent(Agent):
    """Generialized value iteration.
    """


    def __init__(self, name="GviAgent", operator, **kwds):
        super().__init__(name, **kwds)

        self.operator = operator


def DbsValueIterationAgent():
    return GviAgent(name="DbsValueIterationAgent", operator=)
