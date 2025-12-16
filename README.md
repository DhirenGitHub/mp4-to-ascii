# Bad Apple ASCII Video Player

A Python-based ASCII video player inspired by the legendary "Bad Apple!!" music video meme. Convert any video into glorious ASCII art and play it right in your terminal with synchronized audio!

## Features

- **Video to ASCII Conversion**: Converts video frames into ASCII art using grayscale mapping
- **Audio Support**: Extracts and plays audio synchronized with the ASCII video
- **Frame Skipping**: Configurable frame skipping for faster processing and playback
- **Smart Caching**: Reuse previously processed videos without re-rendering
- **Customizable Width**: Adjust ASCII art resolution to fit your terminal
- **Real-time Playback**: Maintains proper frame rate for smooth playback

## Demo

Transform this:
<img width="1502" height="1127" alt="image" src="https://github.com/user-attachments/assets/c4ee9e77-6242-4579-8466-437515d344b5" />

Into this:

<img width="662" height="497" alt="image" src="https://github.com/user-attachments/assets/70da3e5f-1a38-4943-9701-3cac5245b522" />


## Requirements

- Python 3.6+
- OpenCV (cv2)
- ffmpeg (for audio extraction)

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
```bash
pip install opencv-python
```

3. **Install ffmpeg:**

   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**:
     ```bash
     brew install ffmpeg
     ```
   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt install ffmpeg
     ```

## Usage

### Basic Usage

Simply run the script:
```bash
python main.py
```

The script will guide you through the process:

1. **First time running** - You'll be prompted for:
   - Path to your video file
   - ASCII width (default: 100 characters)

2. **Subsequent runs** - If processed files exist:
   - Press Enter to replay the existing video instantly
   - Type `y` to process a new video

### Configuration

Edit these constants at the top of `main.py`:

```python
# ASCII characters from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "

# Frame skipping: Process every nth frame (1 = all frames, 3 = every 3rd frame)
FRAME_SKIP = 1
```

- **`ASCII_CHARS`**: Characters used for rendering (darkest to lightest)
- **`FRAME_SKIP`**: Process every Nth frame (higher = faster processing, lower quality)

### Example Workflow

```bash
$ python main.py

ASCII Video Player
==================================================

Enter the path to your video file: bad_apple.mp4
Enter ASCII width in characters (default 100): 120

==================================================
Step 1: Extracting frames from video...
==================================================

Video Properties:
  FPS: 30.00
  Total Frames: 6570
  Duration: 219.00 seconds
  Extracting every 1 frame(s)...

[Processing happens...]

Press any key to start...
```

## How It Works

1. **Frame Extraction**: Uses OpenCV to extract frames from your video
2. **Audio Extraction**: Uses ffmpeg to extract audio as MP3
3. **ASCII Conversion**:
   - Converts each frame to grayscale
   - Resizes to specified width (maintains aspect ratio)
   - Maps pixel brightness to ASCII characters
4. **Playback**:
   - Displays ASCII frames in terminal using ANSI escape codes
   - Plays audio in background thread for synchronization

## File Structure

After processing, you'll have:
```
bad-apple/
├── main.py           # Main script
├── README.md         # This file
├── frames/           # Extracted video frames (temporary)
├── ascii_frames/     # ASCII text files (cached)
└── audio.mp3         # Extracted audio (cached)
```

## Tips & Tricks

- **Terminal Size**: Make your terminal fullscreen for the best experience
- **ASCII Width**:
  - 80-100: Good for small terminals
  - 120-150: Better detail for larger terminals
  - 200+: Maximum detail (requires very wide terminal)
- **Frame Skip**:
  - `FRAME_SKIP = 1`: Best quality, slower processing
  - `FRAME_SKIP = 2-3`: Good balance
  - `FRAME_SKIP = 5+`: Fast processing, choppy playback
- **Font**: Use a monospace font for proper ASCII alignment

## Troubleshooting

### Audio not playing
- Ensure ffmpeg is installed and in your PATH
- The script will continue without audio if ffmpeg is unavailable

### Terminal too small
- Reduce the ASCII width when prompted
- Make your terminal window larger or fullscreen

### Slow playback
- Increase `FRAME_SKIP` to reduce frame count
- Use a smaller ASCII width
- Close other applications

### Video won't open
- Ensure the video path is correct
- Supported formats: MP4, AVI, MOV, and other OpenCV-compatible formats

## Credits

Inspired by the "Bad Apple!!" Touhou music video and the countless ASCII art renditions that followed.

## License

Free to use, modify, and share. Have fun!

## Contributing

Feel free to fork, improve, and share your own versions. Suggestions and improvements are welcome!

