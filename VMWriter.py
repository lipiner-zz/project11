CONSTANT_SEGMENT = "constant"
LOCAL_SEGMENT = "local"
ARG_SEGMENT = "argument"
STATIC_SEGMENT = "static"
POINTER_SEGMENT = "pointer"
TEMP_SEGMENT = "temp"
THAT_SEGMENT = "that"
THIS_SEGMENT = "this"
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
        :param label:
        :return:
        """
        self.__output_stream.write(LABEL_NAME + str(label))

    def write_goto(self, label):
        """
        Writes a VM label command
        :param label:
        :return:
        """
        pass

    def write_if(self, label):
        """
        Writes a VM If-goto command
        :param label:
        :return:
        """
        pass

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