import pygame
import sys
import logging
from datetime import datetime

from music_generator import *
from hitl_rl_agent import *

# Initialize the mixer module
pygame.mixer.init()
pygame.font.init()

# Button Class
class Button:
    """
    A class to represent a button in the GUI.
    """
    def __init__(self, x, y, text, border=1):
        """
        Initialize the Button object.

        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            text (str): The text content of the button.
            border (int, optional): The border width of the button. Defaults to 1.
        """
        self.x = x
        self.y = y
        self.text = text
        self.content = font.render("  " + self.text + " ", True, [WHITE] * 3)
        self.width = self.content.get_width() + 4
        self.height = self.content.get_height() + 2
        self.border = border
        self.inner_colour = BLACK
        
    def draw(self, screen):
        """
        Draw the button on the screen.

        Args:
            screen: The Pygame screen to draw on.
        """
        pygame.draw.rect(screen, [WHITE] * 3, (self.x - self.border, self.y - self.border, self.width + 2 * self.border, self.height + 2 * self.border))
        pygame.draw.rect(screen, [self.inner_colour] * 3, (self.x, self.y, self.width, self.height - 1))
        screen.blit(self.content, (self.x, self.y))

    def hovered(self, x, y):
        """
        Check if the mouse is hovering over the button.

        Args:
            x (int): The x-coordinate of the mouse.
            y (int): The y-coordinate of the mouse.

        Returns:
            bool: True if the mouse is hovering over the button, False otherwise.
        """
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.inner_colour = GREY
            return True
        self.inner_colour = BLACK
        return False

    def rerender(self):
        """
        Rerender the button's content.
        """
        self.content = font.render("  " + self.text + " ", True, [WHITE] * 3)
        self.width = self.content.get_width() + 4
        self.height = self.content.get_height() + 2

# Input Class
class IntInput(Button):
    """
    A class to represent an input field for integer values.
    """
    def __init__(self, x, y, text, width, label, border=1):
        """
        Initialize the IntInput object.

        Args:
            x (int): The x-coordinate of the input field.
            y (int): The y-coordinate of the input field.
            text (str): The text content of the input field.
            width (int): The width of the input field.
            label (str): The label for the input field.
            border (int, optional): The border width of the input field. Defaults to 1.
        """
        super().__init__(x, y, text, border)
        self.width = width
        self.typing = False
        self.label = font.render(label, True, [WHITE] * 3)

    def rerender(self):
        """
        Rerender the input field's content and adjust width if needed.
        """
        saved_width = self.width
        super().rerender()
        if self.width > saved_width:
            self.text = self.text[:-1]
            self.rerender()
        self.width = saved_width
    
    def hovered(self, x, y):
        """
        Check if the mouse is hovering over the input field.

        Args:
            x (int): The x-coordinate of the mouse.
            y (int): The y-coordinate of the mouse.

        Returns:
            bool: True if the mouse is hovering over the input field, False otherwise.
        """
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            self.inner_colour = GREY
            return True

        if not self.typing:
            self.inner_colour = BLACK
        return False

    def draw(self, screen):
        """
        Draw the input field on the screen.

        Args:
            screen: The Pygame screen to draw on.
        """
        super().draw(screen)
        screen.blit(self.label, (self.x - self.label.get_width() - self.border - 5, self.y))


# Function to display episode and step information
def display_episode_step(episode, step):
    episode_step_text = font.render(f"Playing: Episode {episode}, Step {step}.", True, [WHITE] * 3)
    screen.blit(episode_step_text, (180, 250))

    waiting_text = font.render(f"Enter User Rating and Press 'Next Track'.", True, [WHITE] * 3)
    screen.blit(waiting_text, (132, 265))

# Define constants
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

LINE_THICKNESS = 3
LINE_GAP = 30

PADDING = 100
GREY = 175
BLACK = 18
WHITE = 255

# MIDI settings
user_id = '000000'
base_note = 60
tempo = 90
volume = 90
chord_freq = 4
track_array_length = 8

# RL settings
total_episodes = 10

scale_type = 'major'
chords_flag = False
percussion_flag = True

