# """Utils"""

# Author: gabisurita -- <gabsurita@gmail.com>
# License: GPL 3.0


class ContentFinder(object):
    def __init__(self, data, separator='\n'):
        self.data = data
        self.split = [s.strip() for s in data.split(separator) if s.strip()]

    def find_by_content(self, pattern, offset=0, count=None,
                        end_pattern=None):
        try:
            pattern = pattern.decode('utf-8')
        except:
            pass

        for piece, i in zip(self.split, range(len(self.split))):
            if pattern in piece:
                start_at = i
                break

        if count:
            return self.split[start_at + offset:start_at + count]

        elif end_pattern:
            for piece, i in zip(self.split[start_at:],
                                range(start_at, len(self.split))):
                if end_pattern in piece:
                    end_idx = i
                    break

            return self.split[start_at + offset:end_idx]

        else:
            return self.split[start_at + offset]
