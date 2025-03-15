class Formatter:
    def format_bytes(bytes):
        suffixes = ['B', 'KB', 'MB', 'GB']
        index = 0

        while bytes >= 1024 and index < len(suffixes) - 1:
            bytes /= 1024.0
            index += 1

        return '{:.3g} {}'.format(bytes, suffixes[index])