# Create fonts
font = pygame.font.SysFont("Helvetica", 12)
font2 = pygame.font.SysFont("Consolas", 90)

hash_sym = font.render("#", True, [WHITE] * 3)

# Text flip dictionaries
op_chords = {
    "Chords: On": "Chords: Off",
    "Chords: Off": "Chords: On"
}
op_percussion = {
    "Percussion: On": "Percussion: Off",
    "Percussion: Off": "Percussion: On"
}
op_scale = {
    "Scale: Major": "Scale: Minor",
    "Scale: Minor": "Scale: Major",
}

# Button settings
BUTTON_PADDING = 20
Y_PADDING = 10
X_PADDING = 10
INPUT_WIDTH = 30
TEXT_PADDING = 80

# Create buttons
buttonStartNew = Button(90 + X_PADDING, 200 + Y_PADDING, "Start New")
buttonNextTrack = Button(buttonStartNew.x + buttonStartNew.width + 125, 290 + Y_PADDING, "Next Track")
buttonChords = Button(90 + X_PADDING, Y_PADDING + 50, "Chords: Off")
buttonPercussion = Button(buttonChords.x + buttonChords.width + BUTTON_PADDING, Y_PADDING + 50, "Percussion: On")
buttonScale = Button(buttonPercussion.x + buttonPercussion.width + BUTTON_PADDING, Y_PADDING + 50, "Scale: Major")

inputs = [
    IntInput(buttonStartNew.x + buttonStartNew.width + TEXT_PADDING + 100 - 50, 200 + Y_PADDING, str(user_id), INPUT_WIDTH + 70, "User ID:"),
    IntInput(buttonStartNew.x + TEXT_PADDING + 50, 290 + Y_PADDING, "", INPUT_WIDTH, "User Rating (0-9):"),
    IntInput(X_PADDING + TEXT_PADDING, 125 + Y_PADDING, str(base_note), INPUT_WIDTH, "Base Note: "),
    IntInput(110 + TEXT_PADDING, 125 + Y_PADDING, str(tempo), INPUT_WIDTH, "Tempo: "),
    IntInput(210 + TEXT_PADDING, 125 + Y_PADDING, str(volume), INPUT_WIDTH, "Volume: "),
    IntInput(375 + TEXT_PADDING, 125 + Y_PADDING, str(track_array_length), INPUT_WIDTH, "Track Array Length: "),
    IntInput(buttonChords.x, 85 + Y_PADDING, str(chord_freq), INPUT_WIDTH, "Chord Freq: ")
]

# Music playback state
waiting = False
reward = None

clock = pygame.time.Clock()

