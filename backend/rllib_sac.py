import ray
from ray import tune
from ray.rllib.agents.sac import SACTrainer

ray.init(dashboard_host="0.0.0.0", dashboard_port=41551)

tune.run(SACTrainer, config={
    "env": "HalfCheetah-v3",
    "num_gpus": 1,
    "framework": "torch",

    # === Model ===
    # Use two Q-networks (instead of one) for action-value estimation.
    # Note: Each Q-network will have its own target network.
    "twin_q": True,
    # Model options for the Q network(s).
    "Q_model": {
        "fcnet_activation": "relu",
        "fcnet_hiddens": [256, 256],
    },
    # Model options for the policy function.
    "policy_model": {
        "fcnet_activation": "relu",
        "fcnet_hiddens": [256, 256],
    },

    # === Learning ===
    # Update the target by \tau * policy + (1-\tau) * target_policy.
    "tau": 5e-3,
    # Initial value to use for the entropy weight alpha.
    "initial_alpha": 1.0,
    # N-step target updates. If >1, sars' tuples in trajectories will be
    # postprocessed to become sa[discounted sum of R][s t+n] tuples.
    "n_step": 1,
    # Number of env steps to optimize for before returning.
    "timesteps_per_iteration": 100,

    # === Replay buffer ===
    # Size of the replay buffer. Note that if async_updates is set, then
    # each worker will have a replay buffer of this size.
    "buffer_size": int(1e6),

    # === Optimization ===
    "optimization": {
        "actor_learning_rate": 3e-4,
        "critic_learning_rate": 3e-4,
        "entropy_learning_rate": 3e-4,
    },
    # If not None, clip gradients during optimization at this value.
    "grad_clip": None,
    # How many steps of the model to sample before learning starts.
    "learning_starts": 1500,
    # Update the replay buffer with this many samples at once. Note that this
    # setting applies per-worker if num_workers > 1.
    "rollout_fragment_length": 1,
    # Size of a batched sampled from replay buffer for training. Note that
    # if async_updates is set, then each worker returns gradients for a
    # batch of this size.
    "train_batch_size": 256,
    # Update the target network every `target_network_update_freq` steps.
    "target_network_update_freq": 0,
})
