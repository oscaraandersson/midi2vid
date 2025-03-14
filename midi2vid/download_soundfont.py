import os
from pathlib import Path

from gdown import download  # type: ignore


def download_soundfont() -> None:
  # Here I found multiple soundfonts
  # https://sites.google.com/site/soundfonts4u/
  url = "https://drive.google.com/uc?id=1nvTy62-wHGnZ6CKYuPNAiGlKLtWg9Ir9"

  # Define the target directory and file
  data_dir = Path(os.path.dirname(__file__)) / "data"
  data_dir.mkdir(parents=True, exist_ok=True)
  target_file = data_dir / "soundfont.sf2"

  # Download the file
  if not target_file.exists():
    print(f"Downloading file from Google Drive to {target_file}...")
    try:
      download(url, str(target_file), quiet=False)
      print("Download complete.")
    except Exception as e:
      print(f"Failed to download the file: {e}")
      raise e
  else:
    print(f"{target_file} already exists. Skipping download.")


if __name__ == "__main__":
  download_soundfont()
