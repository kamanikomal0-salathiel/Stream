import subprocess
import os
import requests

VIDEO_FILE = "A.mp4"

def download_from_google_drive(drive_url):
    """Download file from Google Drive."""
    try:
        print(f"Downloading from Google Drive URL: {drive_url}")
        file_id = None

        # Extract file ID from different types of Google Drive URLs
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[1].split("&")[0]
        elif "/d/" in drive_url:
            file_id = drive_url.split("/d/")[1].split("/")[0]

        if not file_id:
            raise ValueError("Invalid Google Drive URL format")

        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        subprocess.run(["wget", "--no-check-certificate", "-O", VIDEO_FILE, download_url], check=True)
        print(f"File downloaded as {VIDEO_FILE}.")
    except Exception as e:
        print(f"Error downloading from Google Drive: {e}")

def download_direct_url(direct_url):
    """Download file from a direct URL."""
    try:
        print(f"Downloading from Direct URL: {direct_url}")
        subprocess.run(["wget", "-O", VIDEO_FILE, direct_url], check=True)
        print(f"File downloaded as {VIDEO_FILE}.")
    except Exception as e:
        print(f"Error downloading from Direct URL: {e}")

def download_video(url):
    """Determine the URL type and download the file."""
    if "drive.google.com" in url:
        download_from_google_drive(url)
    else:
        download_direct_url(url)

def main():
    """Main function to handle multiple URLs."""
    urls = [
        "https://drive.usercontent.google.com/download?id=1-ShHsQuwAqK1CaLPlaQMY2aioD4VnCnC&export=download&authuser=0&confirm=t&uuid=3d8940bf-4b92-40e0-a69a-e39d9206d3c4&at=AENtkXa9Nn5XoixfZrQCDRy95khm%3A1731827305313",  # Example Google Drive URL
        "https://example.com/path/to/video.mp4",  # Example direct URL
    ]

    for url in urls:
        if os.path.exists(VIDEO_FILE):
            print(f"{VIDEO_FILE} already exists. Deleting the old file.")
            os.remove(VIDEO_FILE)
        
        download_video(url)

        if os.path.exists(VIDEO_FILE):
            print(f"Successfully downloaded: {VIDEO_FILE}")
        else:
            print("Failed to download file. Skipping...")

if __name__ == "__main__":
    main()
