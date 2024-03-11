import subprocess  # nosec
import sys


def run():
    subprocess.call(["flask", "run"])  # nosec

if __name__ == "__main__":
    # This shim doesn't import anything from the application, so has no logger configuration.
    # Print warnings to STDOUT.
    print("WARNING: use of manage.py is deprecated")
    if len(sys.argv) <= 1:
        raise Exception("Please specify a command")

    command = sys.argv[1]

    if command == "runserver":
        run()
    else:
        raise Exception("Command unknown")
