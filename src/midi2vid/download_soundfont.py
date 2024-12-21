from pathlib import Path

from gdown import download  # type: ignore


def find_project_root(marker: str = "pyproject.toml"):
  """
  Traverse upward from the current file's location to find the project root
  containing the specified marker file (e.g., pyproject.toml).
  """
  current_path = Path(__file__).resolve().parent
  while current_path != current_path.parent:
    if (current_path / marker).exists():
      return current_path
    current_path = current_path.parent
  raise FileNotFoundError(
    f"Project root not found. '{marker}' file is missing."
  )


def download_soundfont():
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
      raise
  else:
    print(f"{target_file} already exists. Skipping download.")


if __name__ == "__main__":
  download_soundfont()
