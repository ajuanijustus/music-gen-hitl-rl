from user_interface import *
from music_generator import *
from hitl_rl_agent import *

generator = MusicGenerator(tempo = 120)
ui = UserInterface(soundfont_path='soundfont/GeneralUser GS v1.471.sf2')
hitl_rl = HITL_RL_Agent(generator, ui, total_episodes = 10, learning_rate = 0.1, discount_factor = 0.9)
hitl_rl.run()

# ui.play_melody('midiFiles/modified_melody_9.mid')
