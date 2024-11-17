import subprocess
import os
import gdown

# YouTube Stream Key and Main RTMP URL
YOUTUBE_STREAM_KEY = "6rdk-91fu-05cu-u9b3-50dk"
YOUTUBE_RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"

# Backup RTMP URL
YOUTUBE_BACKUP_RTMP_URL = "rtmp://b.rtmp.youtube.com/live2?backup=1"

# File to be streamed
VIDEO_FILE = "video.mp4"

def download_google_drive_file(share_link, output_file):
    """Download a file from Google Drive."""
    try:
        # Extract the file ID from the sharing link
        file_id = share_link.split('/d/')[1].split('/view')[0]
        # Create the download URL
        download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        
        # Download the file
        gdown.download(download_url, output_file, quiet=False)
        print(f"Downloaded: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_video(video_url):
    """Download the video using wget or Google Drive."""
    if os.path.exists(VIDEO_FILE):
        print(f"{VIDEO_FILE} already exists. Skipping download.")
    else:
        if "drive.google.com" in video_url:
            print("Detected Google Drive link. Downloading...")
            download_google_drive_file(video_url, VIDEO_FILE)
        else:
            print(f"Downloading video from {video_url}...")
            subprocess.run(["wget", "-O", VIDEO_FILE, video_url], check=True)
            print(f"Video downloaded as {VIDEO_FILE}.")

def stream_video():
    """Stream the video using FFmpeg."""
    ffmpeg_command = [
        "ffmpeg",
        "-re",  # Real-time streaming
        "-stream_loop", "-1",  # Loop the video indefinitely
        "-i", VIDEO_FILE,  # Input video file
        "-vf", "scale=1080:1920",  # Resize to 9:16 aspect ratio (720x1280 for Shorts)
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "3000k",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "50",
        "-c:a", "aac",
        "-b:a", "160k",
        "-ar", "44100",
        "-f", "flv",  # RTMP requires FLV format
        YOUTUBE_RTMP_URL
    ]

    try:
        print("Starting stream on main RTMP URL...")
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError:
        print("Main RTMP URL failed, switching to backup URL...")
        ffmpeg_command[-1] = YOUTUBE_BACKUP_RTMP_URL
        subprocess.run(ffmpeg_command)

def main():
    """Main function to download and stream the video."""
    video_url = input("Enter the video URL (Google Drive or direct link): ")
    
    while True:
        download_video(video_url)
        stream_video()
        print("Streaming completed. Restarting...")

if __name__ == "__main__":
    main()
