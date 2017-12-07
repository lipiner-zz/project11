from Variable import Variable

STATIC_SEGMENT_KEYWORD = "static"
FIELD_SEGMENT_KEYWORD = "field"
ARG_SEGMENT_KEYWORD = "argument"
VAR_SEGMENT_KEYWORD = "local"
CLASS_VAR_DEC_KEYWORDS = ["field", "static"]


class SymbolTable:

    def __init__(self):
        self.__class_variables = {}
        self.__subroutine_variables = {}
        self.__var_segment_count = {STATIC_SEGMENT_KEYWORD: 0, FIELD_SEGMENT_KEYWORD: 0, ARG_SEGMENT_KEYWORD: 0,
                                    VAR_SEGMENT_KEYWORD: 0}

    def start_subroutine(self):
        pass

    def define(self, name, var_type, kind):
        pass

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
