from Variable import Variable

STATIC_SEGMENT_KEYWORD = "static"
FIELD_SEGMENT_KEYWORD = "field"
ARG_SEGMENT_KEYWORD = "argument"
VAR_SEGMENT_KEYWORD = "var"
CLASS_VAR_DEC_KEYWORDS = [FIELD_SEGMENT_KEYWORD, STATIC_SEGMENT_KEYWORD]


class SymbolTable:

    def __init__(self):
        self.__class_variables = {}
        self.__subroutine_variables = {}
        # saves how mane variable there are from each kind - will be the next index of that kind's variable
        self.__var_segment_count = {STATIC_SEGMENT_KEYWORD: 0, FIELD_SEGMENT_KEYWORD: 0, ARG_SEGMENT_KEYWORD: 0,
                                    VAR_SEGMENT_KEYWORD: 0}

    def start_subroutine(self):
        self.__subroutine_variables = {}
        # nullify the number of args and vars
        self.__var_segment_count[ARG_SEGMENT_KEYWORD] = 0
        self.__var_segment_count[VAR_SEGMENT_KEYWORD] = 0

    def define(self, name, var_type, kind):
        # creates new var with the next index
        new_var = Variable(name, var_type, kind, self.__var_segment_count[kind])
        # adds the var to the correct dictionary
        if kind in FIELD_SEGMENT_KEYWORD:
            self.__class_variables[name] = new_var
        else:
            self.__subroutine_variables[name] = new_var

        self.__var_segment_count[kind] += 1  # increment the next index of that kind

    def var_count(self, kind):
        return self.__var_segment_count[kind]

    def type_of(self, var_name):
        if var_name in self.__subroutine_variables:
            return self.__subroutine_variables[var_name].get_type()
        if var_name in self.__class_variables:
            return self.__class_variables[var_name].get_type()
        return None

    def kind_of(self, var_name):
        if var_name in self.__subroutine_variables:
            return self.__subroutine_variables[var_name].get_type()
        if var_name in self.__class_variables:
            return self.__class_variables[var_name].get_type()
        return None

    def index_of(self, var_name):
        if var_name in self.__subroutine_variables:
            return self.__subroutine_variables[var_name].get_type()
        if var_name in self.__class_variables:
            return self.__class_variables[var_name].get_type()
        return None
