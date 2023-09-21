# Music Generation using Human-In-The-Loop Reinforcement Leanring

This repository contains the code base for my MSc Comp Sci dissertation that uses HITL RL to generate music.

## Abstract
This dissertation presents an approach that combines Human-In-The-Loop Reinforcement Learning (HITL RL) with principles derived from music theory to facilitate the real-time generation of musical compositions. HITL RL, previously employed in diverse applications such as modelling humanoid robot mechanics and enhancing language models, harnesses human feedback to refine training processes. In this study, we leverage constraints and principles grounded in music theory with the HITL RL framework, employing the Markov Decision Process and Greedy Epsilon Q-Learning Algorithm. The system generates musical tracks (compositions), continuously enhancing its quality through iterative human-in-the-loop feedback. The reward function for this process is the subjective musical taste of the user.

Keywords: Reinforcement Learning, Human-In-The-Loop, Music Generation, HITL RL, Algorithmic Music, Audio Machine Learning

## Usage

1. Clone this repository to your local machine.
2. Install the required dependencies using the provided `requirements.txt` file:
```pip install -r requirements.txt```
3. Run the `main_gui.py` script:
```python main_gui.py```
4. The GUI window will open, allowing you to configure settings for music generation and RL.
5. Click the "Start New" button to start the RL loop.
6. Play melodies and rate them using the GUI. The RL agent will learn from your ratings and modify the melodies accordingly.

## Files

- `music_generator.py`: Contains the MusicGenerator class for generating MIDI melodies.
- `hitl_rl_agent.py`: Contains the HITL_RL_Agent class for implementing Human-in-the-Loop Reinforcement Learning.
- `main_gui.py`: Implements the GUI interface using the Pygame library for user interaction.

## Author

Aju Ani Justus

## License

This project is licensed under the [MIT License](LICENSE).
