import random
import copy

class HITL_RL_Agent:
    """
    An Agent that uses Human-in-the-Loop Reinforcement Learning to modify melodies.
    """

    def __init__(self, generator, ui, total_episodes, learning_rate, discount_factor):
        """
        Initialize the HITL_RL_Agent.

        Args:
            generator: The melody generator.
            ui: The user interface for feedback collection and melody playback.
            total_episodes: The total number of episodes to run.
            learning_rate: The learning rate for Q-learning updates.
            discount_factor: The discount factor for future rewards in Q-learning.
        """
        self.generator = generator
        self.ui = ui
        self.total_episodes = total_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = {}
        
    def run(self):
        """
        Run the HITL_RL_Agent to modify melodies over multiple episodes.
        """
        for episode in range(self.total_episodes):
            track_array = self.generator.generate_random_track_array(array_length=8)

            # Reinforcement Learning loop
            for step in range(len(track_array)):
                modified_midi_path = f"midiFiles/modified_melody_ep_{episode}_step_{step}.mid"
                self.generator.generate_midi(modified_midi_path, track_array=track_array)
                self.ui.play_melody(modified_midi_path)

                reward = random.randint(1, 10)  # Simulated user feedback rating

                state = tuple(tuple(note) for note in track_array)
                action = (
                    random.randint(0, 3),
                    random.randint(0, len(track_array) - 1),
                    random.choice(self.generator.note_options),
                )
                
                new_track_array = copy.deepcopy(track_array)
                self.generator.apply_action(new_track_array, action)
                new_state = tuple(tuple(note) for note in new_track_array)

                # Q-learning update
                current_q = self.q_table.get((state, action), 0)
                max_next_q = max(
                    [self.q_table.get((new_state, a), 0) for a in range(5)]
                )
                updated_q = current_q + self.learning_rate * (
                    reward + self.discount_factor * max_next_q - current_q
                )
                self.q_table[(state, action)] = updated_q

                track_array = new_track_array

            # Save and play the modified melody at the end of the episode
            print(f"Final tune of episode {episode} playing 🎶")
            modified_midi_path = f"midiFiles/modified_melody_ep_{episode}.mid"
            self.generator.generate_midi(modified_midi_path, track_array=track_array)
            self.ui.play_melody(modified_midi_path)
