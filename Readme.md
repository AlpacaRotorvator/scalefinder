# scalefinder

Finding scales(and keys) in MIDI files.

# Requirements

* numpy
* scipy
* mido
* scales.xml file from Tuxguitar(see below)

# Installation

Before using the module either download `scales.xml` from [Tuxguitar repositories](https://sourceforge.net/p/tuxguitar/code/HEAD/tree/trunk/TuxGuitar/share/scales/scales.xml?format=raw) or copy from an existing installation. Drop it into a subfolder named `res`.

# Usage

```
from scalefinder import scaleFinder

song = scaleFinder('./smp/Gscale.mid')
res = song.analyse()
res[0:10]
```

Should analyse the sample G major scale and return a slice of the resulting list of tuples containing the 10 best matches, along with their respective scores.

By default the module uses an optimization that expects the tonic of a scale to be slightly more frequent than other notes. This works great for real, western tonal tradition, pieces but causes the G major scale to appear only as the 8th best match for this particular sample. To disable the optimization use:

```
song = scaleFinder('./smp/Gscale.mid', tonal=False)
```

Now the G major scale should be at the top, but the module can't distinguish between G major and its minor relative, E minor, anymore.

Other possible options include:

* passing a custom `metric` to the constructor. The default one is `scipy.spatial.distance.correlation`.
* passing a list of `channels` to `analyse`(or `midiprep`) will cause the module to only listen for note on events in those MIDI channels. The default is channels 0 through 15.
* `noteSlice` to `analyse`(or `midiprep`), a 2-element list `[a,b]` that causes the analysis to skip the first `a` note on events and stop after the `b`th event. Defaults to the whole midi file.


# Samples

This module currently ships with the following samples in the `smp` subfolder:

* `Gscale.mid`: a G Major Scale.
