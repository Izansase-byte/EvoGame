# EvoGame

An evolution simulator built with Python and Pygame

Watch creatures search for food, consume energy and reproduce. Offspring inherit their parent's speed and vision range, with possible mutations that allow population to evolve over time.

## Features

- Creatures with individual energy, speed, and vision.
- Reproduction with inherited traits and mutations.
- Seasons that change environmental conditions.
- Laboratory mode to adjust simulation parameters.
- Population, average speed, and average vision charts.
speed and vision distribution histograms.
- Save and load experiments.
- Export simulation statistics to CSV.
- Random seed for reproducible experiments

## Installation 

Requires Python 3.10 or newer.

1. Clone the repository:

```bash
git clone https://github.com/Izansase-byte/EvoGame.git
cd EvoGame
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate it:
**MacOS/Linux**
```bash
sourche .venv/bin/activate
```

**Windows**
```powershell
.venv\Scripts\Activate.ps1
```

4. Install Pygame CE:

```bash
python -m pip install pygame-ce
```

5. Run the simulator:

```bash
python main.py
```

## Controls

|Key/Action|Function|
|---|---|
| Space |Pause or resume the simulation |
| Tab | Open or close the laboratory |
| R | Restart using the same seed|
| 1 / 2 / 3 | Set simulation speed to 1x / 2x / 5x|
| Up / Down | Increase or decrease food spawn rate |
| Left click | Add food on the cursor |
| Right click on a creature | Inspect its traits and vision range |
| H | Show or hide the information panel |
| G | Show or hide the history chart |
| V | Cycle through population, average speed, and average vision charts |
| B | Cycle through speed histogram, vision histogram, and hidden |
| S | Save the current experiment |
| L | Load the last saved experiments |
| E | Export statistics to CSV |

The simulation pauses while the laboratory is open. if you passed manually, press Space to resume.

Loaded experiments start paused. Press Space to continue.

## How it works

Creatures search for the closest food within their vision range. Eating restores energy, whili moving consumes it. Higher speed and a wider vision range increase energy costs.

When a creaturre has enough energy. It reproduces and shares its energy with its offsprimgs.
Offspring inherit speed and vision, with random mutations controlled by the mutation rate.

Creatures die when they run out of energy. Over generations, the populatios traits may change depending on food availabilty and environmental conditions.

## Laboratory

Press Tab to open the laboratory and adjust:

- Mutation rate.
- Energy consumption multiplier.
- Food spawn rate.
- Seasons and their duration.

Presets let you explore abundant food, scarce food, and high mutation rate.

You can also choose a random seed and restart the experiment. Restarting clears the current population and statistics.

## Saving and Exporting

Press S to save the current experiment to `saves/last.json`. Saving again overwrites this file.

Press L to restore it. Loaded experiments start paused.

Press E to export statistics to a timestamped CSV file in `exports/`. CSV exports contain statistics for analysis; use JSON saves to resume an experiment.