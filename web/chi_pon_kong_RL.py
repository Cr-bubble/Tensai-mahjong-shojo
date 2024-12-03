import random

class ChiPongKongEnvironment:
    def __init__(self):
        self.state = self.initialize_state()
        self.done = False

    def initialize_state(self):
        hands = [0] * 34
        action_type = random.choice(["chi", "pong", "kong"])
        if action_type == "chi":
            start = random.randint(0, 6)
            hands[start] += 1
            hands[start + 1] += 1
            hands[start + 2] += 1
        elif action_type == "pong":
            tile = random.randint(0, 33)
            hands[tile] += 3
        elif action_type == "kong":
            tile = random.randint(0, 33)
            hands[tile] += 4

        while sum(hands) < 13:
            tile = random.randint(0, 33)
            hands[tile] += 1

        return {"hands": hands, "valid_actions": self.get_valid_actions(hands)}

    def has_valid_yaku(self, hands):
        """
        檢查手牌是否有役牌
        """
        for i in range(34):
            if hands[i] >= 2:  # 假設兩張同樣的牌可作為役
                return True
        return False

    def get_valid_actions(self, hands):
        valid_actions = []
        for i in range(7):
            if hands[i] > 0 and hands[i + 1] > 0 and hands[i + 2] > 0:
                valid_actions.append("chi")
                break
        for i in range(34):
            if hands[i] >= 3:
                valid_actions.append("pong")
                break
        for i in range(34):
            if hands[i] >= 4:
                valid_actions.append("kong")
                break
        valid_actions.append("skip")
        return valid_actions

    def distance_to_hu(self, hands):
        return 13 - (self.count_complete_sets(hands) + self.count_pairs(hands))

    def count_complete_sets(self, hands):
        count = 0
        for i in range(7):
            count += min(hands[i], hands[i + 1], hands[i + 2])
        for i in range(34):
            count += hands[i] // 3
        return count

    def count_pairs(self, hands):
        return sum(1 for count in hands if count == 2)

    def count_isolated_tiles(self, hands):
        return sum(1 for count in hands if count == 1)

    def evaluate_state(self, hands, prev_hands):
        prev_distance = self.distance_to_hu(prev_hands)
        curr_distance = self.distance_to_hu(hands)

        # 基本獎勵：減少距離
        reward = (prev_distance - curr_distance) * 50

        # 額外獎勵：完成組
        reward += (self.count_complete_sets(hands) - self.count_complete_sets(prev_hands)) * 30

        # 額外獎勵：增加對子
        reward += (self.count_pairs(hands) - self.count_pairs(prev_hands)) * 20

        # 孤牌懲罰
        reward -= (self.count_isolated_tiles(hands) - self.count_isolated_tiles(prev_hands)) * 10

        # 胡牌獎勵
        if curr_distance == 0 and self.has_valid_yaku(hands):
            reward += 1000  # 有役牌胡牌的大獎勵
        elif curr_distance == 0 and not self.has_valid_yaku(hands):
            reward -= 500  # 無役牌胡牌的大懲罰

        # 設置 baseline，避免過度負分
        reward = max(reward, -50)

        return reward

    def step(self, action):
        hands = self.state["hands"].copy()
        prev_hands = hands.copy()
        valid_actions = self.state["valid_actions"]

        if action not in valid_actions and action != "skip":
            return self.state, -5, False

        if action == "skip":
            return self.state, 0.1, False

        if action == "chi":
            for i in range(7):
                if hands[i] > 0 and hands[i + 1] > 0 and hands[i + 2] > 0:
                    hands[i] -= 1
                    hands[i + 1] -= 1
                    hands[i + 2] -= 1
                    break
        elif action == "pong":
            for i in range(34):
                if hands[i] >= 3:
                    hands[i] -= 3
                    break
        elif action == "kong":
            for i in range(34):
                if hands[i] >= 4:
                    hands[i] -= 4
                    break

        next_valid_actions = self.get_valid_actions(hands)
        self.state["hands"] = hands
        self.state["valid_actions"] = next_valid_actions
        reward = self.evaluate_state(hands, prev_hands)
        done = sum(hands) == 0 and self.has_valid_yaku(hands)  # 只有有役才能結束
        return self.state, reward, done


class RLAgent:
    def __init__(self, action_space):
        self.q_table = {}
        self.actions = action_space
        self.learning_rate = 0.1
        self.discount_factor = 0.8
        self.epsilon = 1.0

    def choose_action(self, state):
        valid_actions = state["valid_actions"]
        state_key = self.get_state_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in self.actions}

        for action in valid_actions:
            if action not in self.q_table[state_key]:
                self.q_table[state_key][action] = 0

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_actions)
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def learn(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in self.actions}
        for a in state["valid_actions"]:
            if a not in self.q_table[state_key]:
                self.q_table[state_key][a] = 0

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0 for a in self.actions}
        for a in next_state["valid_actions"]:
            if a not in self.q_table[next_state_key]:
                self.q_table[next_state_key][a] = 0

        q_predict = self.q_table[state_key][action]
        q_target = reward + self.discount_factor * max(self.q_table[next_state_key].values(), default=0)
        self.q_table[state_key][action] += self.learning_rate * (q_target - q_predict)

    def get_state_key(self, state):
        return tuple(state["hands"])


def train_agent():
    env = ChiPongKongEnvironment()
    agent = RLAgent(action_space=["chi", "pong", "kong", "skip"])
    episodes = 1000
    total_reward = 0

    for episode in range(episodes):
        state = env.initialize_state()
        done = False
        steps = 0

        while not done and steps < 100:
            valid_actions = state["valid_actions"]
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            steps += 1

        # 動態調整 epsilon
        agent.epsilon = max(0.01, agent.epsilon * 0.995)

        # 動態調整學習率
        agent.learning_rate = max(0.01, agent.learning_rate * 0.995)

        if episode % 100 == 0:
            avg_reward = total_reward / (episode + 1)
            print(f"Episode {episode}: Total Reward = {total_reward:.2f}, Avg Reward = {avg_reward:.2f}")


if __name__ == "__main__":
    train_agent()
