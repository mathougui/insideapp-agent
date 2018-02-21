import sys

from network import ApiCall


def main():
    if len(sys.argv) != 3:
        print("Usage: insideapp [api-key] [process name]")
        return
    api_call = ApiCall()
    api_call.launch_main_loop()


if __name__ == "__main__":
    main()
