class Log:
    files = {}

    def __init__(self, filenames):
        for filename in filenames:
            file = open(filenames[filename], 'r')
            file.seek(0, 2)
            self.files[filename] = file

    def get_logs(self, log_type):
        lines = self.files[log_type].readlines()
        to_remove = []
        for index, line in enumerate(lines):
            striped_line = line.rstrip('\n')
            if not striped_line:
                to_remove += line
            else:
                lines[index] = striped_line
        for element in to_remove:
            lines.remove(element)
        return lines
