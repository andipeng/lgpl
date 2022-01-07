import argparse
import os
import pickle
from os import getcwd

import gym
import numpy as np
import torch
import torch.optim as optim
from lgpl.algos.ppo import PPO
from lgpl.models.mlp import MLP
from lgpl.models.baselines import NNBaseline
from lgpl.policies.discrete import CategoricalNetwork
import torch.nn as nn
import lgpl.envs.pusher.pusher_env3

parser = argparse.ArgumentParser()
variant_group = parser.add_argument_group('variant')
variant_group.add_argument('--exp_dir', default='tmp')
variant_group.add_argument('--gpu', action='store_true')
variant_group.add_argument('--mode', default='local')
variant_group.add_argument('--exp_id_start', default=0)
variant_group.add_argument('--exp_id_stride', default=1)
v_command_args = parser.parse_args()
command_args = {k.dest:vars(v_command_args)[k.dest] for k in variant_group._group_actions}

seed = 111
env_version = 4
#pusher_id = range(int(command_args['exp_id_start']), 1000, int(command_args['exp_id_stride'])
pusher_id = 0

env_id = 'PusherEnv2v%d-v%d' % (pusher_id, env_version)
env = gym.make(env_id)

obs_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

path_len = 350
# Make policy
policy = CategoricalNetwork(prob_network=MLP(obs_dim, action_dim, final_act=nn.Softmax), output_dim=action_dim)
baseline = NNBaseline(MLP(obs_dim, 1, hidden_sizes=(64, 64)))

n_envs = 20
algo = PPO(env, env_id, policy, baseline, obs_dim=obs_dim, action_dim=action_dim,
            optimizer=optim.Adam(list(policy.parameters()) + list(baseline.parameters()), lr=1e-3), max_path_length=path_len,
            batch_size=path_len*n_envs, plot=True, n_itr=500, save_step=2, use_gae=False, terminate_early=True,
            save_last=True, ppo_batch_size=128, entropy_bonus=0.001)

algo.train()