# Main loop
while True:
    pressed_keys = []
    k = pygame.key.get_pressed()
    mouse_pressed = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.unicode in list("1234567890"):
                pressed_keys.append(event.unicode)
            elif event.key == pygame.K_BACKSPACE:
                pressed_keys.append("back")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

    # Clear the screen
    screen.fill([BLACK] * 3)

    # Draw buttons
    for button in [buttonStartNew, buttonNextTrack, buttonChords, buttonScale, buttonPercussion]:
        button.draw(screen)

    for i, input in enumerate(inputs):
        if i == len(inputs)-1 and not chords_flag:
            continue
        input.draw(screen)

    # Check if StartNew button hovered/clicked
    if buttonStartNew.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        if inputs[0].text != "":
            user_id = inputs[0].text
        if inputs[2].text != "":
            base_note = int(inputs[2].text)
        if inputs[3].text != "":
            tempo = int(inputs[3].text)
        if inputs[4].text != "":
            volume = int(inputs[4].text)
        if inputs[5].text != "":
            track_array_length = int(inputs[5].text)
        if inputs[6].text != "":
            chord_freq = int(inputs[6].text)

        episode = 0
        step = 0

        # Configure the logger
        current_datetime = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        log_filename = 'logs/hitl_rl_'+user_id+'_'+str(current_datetime)+'.log'
        logging.basicConfig(filename=log_filename, encoding='utf-8', format='%(name)s - %(levelname)s - %(message)s')
        logging.getLogger().setLevel(logging.DEBUG)

        # Reinforcement Learning loop
        logging.info(f'Starting new HITL RL model training with the following configuration:')
        logging.info(f'User ID: {user_id}')
        logging.info(f'Base Note: {base_note}')
        logging.info(f'Tempo: {tempo}')
        logging.info(f'Volume: {volume}')
        logging.info(f'Chord Frequency: {chord_freq}')
        logging.info(f'Track Array Length: {track_array_length}')
        logging.info(f'Scale Type: {scale_type}')
        logging.info(f'Chords toggle: {chords_flag}')
        logging.info(f'Percussion toggle: {percussion_flag}')

        # Load the music generator and the RL agent
        generator = MusicGenerator(base_note, scale_type, tempo, volume, chords_flag, percussion_flag, chord_freq, track_array_length)
        hitl_rl = HITL_RL_Agent(generator, learning_rate = 0.1, discount_factor = 0.9, initial_epsilon = 0.5, decay_rate = 0.01, log_filename=log_filename)
        track_array = generator.generate_random_track_array(array_length=track_array_length)
        
        modified_midi_path = f"midiFiles/modified_melody_ep_{episode}_step_{step}.mid"
        generator.generate_midi(modified_midi_path, track_array=track_array)

        # Stop the music so that the file is no longer open
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            ...

        pygame.mixer.music.load(modified_midi_path)
        pygame.mixer.music.play()

        waiting = True

    # Check if NextTrack button hovered/clicked
    if buttonNextTrack.hovered(*pygame.mouse.get_pos()) and mouse_pressed and not waiting:
        # Reset user rating input
        inputs[1].text = ""
        inputs[1].rerender()

        # Reinforcement Learning loop
        if step == 0:
            track_array = generator.generate_random_track_array(array_length=track_array_length)
        
        modified_midi_path = f"midiFiles/modified_melody_ep_{episode}_step_{step}.mid"
        generator.generate_midi(modified_midi_path, track_array=track_array)

        # Stop the music so that the file is no longer open
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            ...

        pygame.mixer.music.load(modified_midi_path)
        pygame.mixer.music.play()

        waiting = True

    # Check if toggle button hovered/clicked
    if buttonChords.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        buttonChords.text = op_chords[buttonChords.text]
        buttonChords.rerender()
        chords_flag = not chords_flag

    if buttonPercussion.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        buttonPercussion.text = op_percussion[buttonPercussion.text]
        buttonPercussion.rerender()
        percussion_flag = not percussion_flag

    if buttonScale.hovered(*pygame.mouse.get_pos()) and mouse_pressed:
        buttonScale.text = op_scale[buttonScale.text]
        buttonScale.rerender()
        scale_type = buttonScale.text.split(' ')[1].lower()
    
    for input in inputs:
        if input.hovered(*pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                input.text=""
                input.typing = True
                input.inner_colour = GREY
        elif pygame.mouse.get_pressed()[0]:
            input.typing = False
            input.inner_colour = BLACK
        
        if input.typing:
            for num in pressed_keys:
                if num == "back":
                    input.text = input.text[:-1]
                else:
                    input.text += num
                input.rerender()

    if waiting:
        display_episode_step(episode, step)
        if episode<total_episodes:
            try:
                # reward = random.randint(1, 10) # for code testing
                reward = int(inputs[1].text)
            except:
                ...

            if reward:
                logging.info(f'Track array for episode {episode}, step {step}: {track_array}')
                logging.info(f'User rating for episode {episode}, step {step}: {reward}')

                track_array = hitl_rl.update_q(track_array, reward, episode)

                step += 1

                if step >= track_array_length:
                    logging.info(f'EPISODE {episode} OF RL LOOP COMPLETE!')
                    step = 0
                    episode += 1

                waiting = False
                reward = None
        else:
            logging.info(f'RL LOOP COMPLETE!')
            waiting = False
            reward = None
            hitl_rl.log_q_table()
            hitl_rl.save_q_table(user_id)
            hitl_rl.load_q_table(user_id)

    # Update the screen
    pygame.display.flip()
    clock.tick(30)  # Limit frame rate to 30 FPS