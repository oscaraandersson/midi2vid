# MIDI2VID

Midi to video converter. This program renders the notes of a midi file to a
video. The renderer is built on top of the [pygame](https://www.pygame.org/)
library and uses multiple processes to generate the frames of the video. It then
uses ffmpeg to convert the frames to a video. It also uses the fluidsynth
library to render the midi file to a wav file.

## Installation
Install from github using pip:
```bash
pip install git+https://github.com/pianoviz/midi2vid.git
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

## Options
```bash
-i, --input: Input midi file
-o, --output: Output video file
```

## Example
```bash
midi2vid -i example.mid -o example.mp4
```

## Dependencies
- [pygame](https://www.pygame.org/)
- [ffmpeg](https://ffmpeg.org/)
- [fluidsynth]()

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on
GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.

