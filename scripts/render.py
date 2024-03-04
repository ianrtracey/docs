import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-refresh",
        help="rerun jupyter notebooks",
        action="store_true",
    )
    args = parser.parse_args()
    if args.full_refresh:
        subprocess.run("python scripts/rerun_jupyter.py", shell=True)

    subprocess.run("quarto render", shell=True)
    subprocess.run("python scripts/replace_pre.py", shell=True)
