import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines.common import set_global_seeds
from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines import PPO2
from gym_unity.envs import UnityEnv


def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = UnityEnv(env_id, rank)
        env.seed(seed + rank)
        return env
    set_global_seeds(seed)
    return _init

env_id = './envs/Walker'
num_cpu = 4  # Number of processes to use
# Create the vectorized environment
env = SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)])
# Automatically normalize the input features
env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)
# env = VecNormalize(env, norm_obs=True, norm_reward=False)

model = PPO2(MlpPolicy, env, 
    gamma=0.99,
    learning_rate=1.0e-3,
    lam=0.95,
    n_steps=512,
    verbose=1)
model.learn(total_timesteps=1000000)
model.save("./models/my-model")

