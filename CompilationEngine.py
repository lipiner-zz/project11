from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_CONST_TYPE, IDENTIFIER_TYPE, TAG_CLOSER
from SymbolTable import CLASS_VAR_DEC_KEYWORDS
from VMWriter import VMWriter, CONSTANT_SEGMENT, LOCAL_SEGMENT, ARG_SEGMENT, STATIC_SEGMENT,\
    POINTER_SEGMENT, TEMP_SEGMENT, THAT_SEGMENT, THIS_SEGMENT
from SymbolTable import SymbolTable, STATIC_SEGMENT_KEYWORD, FIELD_SEGMENT_KEYWORD, ARG_SEGMENT_KEYWORD, \
    VAR_SEGMENT_KEYWORD

OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP_LIST = ['-', '~']
COMPILER_TAG = "tokens"
CLASS_TAG = "class"
CLASS_VAR_TAG = "classVarDec"
SUBROUTINE_BODY_TAG = "subroutineBody"
VAR_DEC_TAG = "varDec"
PARAMETERS_LIST_TAG = "parameterList"
SUBROUTINE_DEC_TAG = "subroutineDec"
METHOD_DEC_KEYWORD = 'method'
CONSTRUCTOR_DEC_KEYWORD = 'constructor'
SUBROUTINE_DEC_KEYWORDS = [CONSTRUCTOR_DEC_KEYWORD, 'function', METHOD_DEC_KEYWORD]
VAR_KEYWORDS = [VAR_SEGMENT_KEYWORD]
TYPE_LIST = ["int", "char", "boolean"]
STATEMENTS_TAG = "statements"
LET_KEYWORD = "let"
IF_KEYWORD = "if"
ELSE_KEYWORD = "else"
WHILE_KEYWORD = "while"
DO_KEYWORD = "do"
RETURN_KEYWORD = "return"
STATEMENTS_LIST = [LET_KEYWORD, IF_KEYWORD, WHILE_KEYWORD, DO_KEYWORD, RETURN_KEYWORD]
LET_TAG = "letStatement"
IF_TAG = "ifStatement"
WHILE_TAG = "whileStatement"
DO_TAG = "doStatement"
RETURN_TAG = "returnStatement"
EXPRESSION_TAG = "expression"
TERM_TAG = "term"
EXPRESSION_LIST_TAG = "expressionList"
ADDITIONAL_VAR_OPTIONAL_MARK = ","
END_LINE_MARK = ";"
OPEN_BRACKET = '('
CLOSE_BRACKET = ')'
OPEN_ARRAY_ACCESS_BRACKET = '['
CALL_CLASS_METHOD_MARK = "."
FUNCTION_CALL_MARKS = [OPEN_BRACKET, CALL_CLASS_METHOD_MARK]
TRUE_CONSTANT = "true"
FALSE_CONSTANT = "false"
THIS_CONSTANT = "this"
NULL_CONSTANT = "null"
KEYWORD_CONSTANT_LIST = [TRUE_CONSTANT, FALSE_CONSTANT, THIS_CONSTANT, NULL_CONSTANT]
TAG_OPENER = "\t"
TAG_END_OF_LINE = "\n"
MINUS = "-"
PLUS = "+"
NOT_OPERATOR = "~"
ARRAY_TYPE = "array"
THAT_POINTER_INDEX = 1
THIS_POINTER_INDEX = 0
ALLOC_FUNCTION = "Memory.alloc"
ALLOC_ARGS_NUM = 1
STRING_CONSTRUCTOR = "String.new"
STRING_CONSTRUCT_NUM_ARGS = 1
STRING_APPEND = "String.appendChar"
STRING_APPEND_NUM_ARGS = 2


