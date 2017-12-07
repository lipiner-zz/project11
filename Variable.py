

class Variable:

    def __init__(self, name, type, kind, index):
        self.__name = name
        self.__type = type
        self.__kind = kind
        self.__index = index

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_kind(self):
        return self.__kind

    def get_index(self):
        return self.__index
