import glob
import os
import subprocess

if __name__ == "__main__":
    for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(__file__))):
        for file in glob.glob(os.path.join(root, "*.ipynb")):
            subprocess.run(
                f"jupyter nbconvert --to notebook --execute --clear-output {file}",
                shell=True,
            )
