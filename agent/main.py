import sys

from mainLoop import MainLoop


def main():
    if len(sys.argv) != 3:
        print("Usage: insideapp [api-key] [process name]")
        return
    api_call = MainLoop()
    api_call.launch_main_loop()


if __name__ == "__main__":
    main()
