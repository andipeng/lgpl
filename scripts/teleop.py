import pickle
from gym.envs import register
from gym.envs.mujoco.mujoco_env import MujocoEnv
import gym
from lgpl.utils.getch import getKey

if __name__ == "__main__":
    import lgpl.envs.pusher.pusher_env3
    trajs = dict(obs=[], rewards=[], actions=[], infos=[])
    #env_id = np.random.choice(range(1000))
    #env_name = 'PusherEnv2v%d-v4' % env_id

    env = gym.make('PusherEnv2v0-v4')
    env.reset()
    env_return = 0
    while True:
        env.render()
        key = getKey()

        if key == 'a': # left
            a = 0
        elif key == 'w': # forward
            a = 2
        elif key  == 'd': # right
            a = 1
        elif key  == 's': # backward
            a = 3
        elif key  == 'q':
            pickle.dump(trajs, open('human_traj.pkl', 'wb'))
            break

        obs, reward, done, info = env.step(a)
        trajs['obs'].append(obs)
        trajs['rewards'].append(reward)
        trajs['actions'].append(a)
        trajs['infos'].append(info)
        env_return += reward
        print('reward=%.3f, return=%.3f' % (reward, env_return))

        env.render()

        if info['has_finished']:
            break