class CompilationEngine:
    """
    Effects the actual compilation output. Gets its input from a JackTokenizer and
    emits its parsed structure into an output file/stream. The output is generated by a series of compilexxx()
    routines, one for every syntactic element xxx of the Jack grammar. The contract between these routines is
    that each compilexxx() routine should read the syntactic construct xxx from the input, advance() the
    tokenizer exactly beyond xxx, and output the parsing of xxx. Thus, most of the compilexxx() may only be called if
    indeed xxx is the next syntactic element of the input.
    The module emits a structured printout of the code, wrapped in XML tags.
    """
    def __init__(self, input_stream, output_stream):
        """
        Creates a new compilation engine with the
        given input and output. The next routine
        called must be compileClass().
        """
        self.__prefix = ""
        self.__tokenizer = JackTokenizer(input_stream)
        self.__writer = VMWriter(output_stream)
        self.__symbol_table = SymbolTable()
        self.__label_counter = 0
        self.__class_name = None

    def compile(self):
        """
        Compiles the whole file
        """
        # self.__output_stream.write(self.__create_tag(COMPILER_TAG))
        self.__compile_class()
        # self.__output_stream.write(self.__create_tag(COMPILER_TAG, TAG_CLOSER))

    def __compile_class(self):
        """
        Compiles a complete class
        :return: True iff the class was compiled successfully
        """
        # checks the next parts of the class and writes them to the file
        self.__check_keyword_symbol(KEYWORD_TYPE)  # "class"
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # className
        self.__class_name = self.__tokenizer.get_value()  # saves the class's name for its type when creating this
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "{"
        while self.__compile_class_var_dec():
            continue
        while self.__compile_subroutine(False):
            self.__advance_tokenizer()

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # block closer "}"

    def __compile_class_var_dec(self, make_advance=True):
        """
        Compiles a static declaration or a field declaration
        :param: make_advance: boolean parameter- should make advance before the first call or not. Default value is True
        :return: True iff there was a valid class var declaration
        """
        if not self.__check_keyword_symbol(KEYWORD_TYPE, CLASS_VAR_DEC_KEYWORDS, make_advance):
            # It is not a class var dec
            return False

        var_kind = self.__tokenizer.get_value()  # saves the variable's kind
        self.__check_type()
        var_type = self.__tokenizer.get_value()  # saves the variable's type
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
        var_name = self.__tokenizer.get_value()  # saves the variable's name
        self.__symbol_table.define(var_name, var_type, var_kind)  # adds the variable to the symbol table

        # adds all additional variables to the symbol table
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):  # "," more varName
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
            var_name = self.__tokenizer.get_value()  # saves the variable's name
            self.__symbol_table.define(var_name, var_type, var_kind)  # adds the variable to the symbol table

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ";"

        return True

    def __compile_subroutine(self, make_advance=True):
        """
        Compiles a complete method, function, or constructor.
        :param: make_advance: boolean parameter- should make advance before the first call or not. Default value is True
        :return: True iff there was a valid subroutine declaration
        """
        if not self.__check_keyword_symbol(KEYWORD_TYPE, SUBROUTINE_DEC_KEYWORDS, make_advance):
            # It is not a subroutine
            return False

        self.__symbol_table.start_subroutine()  # creates new subroutine table

        # adds this object in case of a method
        if self.__tokenizer.get_value() == METHOD_DEC_KEYWORD:
            self.__symbol_table.define(THIS_CONSTANT, self.__class_name, ARG_SEGMENT_KEYWORD)
        # creates the object in case of a constructor
        elif self.__tokenizer.get_value() == CONSTRUCTOR_DEC_KEYWORD:
            num_of_fields = self.__symbol_table.var_count(FIELD_SEGMENT_KEYWORD)
            self.__writer.write_push(CONSTANT_SEGMENT, num_of_fields)  # push the number of fields needed for the object
            self.__writer.write_call(ALLOC_FUNCTION, ALLOC_ARGS_NUM)  # calls the alloc function
            self.__writer.write_pop(POINTER_SEGMENT, THIS_POINTER_INDEX)  # anchors this at the base address

        if not self.__check_keyword_symbol(KEYWORD_TYPE):  # not void
            self.__check_type(False)
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # subroutineName
        func_name = self.__tokenizer.get_value()  # saves the function's mame
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "("

        self.__compile_parameter_list()
        # advance was made in the compile_parameter_list without use
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ")"
        self.__compile_subroutine_body(func_name)

        return True

    def __compile_subroutine_body(self, subroutine_name):
        """
        Compiles a subroutine body
        """
        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'

        vars_amount = 0  # number of locals the function needs
        # compiles and writes all variable declarations
        current_dec_var_amount = self.__compile_var_dec()
        while current_dec_var_amount:  # as long there are more declaration
            vars_amount += current_dec_var_amount  # adds the last amount of vars that were declared
            current_dec_var_amount = self.__compile_var_dec()

        self.__writer.write_function(self.__class_name, subroutine_name, vars_amount)  # writes the function's title
        # compiles the statements of the subroutine
        self.__compile_statements()

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'

    def __compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list, not including the enclosing “()”.
        In any way, the function advance the tokenizer
        """
        if self.__check_type():
            var_type = self.__tokenizer.get_value()  # gets the variable's type
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
            var_name = self.__tokenizer.get_value()  # gets the variable's name
            self.__symbol_table.define(var_name, var_type, ARG_SEGMENT_KEYWORD)  # add the variable to the symbol table

            # adds all additional parameters to the symbol table
            while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):  # "," more varName
                self.__check_type()
                var_type = self.__tokenizer.get_value()  # gets the variable's type
                self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
                var_name = self.__tokenizer.get_value()  # gets the variable's name
                # add the variable to the symbol table
                self.__symbol_table.define(var_name, var_type, ARG_SEGMENT_KEYWORD)

    def __compile_var_dec(self):
        """
        checks if the current token is set to variable declaration, If so, returns true and writes the tokens
        to the stream. Otherwise, doesn't write to the stream, and returns False
        :return: number of variables that were declared. If the current token is not set to the beginning of
        variable declaration, returns 0
        """
        vars_amount = 0
        # checks if the current token is set to 'var', which means it is a var declaration
        if not self.__check_keyword_symbol(KEYWORD_TYPE, VAR_KEYWORDS):  # 'var'
            return vars_amount

        vars_amount += 1  # first variable declaration
        self.__check_type()
        var_type = self.__tokenizer.get_value()

        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # variableName
        var_name = self.__tokenizer.get_value()
        self.__symbol_table.define(var_name, var_type, VAR_SEGMENT_KEYWORD)  # add the variable to symbol table

        # adds all additional variables to the symbol table
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):
            vars_amount += 1  # more variable declarations
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # variableName
            var_name = self.__tokenizer.get_value()
            self.__symbol_table.define(var_name, var_type, VAR_SEGMENT_KEYWORD)

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'
        return vars_amount

    def __compile_statements(self):
        """
        compiles the statements inside a subroutine.
        Assumes the tokenizer is advanced for the first call.
        """
        # compiling all statements
        while self.__check_keyword_symbol(KEYWORD_TYPE, STATEMENTS_LIST, False):
            # checking which statement to compile
            if self.__tokenizer.get_value() == LET_KEYWORD:
                self.__compile_let()
            elif self.__tokenizer.get_value() == DO_KEYWORD:
                self.__compile_do()
            elif self.__tokenizer.get_value() == WHILE_KEYWORD:
                self.__compile_while()
            elif self.__tokenizer.get_value() == RETURN_KEYWORD:
                self.__compile_return()
            else:
                self.__compile_if()

    def __compile_do(self):
        """
        Compiles a do statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end
        """
        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'do'

        # advance the tokenizer for the subroutine call
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # identifier that would be operate on
        self.__check_subroutine_call()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'

        self.__advance_tokenizer()

    def __compile_let(self):
        """
        Compiles a let statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'let'

        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
        left_side_var = self.__tokenizer.get_value()
        # left_side_type = self.__symbol_table.get_type_of(left_side_var)
        # left_side_kind = self.__symbol_table.get_kind_of(self.__tokenizer.get_value())
        # compile the left side of the equation
        # self.__advance_tokenizer()
        # self.__compile_expression()
        # self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '='

        # compile the left side of the equation
        # if self.__symbol_table.get_type_of(left_side_var) == ARRAY_TYPE:
        if self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_ARRAY_ACCESS_BRACKET]):  # array access, if not: =
            self.__analyze_array_var(left_side_var)
            self.__check_keyword_symbol(SYMBOL_TYPE)  # '='
        # else:  # with calling advance
        #     self.__check_keyword_symbol(SYMBOL_TYPE)  # '='

        # if self.__check_keyword_symbol(SYMBOL_TYPE, OPEN_ARRAY_ACCESS_BRACKET):  # '['
        #     # advance the tokenizer for the expression
        #     self.__advance_tokenizer()
        #     self.__compile_expression()
        #     self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ']'
        #     self.__check_keyword_symbol(SYMBOL_TYPE)  # '='
        # else:  # without calling advance
        #     self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '='

        # # compile the left side of the equation
        # self.__advance_tokenizer()
        # self.__compile_expression()
        # self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '='

        # compile the right side of the equation
        self.__advance_tokenizer()  # advance the tokenizer for the expression
        self.__compile_expression()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'
        self.__advance_tokenizer()

        # assign the right side of the equation (that is in the stack) into the left side
        if self.__symbol_table.get_type_of(left_side_var) == ARRAY_TYPE:
            # assign into an array
            self.__writer.write_pop(TEMP_SEGMENT, 0)
            self.__writer.write_pop(POINTER_SEGMENT, THAT_POINTER_INDEX)
            self.__writer.write_push(TEMP_SEGMENT, 0)
            self.__writer.write_pop(THAT_SEGMENT, 0)
        else:
            # assign into any other variable directly
            self.__writer.write_pop(self.__symbol_table.get_kind_of(left_side_var),
                                    self.__symbol_table.get_index_of(left_side_var))

    def __compile_while(self):
        """
        Compiles a while statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'while'
        self.__check_keyword_symbol(SYMBOL_TYPE)  # '('

        # writes the loop label
        start_loop_label = self.__label_counter
        self.__label_counter += 1
        self.__writer.write_label(start_loop_label)
        # advance the tokenizer for the expression
        self.__advance_tokenizer()
        self.__compile_expression()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'
        self.__writer.write_arithmetic(NOT_OPERATOR, True)
        # if the expression is false, goto the next label
        end_loop_label = self.__label_counter
        self.__label_counter += 1
        self.__writer.write_if(end_loop_label)

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'
        # advance the tokenizer for the statements
        self.__advance_tokenizer()
        self.__compile_statements()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'

        self.__advance_tokenizer()

        # goes back to the top of the label
        self.__writer.write_goto(start_loop_label)
        self.__writer.write_label(end_loop_label)  # writes the end loop label

    def __compile_return(self):
        """
        Compiles a return statement.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'return'

        if not self.__check_keyword_symbol(SYMBOL_TYPE, [END_LINE_MARK]):
            if self.__tokenizer.get_value() == THIS_CONSTANT and \
                            self.__symbol_table.get_type_of(THIS_CONSTANT) is None:
                # returning this in the constructor - push pointer 0
                self.__writer.write_push(POINTER_SEGMENT, THIS_POINTER_INDEX)
                self.__advance_tokenizer()
            else:
                # returning an expression
                self.__compile_expression()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'
        else:
            # return void - push a junk constant 0 for a return value
            self.__writer.write_push(CONSTANT_SEGMENT, 0)

        self.__advance_tokenizer()

        self.__writer.write_return()

    def __compile_if(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        Assumes the tokenizer is advanced for the first call.
        Advance the tokenizer at the end.
        """
        self.__check_keyword_symbol(KEYWORD_TYPE, make_advance=False)  # 'if'

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '('
        # advance the tokenizer for the expression
        self.__advance_tokenizer()
        self.__compile_expression()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'
        self.__writer.write_arithmetic(NOT_OPERATOR, True)
        # if the expression is false, goto the next label (else label)
        else_label = self.__label_counter
        self.__label_counter += 1
        self.__writer.write_if(else_label)

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'
        # advance the tokenizer for the statements
        self.__advance_tokenizer()
        self.__compile_statements()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'

        end_if_label = self.__label_counter
        self.__label_counter += 1
        self.__writer.write_goto(end_if_label)  # goto the end of the if statement

        self.__writer.write_label(else_label)  # writes else label
        if self.__check_keyword_symbol(KEYWORD_TYPE, [ELSE_KEYWORD]):  # 'else'
            self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'
            # advance the tokenizer for the statements
            self.__advance_tokenizer()
            self.__compile_statements()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # '}'
            self.__advance_tokenizer()

        self.__writer.write_label(end_if_label)  # write the end if statement label

    def __compile_expression(self):
        """
        compiles an expression
        Assumes the tokenizer is advanced for the first call.
        Advances the tokenizer at the end
        """
        # compiles the first term
        self.__compile_term()

        # compiles all the op + term that exists
        while self.__check_op(False):
            op = self.__tokenizer.get_value()
            self.__advance_tokenizer()
            self.__compile_term()
            self.__writer.write_arithmetic(op)

    def __compile_term(self):
        """
        compiles a term
        Assumes the tokenizer is advanced for the first call.
        Advances the tokenizer at the end
        """
        # checks for all the term options:
        # integer constant
        if self.__tokenizer.get_token_type() == INTEGER_CONST_TYPE:
            self.__writer.write_push(CONSTANT_SEGMENT, int(self.__tokenizer.get_value()))
            self.__advance_tokenizer()
        # string constant
        elif self.__tokenizer.get_token_type() in STRING_CONST_TYPE:
            self.__compile_string_constant()
            self.__advance_tokenizer()
        # keyword constant
        elif self.__check_keyword_symbol(KEYWORD_TYPE, KEYWORD_CONSTANT_LIST, False):
            if self.__tokenizer.get_value() == THIS_CONSTANT:  # push this
                self.__writer.write_push(POINTER_SEGMENT, 0)
            elif self.__tokenizer.get_value() == TRUE_CONSTANT:  # push -1
                self.__writer.write_push(CONSTANT_SEGMENT, 1)
                self.__writer.write_arithmetic(MINUS, True)
            else:  # false/null- push 0
                self.__writer.write_push(CONSTANT_SEGMENT, 0)
            self.__advance_tokenizer()
        # (expression)
        elif self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_BRACKET], False):
            self.__advance_tokenizer()
            self.__compile_expression()
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'
            self.__advance_tokenizer()
        # unaryOp + term
        elif self.__check_unary_op(False):
            op = self.__tokenizer.get_value()
            self.__advance_tokenizer()
            self.__compile_term()
            self.__writer.write_arithmetic(op, True)
        # varName / varName[expression] / subroutineCall- in any case, starts with identifier
        else:
            # self.__check_keyword_symbol(IDENTIFIER_TYPE)
            identifier_name = self.__tokenizer.get_value()
            # checks for function/method call
            if self.__check_subroutine_call():
                return
            # varName[expression]
            if self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_ARRAY_ACCESS_BRACKET], False):
                self.__analyze_array_var(identifier_name)
                self.__writer.write_pop(POINTER_SEGMENT, THAT_POINTER_INDEX)  # pop pointer 1
                self.__writer.write_push(THAT_SEGMENT, 0)  # push that 0
                self.__advance_tokenizer()
            # varName
            else:
                self.__push_var(identifier_name)  # push the var

    def __analyze_array_var(self, identifier_name):
        """
        varName[expression]
        operate varName + expression
        :param identifier_name: the variable'a name
        """
        self.__push_var(identifier_name)  # push the var
        self.__advance_tokenizer()
        self.__compile_expression()  # push the expression
        self.__writer.write_arithmetic(PLUS)  # varName + expression
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ']'

    def __compile_string_constant(self):
        """
        compiles a string constant
        """
        str_const = repr(self.__tokenizer.get_value())[1:-1]
        str_len = len(str_const)
        self.__writer.write_push(CONSTANT_SEGMENT, str_len)
        self.__writer.write_call(STRING_CONSTRUCTOR, STRING_CONSTRUCT_NUM_ARGS)
        for char in str_const:
            self.__writer.write_push(CONSTANT_SEGMENT, ord(char))  # push the char ASCII code
            self.__writer.write_call(STRING_APPEND, STRING_APPEND_NUM_ARGS)

    def __push_var(self, var_name):
        """
        writes a push var command to the output stream to the
        :param var_name: the variable name to push to the stack
        """
        self.__writer.write_push(self.__symbol_table.get_kind_of(var_name),
                                 self.__symbol_table.get_index_of(var_name))

    def __check_subroutine_call(self):
        """
        checks if the next tokens are subroutine call. If so, writes the vm commands for the subroutine call.
        Advances the tokenizer at the end
        :return: true iff the next tokens are subroutine calls
        """
        num_args = 0
        call_name = ""
        identifier = self.__tokenizer.get_value()
        # checks if the next token is '(' : regular subroutine call
        if self.__check_keyword_symbol(SYMBOL_TYPE, [OPEN_BRACKET]):
            call_name += self.__class_name + CALL_CLASS_METHOD_MARK + identifier
        # checks if the next token is '.' : function/method call
        elif self.__check_keyword_symbol(SYMBOL_TYPE, [CALL_CLASS_METHOD_MARK], False):
            # a variable- method call
            if self.__symbol_table.get_index_of(identifier) is not None:
                var_type = self.__symbol_table.get_type_of(identifier)
                call_name += var_type
                num_args += 1  # the extra 'this' arg
                # push this
                self.__push_var(identifier)
            # function/ constructor call
            else:
                call_name += identifier

            self.__advance_tokenizer()
            func_name = self.__tokenizer.get_value()
            call_name += CALL_CLASS_METHOD_MARK + func_name
            self.__check_keyword_symbol(SYMBOL_TYPE)  # '('
        # if the next token is not ( or . : not a subroutine call
        else:
            return False

        # pushing all args
        num_args += self.__compile_expression_list()
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ')'
        # calling the function
        self.__writer.write_call(call_name, num_args)

        self.__advance_tokenizer()
        return True

    def __compile_expression_list(self):
        """
        compiles an expression list
        :return: the number of expressions compiled
        """
        exp_counter = 0
        self.__advance_tokenizer()

        # if the expression list is not empty: compile all the expression
        if self.__tokenizer.get_value() != CLOSE_BRACKET:
            exp_counter += 1
            # compiles the first expression
            self.__compile_expression()

            # checks for more expressions separated with comma
            while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK], False):
                exp_counter += 1
                # advances the tokenizer
                self.__advance_tokenizer()
                # compiles the next expression
                self.__compile_expression()

        return exp_counter

    def __check_keyword_symbol(self, token_type, value_list=None, make_advance=True):
        """
        checks if the current token is from token_type (which is keyword or symbol), and it's value is one of the
        given optional values (in the value_list).
        :param token_type: the wanted type of the current token: keyword or symbol
        :param value_list: a list of optional values for the current token
        :param make_advance: whether or not the method should call tokenizer.advance() at the beginning
        :return: True if the current token is from Keyword type, and it's value exists in the keyword list,
          and false otherwise
        """
        if make_advance:
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
            else:
                return False
        if self.__tokenizer.get_token_type() == token_type:
            if value_list is None or self.__tokenizer.get_value() in value_list:
                return True

        return False

    def __check_type(self, make_advance=True):
        """
        checks if the current token is a type.
        :param make_advance: whether or not the method should call tokenizer.advance() at the beginning
        :return: true iff the current token is a type
        """
        # checks for builtin types
        if self.__check_keyword_symbol(KEYWORD_TYPE, TYPE_LIST, make_advance):
            return True
        # checks for user-defined class types
        if not self.__check_keyword_symbol(IDENTIFIER_TYPE, make_advance=False):
            return False

        return True

    def __check_op(self, make_advance=True):
        """
        :return: true iff the current token is a symbol containing an operation
        """
        return self.__check_keyword_symbol(SYMBOL_TYPE, OP_LIST, make_advance)

    def __check_unary_op(self, make_advance=True):
        """
        :return: true iff the current token is a symbol containing an unary operation
        """
        return self.__check_keyword_symbol(SYMBOL_TYPE, UNARY_OP_LIST, make_advance)

    def __advance_tokenizer(self):
        """
        advances the inner tokenizer in case when there must be more tokens
        """
        self.__tokenizer.has_more_tokens()  # when there must be more tokens, otherwise the input is invalid
        self.__tokenizer.advance()
