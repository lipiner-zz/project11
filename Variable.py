class Variable:
    """
    A variable object. Contain all the variable info- its name, type, kind (segment), index in the segment
    """
    def __init__(self, name, type, kind, index):
        """
        Initialize a variable object with the given parameters
        :param name: The variable's name
        :param type: The variable's type
        :param kind: The variable's kind (static, field, arg, var)
        :param index: The variable's index in the specified kind
        """
        self.__name = name
        self.__type = type
        self.__kind = kind
        self.__index = index

    def get_name(self):
        """
        :return: The variable's name
        """
        return self.__name

    def get_type(self):
        """
        :return: The variable's type
        """
        return self.__type

    def get_kind(self):
        """
        :return: The variable's kind (static, field, arg, var)
        """
        return self.__kind

    def get_index(self):
        """
        :return: The variable's index in the specified kind
        """
        return self.__index
