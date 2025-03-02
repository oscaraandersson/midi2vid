from pathlib import Path


def find_project_root(marker: str = "pyproject.toml") -> Path:
  """ Traverse upward from the current file's location to find the project root
  containing the specified marker file (e.g., pyproject.toml).  """
  current_path = Path(__file__).resolve().parent
  while current_path != current_path.parent:
    if (current_path / marker).exists():
      return current_path
    current_path = current_path.parent
  raise FileNotFoundError(
    f"Project root not found. '{marker}' file is missing."
  )