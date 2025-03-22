import subprocess

def capture_with_ffmpeg(duration=10, output_file="record.avi"):
    output_file =  output_file
    command = [
        "ffmpeg",
        "-f", "v4l2",
        "-i", "/dev/video0",
        "-c:v", "libx264",
        output_file
    ]

    try:
        # Run the command with a timeout
        subprocess.run(command, timeout=(duration+3), check=True)
        print(f"Video saved as {output_file}")
    except subprocess.TimeoutExpired:
        print(f"Recording stopped after {duration+3} seconds.")
    except subprocess.CalledProcessError as e:
        print(f"Error capturing video: {e}")

