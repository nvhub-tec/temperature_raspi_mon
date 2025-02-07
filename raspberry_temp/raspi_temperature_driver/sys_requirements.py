import platform
import sys


def check_system_requirements():
    # Check if running on Linux
    if platform.system() != "Linux":
        print("Error: This script is designed to run on Linux")
        sys.exit(1)