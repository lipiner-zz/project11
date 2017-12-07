from Variable import Variable

STATIC_SEGMENT_KEYWORD = "static"
FIELD_SEGMENT_KEYWORD = "field"
ARG_SEGMENT_KEYWORD = "arg"
VAR_SEGMENT_KEYWORD = "var"
CLASS_VAR_DEC_KEYWORDS = [FIELD_SEGMENT_KEYWORD, STATIC_SEGMENT_KEYWORD]


class SymbolTable:
    """
    Creates a symbol table with all the class and subroutine variables
    """
    def __init__(self):
        """
        Initializes a new symbol table
        """
        self.__class_variables = {}
        self.__subroutine_variables = {}
        # saves how mane variable there are from each kind - will be the next index of that kind's variable
        self.__var_segment_count = {STATIC_SEGMENT_KEYWORD: 0, FIELD_SEGMENT_KEYWORD: 0, ARG_SEGMENT_KEYWORD: 0,
                                    VAR_SEGMENT_KEYWORD: 0}

    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope)
        """
        self.__subroutine_variables = {}
        # nullify the number of args and vars
        self.__var_segment_count[ARG_SEGMENT_KEYWORD] = 0
        self.__var_segment_count[VAR_SEGMENT_KEYWORD] = 0

    def define(self, name, var_type, kind):
        """
        Defines a new identifier in the table of a given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
        :param name: the name of the variable
        :param var_type: the type of the variable
        :param kind: the kind of the variable (static, field, arg, var)
        """
        # creates new var with the next index
        new_var = Variable(name, var_type, kind, self.__var_segment_count[kind])
        # adds the var to the correct dictionary
        if kind in FIELD_SEGMENT_KEYWORD:
            self.__class_variables[name] = new_var
        else:
            self.__subroutine_variables[name] = new_var

        self.__var_segment_count[kind] += 1  # increment the next index of that kind

    def var_count(self, kind):
        """
        :param kind: a kind of the variables- static, field, arg, var
        :return: the number of variables of the given kind already defined in the current scope.
        """
        return self.__var_segment_count[kind]

    def get_type_of(self, var_name):
        """
        :param var_name: the desired variable's name
        :return: Returns the type of the named identifier in the current scope. Returns NONE if the
        identifier is unknown in the current scope.
        """
        if var_name in self.__subroutine_variables:
            return self.__subroutine_variables[var_name].get_type()
        if var_name in self.__class_variables:
            return self.__class_variables[var_name].get_type()
        return None

    def get_kind_of(self, var_name):
        """
        :param var_name: the desired variable's name
        :return: Returns the kind of the named identifier in the current scope. Returns NONE if the
        identifier is unknown in the current scope.
        """
        if var_name in self.__subroutine_variables:
            return self.__subroutine_variables[var_name].get_type()
        if var_name in self.__class_variables:
            return self.__class_variables[var_name].get_type()
        return None

    def get_index_of(self, var_name):
        """
        :param var_name: the desired variable's name
        :return: Returns the index of the named identifier in the current scope. Returns NONE if the
        identifier is unknown in the current scope.
        """
        if var_name in self.__subroutine_variables:
            return self.__subroutine_variables[var_name].get_type()
        if var_name in self.__class_variables:
            return self.__class_variables[var_name].get_type()
        return None
