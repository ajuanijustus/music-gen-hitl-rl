import random
import copy
import logging
import tensorflow as tf
from tensorflow.keras import layers

# Configure the logger
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)

class HITL_RL_Agent:
    """
    An Agent that uses Human-in-the-Loop Reinforcement Learning to modify melodies.
    """

    def __init__(self, generator, total_episodes, learning_rate, discount_factor):
        """
        Initialize the HITL_RL_Agent.

        Args:
            generator: The melody generator.
            total_episodes: The total number of episodes to run.
            learning_rate: The learning rate for Q-learning updates.
            discount_factor: The discount factor for future rewards in Q-learning.
        """
        self.generator = generator
        self.total_episodes = total_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = {}
        
    def update_q(self, track_array, reward):
        """
        Ran over multiple episodes and step to for the HITL_RL_Agent to update q table and modify melodies.
        """
        state = tuple(tuple(note) for note in track_array)
        action = (
            random.randint(0, 2),
            random.randint(0, len(track_array) - 1),
            random.choice(self.generator.note_options),
            random.choice(self.generator.percussion_options),
            random.choice(self.generator.duration_options),
        )

        logging.info(f'Random action: {action}')
        
        new_track_array = copy.deepcopy(track_array)
        self.generator.apply_action(new_track_array, action)
        new_state = tuple(tuple(note) for note in new_track_array)

        # Q-Learning
        current_q = self.q_table.get((state, action), 0)
        max_next_q = max(
            [self.q_table.get((new_state, a), 0) for a in range(5)]
        )
        updated_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        self.q_table[(state, action)] = updated_q

        logging.info(f'Updated Q: {updated_q}')

        return new_track_array

    def select_best_action_using_ai(self, state):
        # Convert the state to a suitable format (e.g., flatten the tuple of tuples)
        state_array = np.array(state).flatten()

        # Use the trained AI model to predict the action probabilities
        action_probabilities = self.ai_model.predict(np.array([state_array]))[0]

        # Select the action with the highest probability
        selected_action = np.argmax(action_probabilities)
        return selected_action

    def train_ai_model(self, X, y, num_epochs=10):
        # Define and train the AI model
        self.ai_model = tf.keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(len(X[0]),)),
            layers.Dense(64, activation='relu'),
            layers.Dense(5, activation='softmax')  # 5 actions in this example
        ])

        self.ai_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.ai_model.fit(np.array(X), np.array(y), epochs=num_epochs)