import random
from midiutil import MIDIFile

class MusicGenerator:
    """
    A class for generating MIDI melodies with various options.

    Attributes:
        note_options (range): Range of available MIDI note pitches.
        scale_type_options (list): List of available scale types.
        percussion_channel (int): MIDI channel used for percussion.
        duration_options (list): List of available note durations.
        percussion_options (list): List of available percussion pitches.
    """

    def __init__(self, base_note=60, scale_type="major", tempo=90, volume=100, chords=False, chord_freq=2, array_length=8):
        """
        Initializes a MelodyGenerator instance.

        Args:
            base_note (int): Base MIDI note pitch.
            scale_type (str): Type of scale to use.
            tempo (int): Tempo in BPM.
            volume (int): MIDI volume level.
            chords (bool): Whether to include chords.
            chord_freq (int): Frequency of chord inclusion.
            array_length (int): Length of the track array.
        """
        self.note_options = range(60, 96)  # C4 to C7
        self.scale_type_options = ['major', 'minor', 'blues_minor', 'blues_major', 'diatonic_major_hexatonic']
        self.percussion_channel = 9  # Channel 9 is typically used for percussion
        self.duration_options = [0.25, 0.5, 0.75, 1]  # Add more durations if needed [1.5, 2, 3, 4]
        self.percussion_options = [38, 35] #, 42, 46, 49, 50, 45, 39, 36, 51]
        self.base_note = base_note
        self.scale_type = scale_type
        self.tempo = tempo
        self.volume = volume
        self.chords = chords
        self.chord_freq = chord_freq
        self.array_length = array_length
        self.scale = self._generate_scale(base_note, scale_type)

    def generate_midi(self, midi_path, track_array=None):
        """
        Generates a MIDI file with the provided track array.

        Args:
            midi_path (str): Path to save the generated MIDI file.
            track_array (list): Randomly generated array of [note_pitch, note_duration, percussion_pitch].
        """
        if not track_array:
            track_array = self.generate_random_track_array(self.array_length)

        t = 0
        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(track=0, time=t, tempo=self.tempo)

        for note_pitch, note_duration, percussion_pitch in track_array:
            # Add note
            MyMIDI.addNote(track=0, channel=0, pitch=note_pitch, time=t, duration=note_duration, volume=self.volume)

            # Add percussion
            MyMIDI.addNote(0, self.percussion_channel, percussion_pitch, t, 0.25, 100)

            # Add chords
            if self.chords and (t % self.chord_freq == 0):
                chord_pitches = self._get_chord_pitches(note_pitch, self.scale_type)
                volume_diff_for_chords = 10
                for chord_pitch in chord_pitches:
                    MyMIDI.addNote(track=0, channel=1, pitch=chord_pitch, time=t, duration=self.chord_freq, volume=(self.volume - volume_diff_for_chords))

            # Update time
            t += note_duration

        with open(midi_path, "wb") as output_file:
            MyMIDI.writeFile(output_file)

    def generate_random_track_array(self, array_length):
        """
        Generates a random track array.

        Args:
            array_length (int): Length of the track array.

        Returns:
            list: Randomly generated array of [note_pitch, note_duration, percussion_pitch].
        """
        return [[random.choice(self.scale), random.choice(self.duration_options), random.choice(self.percussion_options)] for _ in range(array_length)]

    def apply_action(self, track_array, action):
        """
        Applies a given action to the track array.

        Args:
            track_array (list): Melody track array to modify.
            action (tuple): Action to apply.
                - action_type (int): Type of action.
                - index (int): Index of the element to modify.
                - value (int/float): New value for the element.
        """
        action_type, index, value = action

        if action_type == 0:  # Change pitch
            track_array[index][0] = value
        elif action_type == 1:  # Change duration
            track_array[index][1] = value
        elif action_type == 2:  # Change percussion pitch
            track_array[index][2] = value
        elif action_type == 3:  # Remove a note
            track_array.pop(index)

    def _generate_scale(self, base_note=60, scale_type='major'):
        """
        Generates a scale based on the given parameters.

        Args:
            base_note (int): Base MIDI note pitch.
            scale_type (str): Type of scale to generate.

        Returns:
            list: List of MIDI note pitches representing the scale.
        """
        intervals = {
            'major': [0, 2, 4, 5, 7, 9, 11, 12],
            'minor': [0, 2, 3, 5, 7, 8, 10, 12],
            'blues_minor': [0, 3, 5, 8, 10, 12],
            'blues_major': [0, 2, 5, 7, 9, 12],
            'diatonic_major_hexatonic': [0, 3, 6, 9, 12, 15, 18]
        }
        if scale_type in intervals:
            return [base_note + interval for interval in intervals[scale_type]]
        else:
            print('Invalid scale_type. scale_type defaulting to "major"')
            return [base_note + interval for interval in intervals['major']]

    def _get_chord_pitches(self, pitch, chord_type):
        """
        Gets the pitches of a chord based on the given pitch and chord type.

        Args:
            pitch (int): Root pitch of the chord.
            chord_type (str): Type of chord.

        Returns:
            list: List of MIDI note pitches representing the chord.
        """
        intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6]
        }
        return [pitch + interval for interval in intervals.get(chord_type, [])]
