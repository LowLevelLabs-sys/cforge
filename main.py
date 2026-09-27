import sys
from utils import cforge_main


def main():
    cforge_main()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
