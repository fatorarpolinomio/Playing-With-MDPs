import gymnasium as gym
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

# This code follows the same structure as the CartPole

env = gym.make("CarRacing-v3", render_mode="human")
env.observation_space.shape

observation, info = env.reset()

print(f"Starting observation: {observation}")

reward_list = []
test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for test in test_list:
    episode_over = False
    total_reward = 0
    while not episode_over:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        episode_over = terminated or truncated
    print(f"Episode finished! Total reward: {total_reward}")
    reward_list.append(total_reward)
    observation, info = env.reset()

env.close()

plt.plot(test_list, reward_list)
plt.xlabel("Test")
plt.ylabel("Total Reward")
plt.title("Reward per Test")
plt.show()
