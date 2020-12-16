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

import numpy as np
import random

def true_with_probability(prob):
    # Check legal input or not
    if prob < 0 or prob > 1:
        raise ValueError('The argument prob must be in range [0, 1], got {}'.format(prob))
    
    return random.random() < prob


def sample_from_distibution(distribution):
    """Samples a choice according to the probability distribution of the choices. Only for discrete cases.

    0.0------|--rand----|----|----1.0

    Arguments:
        distribution: {dict}. -- { choice : probability }.
    """

    rand = random.random()
    range_right = 0.0
    for choice, probability in distribution.items():
        range_right += probability
        if range_right > rand:
            return choice
