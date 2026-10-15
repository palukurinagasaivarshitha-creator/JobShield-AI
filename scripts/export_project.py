import os
import sys
import zipfile
from pathlib import Path

# Exclusion patterns for clean export
EXCLUDE_DIRS = {
    "node_modules",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist",
    ".idea",
    ".vscode",
    "brain",
    ".system_generated",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".log",
    ".tmp",
    ".DS_Store",
}

EXCLUDE_FILES = {
    "fake_jobs.db",
    "FakeJobDetection.zip",
    ".env",  # Exclude local secrets, keep .env.example
}


def should_exclude(rel_path: str) -> bool:
    parts = Path(rel_path).parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True

    filename = os.path.basename(rel_path)
    if filename in EXCLUDE_FILES:
        return True

    _, ext = os.path.splitext(filename)
    if ext in EXCLUDE_EXTENSIONS:
        return True

    return False


def create_export_archive(output_filename: str = "FakeJobDetection.zip") -> str:
    root_dir = Path(__file__).resolve().parent.parent
    zip_path = root_dir / output_filename

    print(f"[EXPORT] Packaging project into: {zip_path}")
    file_count = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for foldername, subfolders, filenames in os.walk(root_dir):
            # Modify subfolders in-place to skip excluded directories during recursion
            subfolders[:] = [d for d in subfolders if d not in EXCLUDE_DIRS]

            for filename in filenames:
                full_path = os.path.join(foldername, filename)
                rel_path = os.path.relpath(full_path, root_dir)

                if should_exclude(rel_path):
                    continue

                zipf.write(full_path, arcname=os.path.join("FakeJobDetection", rel_path))
                file_count += 1

    print(f"[EXPORT] Successfully added {file_count} files.")
    
    # Verify archive integrity
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Export failed: {zip_path} not created.")

    with zipfile.ZipFile(zip_path, "r") as zipf:
        bad_file = zipf.testzip()
        if bad_file:
            raise ValueError(f"Corrupted file detected in archive: {bad_file}")
        total_in_zip = len(zipf.namelist())

    file_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[EXPORT] Integrity verified: {total_in_zip} entries, {file_size_mb:.2f} MB")
    print(f"[EXPORT] Output Archive: {zip_path}")
    return str(zip_path)


if __name__ == "__main__":
    archive = create_export_archive()
    print(f"\nFinal export archive ready at:\n{archive}")
