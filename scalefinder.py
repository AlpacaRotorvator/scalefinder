import xml.etree.ElementTree as ET
import scipy.spatial.distance as metrics
import numpy as np
import mido
import operator

class scaleFinder:
    def __init__(self, song=None, metric=metrics.correlation, tonal=True):
        self.tonal = tonal
        self.keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.scales = self.initScales()
        self.metric = metric
        self.setSong(song)

    def initScales(self):
        root = ET.parse('./res/scales.xml').getroot()
        scales = {}
        for child in root:
            if self.tonal:
                notes = np.array([0.25] + [0] * 11)
            else:
                notes = np.array([0] * 12)
            
            for i in child.attrib['keys'].split(','):
                notes[int(i) - 1] += 1

            notes = notes / notes.sum()
            
            scales[child.attrib['name']] = notes

            if child.attrib['name'] == "Diminished Arpeggio":
                break

        return scales

    def setSong(self, song):
        self.song = mido.MidiFile(song)
        
    def analyse(self, channels=range(15), noteSlice=None):
        notes = self.midiprep(channels, noteSlice)
        results = {}
        for scale in self.scales:
            for key in range(12):
                compat = self.metric(self.scales[scale], np.roll(notes, -key))
                results[self.keys[key] + ' ' + scale] = compat

        results = sorted(results.items(), key=operator.itemgetter(1))
        return results

    def midiprep(self, channels=range(15), noteSlice=None):      
        notes = np.array([0] * 12)
        
        if not noteSlice:
            noteSlice = [0, self.song.length]
        
        notesIn = 0
        noteCount = 0
        for msg in self.song:
            if msg.type == 'note_on':
                if noteCount < noteSlice[0]:
                    noteCount += 1
                    continue
                elif noteCount >= noteSlice[1]:
                    break
                elif msg.channel in channels:
                    notes[msg.note % 12] += 1
                    notesIn += 1
                    noteCount += 1

        notes = notes/notesIn
        return notes
