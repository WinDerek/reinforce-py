#!/bin/bash

# RLLib requires Mujoco 2.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/derek/.mujoco/mujoco200/bin

# Run the Python script using the  rllib_env
~/miniconda3/envs/rllib_env/bin/python rllib_sac.py
