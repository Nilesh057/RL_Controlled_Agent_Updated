import os
import pickle
import random

class QLearningAgent:
    def __init__(self, actions, alpha=0.2, gamma=0.9, epsilon=0.2, q_path="data/q_table.pkl"):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_path = q_path
        self.q = {}
        self.load_q_table(q_path)

    def _ensure_state(self, state):
        if state not in self.q:
            self.q[state] = {a: 0.0 for a in self.actions}

    def select_action(self, state):
        self._ensure_state(state)
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return max(self.q[state], key=self.q[state].get)

    def update_q_table(self, state, action, reward, next_state):
        self._ensure_state(state)
        self._ensure_state(next_state)
        old = self.q[state][action]
        next_max = max(self.q[next_state].values()) if self.q[next_state] else 0.0
        new = old + self.alpha * (reward + self.gamma * next_max - old)
        self.q[state][action] = new

    def top_actions(self, state, k=2):
        """Get top k actions for a given state, sorted by Q-value"""
        self._ensure_state(state)
        return sorted(self.q[state].items(), key=lambda kv: kv[1], reverse=True)[:k]
    
    def get_next_best_action(self, state):
        """Get the next best action suggestion (second highest Q-value)"""
        top_actions = self.top_actions(state, k=2)
        if len(top_actions) >= 2:
            return top_actions[1][0]  # Second best action
        elif len(top_actions) == 1:
            return top_actions[0][0]  # Only one action available
        else:
            return random.choice(self.actions)  # Fallback to random
    
    def get_action_confidence(self, state, action):
        """Get confidence score for a specific state-action pair"""
        self._ensure_state(state)
        max_q = max(self.q[state].values()) if self.q[state] else 0
        min_q = min(self.q[state].values()) if self.q[state] else 0
        action_q = self.q[state].get(action, 0)
        
        if max_q == min_q:
            return 0.5  # Neutral confidence when all actions have same Q-value
        
        # Normalize confidence between 0 and 1
        confidence = (action_q - min_q) / (max_q - min_q) if max_q != min_q else 0.5
        return round(confidence, 2)

    def save_q_table(self, path=None):
        path = path or self.q_path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.q, f)

    def load_q_table(self, path=None):
        path = path or self.q_path
        if os.path.exists(path):
            with open(path, "rb") as f:
                self.q = pickle.load(f)
