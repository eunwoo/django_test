class DictToClass:
    def __init__(self, **entries):
        self.__dict__.update(entries)
