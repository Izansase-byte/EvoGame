# EvoGame

An evolution simulator built with Python and Pygame CE.

Watch creatures search for food, consume energy, and reproduce. Offspring inherit their parent's speed and vision range, with possible mutations that allow the population to evolve over time.

## Features

- Creatures with individual energy, speed, and vision.
- Reproduction with inherited traits and mutations.
- Seasons that change environmental conditions.
- Laboratory mode to adjust simulation parameters.
- Population, average speed, and average vision charts.
- Speed and vision distribution histograms.
- Recent event log for births, deaths, season changes, and extinction.
- Save and load experiments, including their event logs.
- Export simulation statistics to CSV.
- Random seeds for reproducible experiments.

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

   On macOS or Linux, use `python3` if `python` is unavailable.

3. Activate it:

   **macOS / Linux**

   ```bash
   source .venv/bin/activate
   ```

   **Windows (PowerShell)**

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

| Key / Action | Function |
| --- | --- |
| Space | Pause or resume the simulation |
| Tab | Open or close the laboratory |
| R | Restart using the same seed |
| 1 / 2 / 3 | Set simulation speed to 1x / 2x / 5x |
| Up / Down | Increase or decrease food spawn rate |
| Left click | Add food at the cursor |
| Right click on a creature | Inspect its traits and vision range |
| H | Show or hide the information panel |
| G | Show or hide the history chart |
| V | Cycle through population, average speed, and average vision charts |
| B | Cycle through speed histogram, vision histogram, and hidden |
| N | Show or hide the recent event log |
| S | Save the current experiment |
| L | Load the last saved experiment |
| E | Export statistics to CSV |

The simulation pauses while the laboratory is open. Close it with Tab to continue. If you paused manually, press Space to resume.

Loaded experiments start paused. Press Space to continue.

## How It Works

Creatures search for the closest food within their vision range. Eating restores energy, while moving consumes it. Higher speed and a wider vision range increase energy costs.

When a creature has enough energy, it reproduces and shares its energy with its offspring. Offspring inherit speed and vision, with random mutations controlled by the mutation rate.

Creatures die when they run out of energy. Over generations, the population's traits may change depending on food availability and environmental conditions.

## Laboratory

Press Tab to open the laboratory and adjust:

- Mutation rate.
- Energy consumption multiplier.
- Food spawn rate.
- Seasons and their duration.

Presets let you explore abundant food, scarce food, and high mutation rates. They preserve the population and disable automatic seasons.

You can also choose a random seed and restart the experiment. Restarting clears the current population, statistics, and event log.

## Saving and Exporting

Press S to save the current experiment to `saves/last.json`, including recent events. Saving again overwrites this file.

Press L to restore it. Loaded experiments start paused. Older saves without an event log load with an empty log.

Press E to export statistics to a timestamped CSV file in `exports/`. CSV exports contain statistics for analysis; use JSON saves to resume an experiment.

## macOS Download

Download `EvoGame-macOS-arm64.zip` from the [releases page](https://github.com/Izansase-byte/EvoGame/releases), extract it, and open `EvoGame.app`. This build is for Apple Silicon Macs; Python is not required. The app is not notarized by Apple.

The packaged app stores saves and CSV exports in `~/EvoGame/`. Running from source stores them next to `main.py`.

## Build and Test

```bash
python -m pip install pygame-ce pyinstaller
python -m unittest discover -v
python -m PyInstaller --noconfirm EvoGame.spec
```

The macOS app is created in `dist/EvoGame.app`.
