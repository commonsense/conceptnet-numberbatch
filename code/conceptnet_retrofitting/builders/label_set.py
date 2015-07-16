from collections import OrderedDict

class LabelSet:

    def __init__(self, iterable=None):
        self._seq = OrderedDict()
        self._index = 0

        if iterable is not None:
            for elem in iterable:
                self.add(elem)

    def add(self, item):
        if item not in self._seq:
            self.append(item)
        return self._seq[item]

    def append(self, item):
        self._seq[item] = self._index
        self._index += 1

    def index(self, item):
        return self._seq[item]

    def __len__(self):
        return len(self._seq)

    def __iter__(self):
        return iter(self._seq)

    def __contains__(self, item):
        return item in self._seq
