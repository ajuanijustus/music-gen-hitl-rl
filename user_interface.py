from midi2audio import FluidSynth

class UserInterface:
    """
    A simple user interface for playing melodies and collecting feedback.
    """

    def __init__(self, soundfont_path='GeneralUser GS v1.471.sf2'):
        """
        Initialize the UserInterface.

        Args:
            soundfont_path (str): Path to the soundfont file.
        """
        self.soundfont_path = soundfont_path
        
    def play_melody(self, midi_path):
        """
        Play a melody from a MIDI file using FluidSynth.

        Args:
            midi_path (str): Path to the MIDI file to be played.
        """
        fs = FluidSynth(self.soundfont_path)
        fs.play_midi(midi_path)

    def collect_feedback(self):
        """
        Collect feedback from the user by prompting them to rate a generated melody.

        Returns:
            int: The user's rating, ranging from 1 to 10.
        """
        while True:
            try:
                rating = int(input("Rate the generated melody (1-10): "))
                if 1 <= rating <= 10:
                    return rating
                else:
                    print("Please enter a rating between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 10.")
