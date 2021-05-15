import gym
import tianshou as ts

env = gym.make('CartPole-v0')

train_envs = gym.make('CartPole-v0')
test_envs = gym.make('CartPole-v0')

import torch, numpy as np
from torch import nn

class Net(nn.Module):
    def __init__(self, state_shape, action_shape):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(np.prod(state_shape), 128), nn.ReLU(inplace=True),
            nn.Linear(128, 128), nn.ReLU(inplace=True),
            nn.Linear(128, 128), nn.ReLU(inplace=True),
            nn.Linear(128, np.prod(action_shape)),
        )

    def forward(self, obs, state=None, info={}):
        if not isinstance(obs, torch.Tensor):
            obs = torch.tensor(obs, dtype=torch.float)
        batch = obs.shape[0]
        logits = self.model(obs.view(batch, -1))
        return logits, state

state_shape = env.observation_space.shape or env.observation_space.n
action_shape = env.action_space.shape or env.action_space.n
net = Net(state_shape, action_shape)
optim = torch.optim.Adam(net.parameters(), lr=1e-3)

policy = ts.policy.DQNPolicy(net, optim, discount_factor=0.9, estimation_step=3, target_update_freq=320)

train_collector = ts.data.Collector(policy, train_envs, ts.data.ReplayBuffer(size=20000))
test_collector = ts.data.Collector(policy, test_envs)

result = ts.trainer.offpolicy_trainer(
    policy, train_collector, test_collector,
    max_epoch=10, step_per_epoch=1000, collect_per_step=10,
    episode_per_test=100, batch_size=64,
    train_fn=lambda epoch, env_step: policy.set_eps(0.1),
    test_fn=lambda epoch, env_step: policy.set_eps(0.05),
    stop_fn=lambda mean_rewards: mean_rewards >= env.spec.reward_threshold,
    writer=None)
print(f'Finished training! Use {result["duration"]}')

# from torch.utils.tensorboard import SummaryWriter
# writer = SummaryWriter('log/dqn')

# policy.eval()
# policy.set_eps(0.05)
# collector = ts.data.Collector(policy, env)
# collector.collect(n_episode=1, render=1 / 35)
