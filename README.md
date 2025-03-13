# Midi2Vid - Simple and Fast Midi to Video Converter

Midi to video converter. This program renders the notes of a midi file to a
video. The renderer is built on top of the pygame library and uses multiple
processes to generate the frames of the video. It then uses ffmpeg to convert
the frames to a video. It also uses the fluidsynth library to render the midi
file to a wav file.

![Example](https://raw.githubusercontent.com/oscaraandersson/midi2vid/main/assets/midi2vid.jpg)

## Installation
Install from github using pip:
```bash
pip install midi2vid
```

Build with docker:
```bash
docker build -t midi2vid-base .
docker run --rm -v $(pwd):/app midi2vid-base -i midi2vid/data/example.mid -o your_output.mp4
```

Build from source:
```bash
git clone https://github.com/pianoviz/midi2vid.git
cd midi2vid
pip install -e .
```

## Usage
```bash
midi2vid -i <input_midi_file> -o <output_video_file>
```

**Options**

```bash
-i, --input: Input midi file
-o, --output: Output video file
--config: Path to the configuration file (default: default.json)
```

**Example**

There is an example midi file in the `data` directory. You can run the following
command to generate a video from the example midi file:
```bash
midi2vid -i midi2vid/data/example.mid -o example.mp4
```

## Configuration

The configuration file is a JSON file that specifies various parameters for the
video generation. Here is an example configuration file:

```json
{
  "soundfont_path": "data/soundfont.sf2",
  "max_note_length": 50,
  "n_processors": 4,
  "screen_width": 1920,
  "screen_height": 1080,
  "bpm": 120,
  "fps": 30,
  "speed": 200,
  "white_note_color": [255, 255, 255],
  "black_note_color": [49, 49, 49],
  "background_color": [43, 43, 43],
  "octave_lines_color": [92, 92, 92],
  "note_color": [179, 44, 49],
  "dark_note_color": [113, 34, 36],
  "right_note_color": [168, 255, 145],
  "left_note_color": [176, 202, 229],
  "dark_right_note_color": [118, 208, 68],
  "dark_left_note_color": [124, 142, 151],
  "estimate_hands": false
}
```

The `estimate_hands` parameter is experimental and is used to estimate the hand
positions based on the notes played. It is currently under development and may
not work as expected.


## Dependencies
- pygame
- ffmpeg
- fluidsynth

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on
GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.

