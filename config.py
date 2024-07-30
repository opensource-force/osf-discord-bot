from collections.abc import Mapping


class Config(Mapping):
    """
    Aggregates Mappings into one Config object.
    Items can be added and overridden, but not removed.
    Deep copies mappings, overrides all other classes.
    """

    def __init__(self, *args: Mapping):
        self._data = {}

        for arg in args:
            if arg is None:
                continue

            for k, v in arg.items():
                if isinstance(v, Mapping):
                    self._data.setdefault(k, Config())
                    self._data[k].update(v)
                else:
                    self._data[k] = v

    def __getitem__(self, __key):
        return self._data[__key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, __key):
        return __key in self._data

    def __setitem__(self, key, value):
        if isinstance(value, Mapping):
            self._data.setdefault(key, Config)
            self._data[key].update(value)
        else:
            self._data[key] = value

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def update(self, other):
        if isinstance(other, Mapping):
            for k, v in other.items():
                if isinstance(v, Mapping):
                    self._data.setdefault(k, Config())
                    self._data[k].update(v)
                else:
                    self._data[k] = v

    def get(self, __key, default=None):
        return self._data.get(__key, default)

    def resolve(self, *args: str, default=None):
        current = self
        for arg in args:
            if (not isinstance(current, Config) or
                    arg not in current):
                return default

            current = current[arg]
        return current
