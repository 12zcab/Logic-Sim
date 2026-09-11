import os
import shutil

def clear_pycache(root_dir="."):
    for root, dirs, files in os.walk(root_dir):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                os.remove(file_path)

if __name__ == "__main__":
    clear_pycache()
