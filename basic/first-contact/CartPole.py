import gymnasium as gym
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# This is the basic implementation of CatPole, described on the first tutorial of Gymnasium
# There will be ten tests and we'll plot the total reward per test

# Discrete action space (button presses)
env = gym.make("CartPole-v1", render_mode="human")
print(f"Action space: {env.action_space}")
print(f"Sample action: {env.action_space.sample()}")

print("\\\\\\\\\\\\\\\\\\")
# Box observation space (continuous values)
print(f"Observation space: {env.observation_space}")
print(f"Sample observation: {env.observation_space.sample()}")
print("\\\\\\\\\\\\\\\\\\")

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
