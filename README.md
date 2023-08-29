# Music Generation and Reinforcement Learning GUI

This repository contains a graphical user interface (GUI) application that combines music generation and reinforcement learning (RL) using the Pygame library.

## Prerequisites

- Python 3.x
- pygame library (`pip install pygame`)
- midiutil library (`pip install midiutil`)

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
