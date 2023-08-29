import random
import copy
import logging
import itertools

class HITL_RL_Agent:
    """
    An Agent that uses Human-in-the-Loop Reinforcement Learning to modify melodies.
    """

    def __init__(self, generator, learning_rate, discount_factor, initial_epsilon, decay_rate, log_filename):
        """
        Initialize the HITL_RL_Agent.
        
        Args:
            generator: The melody generator.
            learning_rate: The learning rate for Q-learning updates.
            discount_factor: The discount factor for future rewards in Q-learning.
            log_filename: The logger filename based on user_id and datetime.
        """
        self.generator = generator
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = {}
        self.initial_epsilon = initial_epsilon
        self.decay_rate = decay_rate

        # Configure the logger
        logging.basicConfig(filename=log_filename, encoding='utf-8', format='%(name)s - %(levelname)s - %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)

    def log_q_table():
        logging.info(f'Updated Q Table: {self.q_table}')
        
    def update_q(self, track_array, reward, episode_number):
        state = (tuple(tuple(note) for note in track_array[0]), tuple(track_array[1]))

        epsilon = self.initial_epsilon * (self.decay_rate ** episode_number)

        if random.random() < epsilon or episode_number<1:
            # Explore: Choose a random action
            action = (
                random.randint(0, 4),
                random.randint(0, len(track_array[0]) - 1)
            )
            logging.info(f'Selected random action: {action}')
        else:
            # Exploit: Choose the action with the highest Q-value for the current state
            # Filter for the best action from combination all possible actions for the state already explored, defaulting to (0,0) if not available
            best_action = max(
                [(a, self.q_table.get((state, a), 0)) for a in list(itertools.product(range(5), range(len(track_array[0]))))],
                key=lambda x: x[1]
            )[0]
            action = best_action
            logging.info(f'Selected best action: {action}')
        
        new_track_array = copy.deepcopy(track_array)
        self.generator.apply_action(new_track_array, action)
        new_state = tuple(tuple(note) for note in new_track_array)

        # Q-Learning
        current_q = self.q_table.get((state, action), 0)
        max_next_q = max(
                [(a, self.q_table.get((state, a), 0)) for a in list(itertools.product(range(5), range(len(track_array[0]))))],
                key=lambda x: x[1]
            )[1]
        updated_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = updated_q

        return new_track_array
