from gdown import download  # type: ignore

from midi2vid.utils import find_project_root


def download_soundfont() -> None:
  # Here I found multiple soundfonts
  # https://sites.google.com/site/soundfonts4u/
  url = "https://drive.google.com/uc?id=1nvTy62-wHGnZ6CKYuPNAiGlKLtWg9Ir9"
  project_root = find_project_root()

  # Define the target directory and file
  assets_dir = project_root / "data"
  assets_dir.mkdir(parents=True, exist_ok=True)
  target_file = assets_dir / "soundfont.sf2"

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
