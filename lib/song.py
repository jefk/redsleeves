import sys
import re
import csv
from subprocess import Popen, PIPE

class Song:

    @classmethod
    def from_midi_path(cls, path):
        csv_data = Popen(['midicsv', path], stdout=PIPE).stdout.readlines()
        data = csv.reader(line.decode('utf8') for line in csv_data)
        return cls(data)

    def __init__(self, data):
        self.raw_data = data
        self._clean_data()
        self._initialize_notes()

    def _initialize_notes(self):
        self.notes = []
        for line in self.raw_data:
            if line[2] != 'Note_on_c':
                continue

            _, time, _, channel, note, velocity = line
            self.notes.append(
                {'time': time, 'channel': channel, 'note': note, 'velocity': velocity}
            )

    def _clean_data(self):
        self.raw_data = [self._strip_whitespace(line) for line in self.raw_data]

    def _strip_whitespace(self, line):
        return [x.strip() for x in line]


if __name__ == '__main__':
    song = Song.from_midi_path(sys.argv[1])
    [print(note) for note in song.notes]
