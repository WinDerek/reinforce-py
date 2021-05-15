import ray
from ray import tune
from ray.rllib.agents.dqn import DQNTrainer

ray.init(dashboard_host="0.0.0.0", dashboard_port=41551)

tune.run(DQNTrainer, config={ "env": "CartPole-v0", "num_gpus": 1, "framework": "torch", "exploration_config": { "type": "SoftQ", "temperature": 1.0 } })
tune.run(DQNTrainer, config={ "env": "Ant-v2", "num_gpus": 1, "framework": "torch", "exploration_config": { "type": "SoftQ", "temperature": 1.0 } })
