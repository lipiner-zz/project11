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
PUSH_COMMAND = "push"
POP_COMMAND = "pop"
GOTO_COMMAND = "goto"
IF_COMMAND = "if-goto"
RETURN_COMMAND = "return"
FUNCTION_COMMAND = "function"
CALL_COMMAND = "call"
COMMAND_SEP = " "
SEGMENTS_DICT = {STATIC_SEGMENT_KEYWORD: STATIC_SEGMENT, ARG_SEGMENT_KEYWORD: ARG_SEGMENT,
                 VAR_SEGMENT_KEYWORD: LOCAL_SEGMENT, FIELD_SEGMENT_KEYWORD: THIS_SEGMENT}
MATH_DICT = {"*": "Math.multiply", "/": "Math.divide"}
MATH_NUM_ARGS = 2
UNARY_OP_DICT = {"-": "neg", "~": "not"}
BINARY_OP_DICT = {"+": "add", "-": "sub", "&": "and", "|": "or", ">": "gt", "<": "lt", "=": "eq"}
LABEL_NAME = "L"
LINE_BREAK = "\n"
FUNCTION_NAME_SEP = "."


class VMWriter:
    """
    VMWriter class. The class writes vm commands into a given output stream
    """
    def __init__(self, output_stream):
        """
        Initialize VMWriter object that writes the vm commands to the given output stream
        :param output_stream: the stream to write the vm command into
        """
        self.__output_stream = output_stream

    def write_push(self, segment, index):
        """
        Writes a VM push command
        :param segment: the memory segment
        :param index: the index within the memory segment
        """
        if segment in SEGMENTS_DICT:
            segment = SEGMENTS_DICT[segment]

        self.__output_stream.write(PUSH_COMMAND + COMMAND_SEP + segment + COMMAND_SEP + str(index) + LINE_BREAK)

    def write_pop(self, segment, index):
        """
        Writes a VM pop command
        :param segment: the memory segment
        :param index: the index within the memory segment
        """
        if segment in SEGMENTS_DICT:
            segment = SEGMENTS_DICT[segment]

        self.__output_stream.write(POP_COMMAND + COMMAND_SEP + segment + COMMAND_SEP + str(index) + LINE_BREAK)

    def write_arithmetic(self, command, is_unary=False):
        """
        Writes a VM arithmetic command
        :param command: the operation to be performed
        :param is_unary: checks if the operation is an unary operation
        """
        if is_unary:
            self.__output_stream.write(UNARY_OP_DICT[command] + LINE_BREAK)
            return

        if command in MATH_DICT:
            self.write_call(MATH_DICT[command], MATH_NUM_ARGS)
        else:
            self.__output_stream.write(BINARY_OP_DICT[command] + LINE_BREAK)

    def write_label(self, label):
        """
        Writes a VM label command
        :param label: The number (index) of the label to create
        """
        self.__output_stream.write(LABEL_PREFIX + LABEL_NAME + str(label) + LABEL_SUFFIX + LINE_BREAK)

    def write_goto(self, label):
        """
        Writes a VM goto command
        :param label: The number (index) of the label to create
        """
        self.__output_stream.write(GOTO_COMMAND + COMMAND_SEP + LABEL_NAME + str(label) + LINE_BREAK)

    def write_if(self, label):
        """
        Writes a VM If-goto command
        :param label: The number (index) of the label to create
        """
        self.__output_stream.write(IF_COMMAND + COMMAND_SEP + LABEL_NAME + str(label) + LINE_BREAK)

    def write_call(self, name, n_args):
        """
        Writes a VM call command
        :param name: the called function name
        :param n_args: the number of arguments passed to the function
        """
        self.__output_stream.write(CALL_COMMAND + COMMAND_SEP + name + COMMAND_SEP + str(n_args) + LINE_BREAK)

    def write_function(self, class_name, name, n_locals):
        """
        Writes a VM function command
        :param name: the function name
        :param n_locals: the number of local variable the function needs
        """
        self.__output_stream.write(FUNCTION_COMMAND + COMMAND_SEP + class_name + FUNCTION_NAME_SEP + name +
                                   COMMAND_SEP + str(n_locals) + LINE_BREAK)

    def write_return(self):
        """
        Writes a VM return command
        """
        self.__output_stream.write(RETURN_COMMAND + LINE_BREAK)
