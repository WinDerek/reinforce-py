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

def format_time(time_interval_in_second):
    days = int(time_interval_in_second / 3600 / 24)
    time_interval_in_second = time_interval_in_second - days * 3600 * 24
    hours = int(time_interval_in_second / 3600)
    time_interval_in_second = time_interval_in_second - hours * 3600
    minutes = int(time_interval_in_second / 60)
    time_interval_in_second = time_interval_in_second - minutes * 60
    secondsf = int(time_interval_in_second)
    time_interval_in_second = time_interval_in_second - secondsf
    millis = int(time_interval_in_second * 1000)

    f = ''
    i = 1
    if days > 0:
        f += str(days) + 'd'
        i += 1
    if hours > 0 and i <= 2:
        f += str(hours) + 'h'
        i += 1
    if minutes > 0 and i <= 2:
        f += str(minutes) + 'm'
        i += 1
    if secondsf > 0 and i <= 2:
        f += str(secondsf) + 's'
        i += 1
    if millis > 0 and i <= 2:
        f += str(millis) + 'ms'
        i += 1
    if f == '':
        f = '0ms'
    return f
