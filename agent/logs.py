import time


def get_logs(path):
    file = open(path, 'r')
    lines = follow(file)
    for line in lines:
        print(line, flush=True)


def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
