class LabelSet:

    def __init__(self, iterable=None):
        self._list = []
        self._dict = {}
        self._index = 0

        if iterable is not None:
            for elem in iterable:
                self.add(elem)

    def add(self, item):
        if item not in self._dict:
            self._list.append(item)
            self._dict[item] = len(self._list) - 1
        return self._dict[item]

    def index(self, item):
        return self._dict[item]

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def __contains__(self, item):
        return item in self._dict
