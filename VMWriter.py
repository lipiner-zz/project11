from SymbolTable import STATIC_SEGMENT_KEYWORD, FIELD_SEGMENT_KEYWORD, ARG_SEGMENT_KEYWORD, \
    VAR_SEGMENT_KEYWORD

CONSTANT_SEGMENT = "constant"
LOCAL_SEGMENT = "local"
ARG_SEGMENT = "argument"
STATIC_SEGMENT = "static"
POINTER_SEGMENT = "pointer"
TEMP_SEGMENT = "temp"
THAT_SEGMENT = "that"
THIS_SEGMENT = "this"
LABEL_PREFIX = "("
LABEL_SUFFIX = ")"
GOTO_COOMAND = "goto "
IF_COMMAND = "if-goto "
SEGMENTS_DICT = {STATIC_SEGMENT_KEYWORD: STATIC_SEGMENT, ARG_SEGMENT_KEYWORD: ARG_SEGMENT,
                 VAR_SEGMENT_KEYWORD: LOCAL_SEGMENT, FIELD_SEGMENT_KEYWORD: FIELD_SEGMENT_KEYWORD}
LABEL_NAME = "L"


class VMWriter:

    def __init__(self, output_stream):
        self.__output_stream = output_stream


    def write_push(self, segment, index):
        """
        Writes a VM push command
        :param segment:
        :param index:
        :return:
        """
        pass

    def write_pop(self, segment, index):
        """
        Writes a VM pop command
        :param segment:
        :param index:
        :return:
        """
        pass

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command:
        :return:
        """
        pass

    def write_label(self, label):
        """
        Writes a VM label command
        :param label: The number (index) of the label to create
        """
        self.__output_stream.write(LABEL_PREFIX + LABEL_NAME + str(label) + LABEL_SUFFIX)

    def write_goto(self, label):
        """
        Writes a VM goto command
        :param label: The number (index) of the label to create
        """
        self.__output_stream.write(GOTO_COOMAND + LABEL_NAME + str(label))

    def write_if(self, label):
        """
        Writes a VM If-goto command
        :param label: The number (index) of the label to create
        """
        self.__output_stream.write(IF_COMMAND + LABEL_NAME + str(label))

    def write_call(self, name, n_args):
        """
        Writes a VM call command
        :param name:
        :param n_args:
        :return:
        """
        pass

    def write_function(self, name, n_locals):
        """
        Writes a VM function command
        :param name:
        :param n_locals:
        :return:
        """
        pass

    def write_return(self):
        """
        Writes a VM return command
        :return:
        """
        pass