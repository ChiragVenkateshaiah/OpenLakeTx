from pathlib import Path
from typing import List, Union




class Storage:
    """
    Low-level filesystem abstraction.

    Responsibilities:
    - Directory creation
    - File read / write
    - File listing
    - Existence checks

    This layer is intentionally dumb

    """

    def __init__(self, base_path: Union[str, Path]):
        self.base_path = Path(base_path)


    # -----------------------------
    # Path helpers
    # -----------------------------
    def resolve(self, path: Union[str, Path]) -> Path:
        """
        Resolve a path relative to base_path.
        """

        path = Path(path)
        if path.is_absolute():
            return path
        return self.base_path / path
    
    # --------------------------------
    # Directory operations
    # --------------------------------
    def mkdir(self, path: Union[str, Path]) -> None:
        """
        Create directory (idempotent)
        """
        full_path = self.resolve(path)
        full_path.mkdir(parents=True, exist_ok=True)

    def exists(self, path: Union[str, Path]) -> bool:
        """
        Check if a file or directory exists.
        """

        return self.resolve(path).exists()
    
    # ------------------------------------------------
    # File operations
    # ------------------------------------------------
    def write_file(self, path: Union[str, Path], data: str) -> None:
        """
        Write data to a file.
        Overwrites if file already exists.
        """
        full_path = self.resolve(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w', encoding="utf-8") as f:
            f.write(data)

    def read_file(self, path: Union[str, Path]) -> str:
        
        """
        Read file content
        """
        full_path = self.resolve(path)
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")
        
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
        
    # -------------------------------------------------------------
    # Listing operations
    # -------------------------------------------------------------
    def list_files(self, path: Union[str, Path]) -> List[str]:
        """
        List files (not directories) in a directory.
        Returns file names sorted lexicographically.
        """

        full_path = self.resolve(path)

        if not full_path.exists():
            return []
        
        if not full_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {full_path}")
        
        return sorted(
            p.name for p in full_path.iterdir() if p.is_file()
        )