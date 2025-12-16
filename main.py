import cv2
import os
import time
import shutil
from pathlib import Path
import subprocess
import threading

ASCII_CHARS = "@%#*+=-:. "
FRAME_SKIP = 1

def extract_frames(video_path, output_folder='frames', frame_interval=1):
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return None, 0
    
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video Properties:")
    print(f"  FPS: {fps:.2f}")
    print(f"  Total Frames: {total_frames}")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  Extracting every {frame_interval} frame(s)...")
    print()
    
    frame_count = 0
    saved_count = 0
    
    while True:
        success, frame = video.read()
        
        if not success:
            break
        
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f'frame_{frame_count:06d}.jpg')
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            if saved_count % 100 == 0:
                print(f"Extracted {saved_count} frames...")
        
        frame_count += 1
    
    video.release()
    
    print(f"\nExtraction complete!")
    print(f"  Total frames processed: {frame_count}")
    print(f"  Frames saved: {saved_count}")
    print(f"  Output folder: {output_folder}")
    
    return fps, saved_count

def resize_frame(frame, new_width=100):
    height, width = frame.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    resized = cv2.resize(frame, (new_width, new_height))
    return resized

def frame_to_ascii(frame, width=100):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    resized = resize_frame(gray, width)
    
    ascii_frame = ""
    for row in resized:
        for pixel in row:
            ascii_index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
            ascii_frame += ASCII_CHARS[ascii_index]
        ascii_frame += "\n"
    
    return ascii_frame

def convert_frames_to_ascii(frames_folder='frames', ascii_folder='ascii_frames', width=100):
    Path(ascii_folder).mkdir(parents=True, exist_ok=True)
    
    frame_files = sorted([f for f in os.listdir(frames_folder) 
                         if f.endswith(('.jpg', '.jpeg', '.png'))])
    
    if not frame_files:
        print(f"No frames found in {frames_folder}")
        return
    
    print(f"Converting {len(frame_files)} frames to ASCII...")
    
    for i, filename in enumerate(frame_files):
        frame_path = os.path.join(frames_folder, filename)
        frame = cv2.imread(frame_path)
        
        if frame is None:
            print(f"Warning: Could not read {filename}")
            continue

        ascii_art = frame_to_ascii(frame, width)
        
        output_filename = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(ascii_folder, output_filename)
        
        with open(output_path, 'w') as f:
            f.write(ascii_art)
        
        if (i + 1) % 50 == 0 or (i + 1) == len(frame_files):
            print(f"Converted {i + 1}/{len(frame_files)} frames")
    
    print(f"\nConversion complete! ASCII frames saved in '{ascii_folder}'")

def play_ascii_video(ascii_folder='ascii_frames', fps=30, audio_path=None):
    ascii_files = sorted([f for f in os.listdir(ascii_folder)
                         if f.endswith('.txt')])

    if not ascii_files:
        print(f"No ASCII frames found in {ascii_folder}")
        return

    frame_delay = 1.0 / fps

    print(f"Playing {len(ascii_files)} frames at {fps} FPS")
    print("Press Ctrl+C to stop")
    print("\nPress any key to start...")
    input()

    audio_thread = None
    if audio_path and os.path.exists(audio_path):
        audio_thread = threading.Thread(target=play_audio, args=(audio_path,), daemon=True)
        audio_thread.start()

    try:
        for filename in ascii_files:
            start_time = time.time()

            with open(os.path.join(ascii_folder, filename), 'r') as f:
                ascii_frame = f.read()

            print("\033[2J\033[H" + ascii_frame, end='', flush=True)

            elapsed = time.time() - start_time
            sleep_time = max(0, frame_delay - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n\nPlayback stopped.")

def extract_audio(video_path, audio_output='audio.mp3'):
    try:
        print(f"Extracting audio from video...")
        result = subprocess.run(
            ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-y', audio_output],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            print(f"Audio extracted successfully: {audio_output}")
            return True
        else:
            print(f"Warning: Could not extract audio. ffmpeg may not be installed.")
            print(f"The video will play without sound.")
            return False
    except FileNotFoundError:
        print("Warning: ffmpeg not found. Install ffmpeg to enable audio playback.")
        print("The video will play without sound.")
        return False
    except Exception as e:
        print(f"Warning: Error extracting audio: {e}")
        print("The video will play without sound.")
        return False

def play_audio(audio_path):
    try:
        subprocess.run(
            ['ffplay', '-nodisp', '-autoexit', audio_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass  

def cleanup_folders(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Deleted: {folder}")

def cleanup_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted: {file}")

def main():
    print("ASCII Video Player")
    print("=" * 50)
    print()

    frames_folder = 'frames'
    ascii_folder = 'ascii_frames'
    audio_file = 'audio.mp3'

    has_frames = os.path.exists(frames_folder) and len(os.listdir(frames_folder)) > 0
    has_ascii = os.path.exists(ascii_folder) and len(os.listdir(ascii_folder)) > 0
    has_audio = os.path.exists(audio_file)

    process_new_video = True
    video_fps = 30
    playback_fps = 30
    audio_available = False

    if has_frames or has_ascii or has_audio:
        print("Found existing processed files:")
        if has_frames:
            print(f"  - {frames_folder}/ folder")
        if has_ascii:
            print(f"  - {ascii_folder}/ folder")
        if has_audio:
            print(f"  - {audio_file}")
        print()

        response = input("Process a new video? (y/n, default: n): ").strip().lower()
        process_new_video = response in ['y', 'yes']

    if process_new_video:
        if has_frames or has_ascii or has_audio:
            print("\nCleaning up old files...")
            cleanup_folders(frames_folder, ascii_folder)
            cleanup_files(audio_file)
            print()

        video_path = input("Enter the path to your video file: ").strip()

        if video_path.startswith('"') and video_path.endswith('"'):
            video_path = video_path[1:-1]
        elif video_path.startswith("'") and video_path.endswith("'"):
            video_path = video_path[1:-1]

        width_input = input("Enter ASCII width in characters (default 100): ").strip()
        width = int(width_input) if width_input else 100

        frame_interval = FRAME_SKIP

        print("=" * 50)
        print("Step 1: Extracting frames from video...")
        print("=" * 50 + "\n")

        video_fps, frames_saved = extract_frames(video_path, frames_folder, frame_interval)

        if video_fps is None or frames_saved == 0:
            print("Failed to extract frames. Exiting.")
            return

        print("\n" + "=" * 50)
        print("Step 2: Extracting audio from video...")
        print("=" * 50 + "\n")

        audio_available = extract_audio(video_path, audio_file)

        print("\n" + "=" * 50)
        print("Step 3: Converting frames to ASCII...")
        print("=" * 50 + "\n")

        convert_frames_to_ascii(frames_folder, ascii_folder, width)

        playback_fps = video_fps / frame_interval
    else:
        print("\nUsing existing processed files...")
        audio_available = has_audio

        if has_frames:
            frame_files = [f for f in os.listdir(frames_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"Found {len(frame_files)} frames")

        playback_fps = 30 / FRAME_SKIP

    print("\n" + "=" * 50)
    print("Playing ASCII video...")
    print("=" * 50 + "\n")

    play_ascii_video(ascii_folder, playback_fps, audio_file if audio_available else None)

    print("\nPlayback complete!")

if __name__ == "__main__":
    main()