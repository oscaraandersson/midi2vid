# Midi2Vid - Simple and Fast Midi to Video Converter

Midi to video converter. This program renders the notes of a midi file to a
video. The renderer is built on top of the pygame library and uses multiple
processes to generate the frames of the video. It then uses ffmpeg to convert
the frames to a video. It also uses the fluidsynth library to render the midi
file to a wav file.

![Example](https://raw.githubusercontent.com/oscaraandersson/midi2vid/main/assets/midi2vid.png)

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
midi2vid <input_midi_file> <output_video_file>
```

**Example**

There is an example midi file in the `data` directory. You can run the following
command to generate a video from the example midi file:
```bash
midi2vid -i midi2vid/data/example.mid out.mp4 --fps 60 --width 1920 --height 1080
```

## Configuration

| Argument                 | Description                                         | Default Value          |
|--------------------------|-----------------------------------------------------|------------------------|
| **Positional Arguments** |                                                     |                        |
| `input`                  | Input MIDI file path                                | N/A                    |
| `output`                 | Output video file path, optional                    | N/A                    |
| **Optional Arguments**   |                                                     |                        |
| `-i, --input`            | Input MIDI file path (overrides positional)         | N/A                    |
| `-o, --output`           | Output video file path (overrides positional)       | N/A                    |
| `--max-note-length`      | Maximum length of notes                             | `80`                   |
| `--n-processors`         | Number of processors to use                         | `4`                    |
| `--screen-width`         | Screen width in pixels                              | `1920`                 |
| `--screen-height`        | Screen height in pixels                             | `1080`                 |
| `--fps`                  | Frames per second                                   | `30`                   |
| `--speed`                | Note falling speed                                  | `300`                  |
| `--estimate-hands`       | Enable hand estimation                              | `True`                 |
| `--debug`                | Enable debug mode                                   | `False`                |
| **Colors**               |                                                     |                        |
| `--white-note-color`     | White note color as RGB                             | `255,255,255`          |
| `--black-note-color`     | Black note color as RGB                             | `49,49,49`             |
| `--background-color`     | Background color as RGB                             | `43,43,43`             |
| `--octave-lines-color`   | Octave lines color as RGB                           | `92,92,92`             |
| `--note-color`           | Note color as RGB                                   | `179,44,49`            |
| `--dark-note-color`      | Dark note color as RGB                              | `113,34,36`            |
| `--right-note-color`     | Right hand note color as RGB                        | `168,255,145`          |
| `--left-note-color`      | Left hand note color as RGB                         | `176,202,229`          |
| `--dark-right-note-color`| Dark right hand note color as RGB                   | `118,208,68`           |
| `--dark-left-note-color` | Dark left hand note color as RGB                    | `124,142,151`          |



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

