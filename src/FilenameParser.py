class FilenameParser:
    def __init__(self):
        return

    @staticmethod
    def parseFileName(path, delimiter):
        filename = path.split(delimiter)[-1]
        filenameParts = filename.split(" ")

        if len(filename) > 10:
            return filenameParts[0] + " ... " + filenameParts[-1]
        else:
            return filename