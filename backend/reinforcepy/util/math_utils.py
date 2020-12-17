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
"""Some utility functions for mathematics.
"""

import math

import numpy as np

def infinity_norm(x_vector):
    return max([ abs(x_item) for x_item in x_vector ])

def boltzmann_softmax(x_list, beta):
    # The max x
    x_max = max(x_list)

    # Divide both the numerator and the denominator by exp(x_max) to overcome the overflow error
    numerator = sum([ np.exp(beta * (x - x_max)) * x for x in x_list ])
    denominator = sum([ np.exp(beta * (x - x_max)) for x in x_list ])

    return numerator / denominator

def vector_norm(x_list, order):
    return math.pow(sum([ math.pow(abs(x), order) for x in x_list ]), 1 / order)
