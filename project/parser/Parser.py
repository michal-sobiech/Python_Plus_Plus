from typing import Optional

from project.lexer.Lexer import Lexer

from project.parser.ast_nodes.conditional_statements.ConditionalStatement import ConditionalStatement
from project.parser.ast_nodes.conditional_statements.ElifStatement import ElifStatement
from project.parser.ast_nodes.conditional_statements.ElseStatement import ElseStatement
from project.parser.ast_nodes.conditional_statements.IfStatement import IfStatement

from project.parser.ast_nodes.dict.Dict import Dict
from project.parser.ast_nodes.dict.DictElement import DictElement
from project.parser.ast_nodes.dict.Pair import Pair

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.function.call.FunctionCall import FunctionCall

from project.parser.ast_nodes.function.definition.FunctionDefinition import FunctionDefinition

from project.parser.ast_nodes.incr_decr_statement.DecrementStatement import DecrementStatement
from project.parser.ast_nodes.incr_decr_statement.IncrementStatement import IncrementStatement

from project.parser.ast_nodes.linq.LinqQuery import LinqQuery

from project.parser.ast_nodes.list.List import List

from project.parser.ast_nodes.literal.BoolLiteral import BoolLiteral
from project.parser.ast_nodes.literal.FloatLiteral import FloatLiteral
from project.parser.ast_nodes.literal.IntLiteral import IntLiteral
from project.parser.ast_nodes.literal.StringLiteral import StringLiteral

from project.parser.ast_nodes.operator_terms.add_or_sub_term.AdditionTerm import AdditionTerm
from project.parser.ast_nodes.operator_terms.add_or_sub_term.SubtractionTerm import SubtractionTerm

from project.parser.ast_nodes.operator_terms.and_term.AndTerm import AndTerm

from project.parser.ast_nodes.operator_terms.comparison_term.CompTermABC import CompTermABC
from project.parser.ast_nodes.operator_terms.comparison_term.EqualTerm import EqualTerm
from project.parser.ast_nodes.operator_terms.comparison_term.GreaterEqualTerm import GreaterEqualTerm
from project.parser.ast_nodes.operator_terms.comparison_term.GreaterTerm import GreaterTerm
from project.parser.ast_nodes.operator_terms.comparison_term.LessEqualTerm import LessEqualTerm
from project.parser.ast_nodes.operator_terms.comparison_term.LessTerm import LessTerm

from project.parser.ast_nodes.operator_terms.mul_or_div_term.MulOrDivTermABC import MulOrDivTermABC
from project.parser.ast_nodes.operator_terms.mul_or_div_term.MultiplicationTerm import MultiplicationTerm
from project.parser.ast_nodes.operator_terms.mul_or_div_term.DivisionTerm import DivisionTerm

from project.parser.ast_nodes.operator_terms.not_term.NotTerm import NotTerm

from project.parser.ast_nodes.operator_terms.or_term.OrTerm import OrTerm

from project.parser.ast_nodes.operator_terms.unary_minus_term.UnaryMinusTerm import UnaryMinusTerm

from project.parser.ast_nodes.operator_terms.DotTerm import DotTerm

from project.parser.ast_nodes.return_statement.ReturnABC import ReturnABC
from project.parser.ast_nodes.return_statement.ReturnNoValue import ReturnNoValue
from project.parser.ast_nodes.return_statement.ReturnWithValue import ReturnWithValue

from project.parser.ast_nodes.Assignment import Assignment
from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.ForLoop import ForLoop
from project.parser.ast_nodes.FunDefOrStatementABC import FunDefOrStatementABC
from project.parser.ast_nodes.Identifier import Identifier
from project.parser.ast_nodes.StatementABC import StatementABC
from project.parser.ast_nodes.WhileLoop import WhileLoop

from project.parser.exceptions.SyntaxError import SyntaxError
from project.parser.exceptions.SyntaxErrorMsg import SyntaxErrorMsg

from project.token.Token import Token
from project.token.ValueToken import ValueToken
from project.token.TokenType import TokenType

from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.literal.NoneLiteral import NoneLiteral

from project.interpreter.ErrorHandler import ErrorHandler


class Parser:
    __slots__ = [
        '_lexer',
        '_token',
        '_error_handler'
    ]

    def __init__(self, lexer: Lexer, error_handler: ErrorHandler) -> None:
        self._lexer = lexer
        self._token: Token = None
        self._error_handler = error_handler

    def _consume_token(self) -> None:
        self._token = self._lexer.get_next_token()

    def _raise_syntax_error(
        self,
        code: SyntaxErrorMsg
    ) -> None:
        raise SyntaxError(code, self._token.position)

    def _must_be(
        self,
        token_type: TokenType,
        exception_code: SyntaxErrorMsg
    ) -> Optional[tuple[object, PositionInCode]]:

        if self._token.type != token_type:
            self._raise_syntax_error(exception_code)

        position = None
        value = None
        if type(self._token) is ValueToken:
            position = self._token.position
            value = self._token.value
        self._consume_token()
        return position, value

    # code = { fun_definition | statement };
    def parse_code(self) -> Code:

        try:
            fun_defs_and_statments: list[FunDefOrStatementABC] = []

            self._consume_token()

            while self._token.type != TokenType.END_OF_FILE:

                if (fun_def := self._parse_fun_def()) is not None:
                    fun_defs_and_statments.append(fun_def)

                elif (statement := self._parse_statement()) is not None:
                    fun_defs_and_statments.append(statement)

                else:
                    self._raise_syntax_error(
                        SyntaxErrorMsg.NEITHER_FUN_DEF_NOR_STATEMENT
                    )

            return Code(fun_defs_and_statments)

        except SyntaxError as error:
            self._error_handler.handle_parser_error(error)

    # fun_definition = "def", id, "(", fun_params, ")", block;
    def _parse_fun_def(self) -> Optional[FunctionDefinition]:

        if self._token.type != TokenType.DEF:
            return None
        position = self._token.position
        self._consume_token()

        function_name = Identifier(
            *self._must_be(
                TokenType.IDENTIFIER,
                SyntaxErrorMsg.FUN_INVALID_NAME
            )
        )

        self._must_be(
            TokenType.PARENTHESES_LEFT,
            SyntaxErrorMsg.FUN_NO_LEFT_PARENTHESES
        )

        if (parameters := self._parse_fun_params()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.FUN_DEF_INVALID_PARAM)

        self._must_be(
            TokenType.PARENTHESES_RIGHT,
            SyntaxErrorMsg.FUN_NO_RIGHT_PARENTHESES
        )

        if (body := self._parse_block()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.FUN_DEF_INVALID_BODY)

        return FunctionDefinition(
            position,
            function_name,
            parameters,
            body
        )

    # fun_params = [ id { ",", id } ];
    def _parse_fun_params(self) -> Optional[list[Identifier]]:

        parameters: list[Identifier] = []

        if self._token.type == TokenType.IDENTIFIER:
            parameters.append(Identifier(
                self._token.position, self._token.value
            ))
            self._consume_token()

            while self._token.type == TokenType.COMMA:
                self._consume_token()

                param = Identifier(*self._must_be(
                    TokenType.IDENTIFIER,
                    SyntaxErrorMsg.FUN_DEF_INVALID_PARAM
                ))
                parameters.append(param)

        return parameters

    # block = "{", { statement }, "}";
    def _parse_block(self) -> Optional[Block]:

        statement_list: list[StatementABC] = []

        if self._token.type != TokenType.BRACES_LEFT:
            return None
        position = self._token.position
        self._consume_token()

        while (statement := self._parse_statement()) is not None:
            statement_list.append(statement)

        self._must_be(
            TokenType.BRACES_RIGHT,
            SyntaxErrorMsg.BLOCK_NO_RIGHT_BRACES
        )

        return Block(position, statement_list)

    # cond_statement = if_statement, { elif_statement }, [ else_statement ];
    def _parse_conditional_statement(self) -> Optional[ConditionalStatement]:

        elif_statements: list[ElifStatement] = []

        if (if_statement := self._parse_if_statement()) is None:
            return None
        position = if_statement.position

        while (elif_statement := self._parse_elif_statement()) is not None:
            elif_statements.append(elif_statement)

        else_statement = self._parse_else_statement()

        return ConditionalStatement(
            position,
            if_statement,
            elif_statements,
            else_statement
        )

    # if_statement = "if", expression, block;
    def _parse_if_statement(self) -> Optional[IfStatement]:

        if self._token.type != TokenType.IF:
            return None
        position = self._token.position
        self._consume_token()

        if (condition := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.IF_INVALID_CONDITION)

        if (body := self._parse_block()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.IF_INVALID_BODY)

        return IfStatement(position, condition, body)

    # elif_statement = "elif", expression, block;
    def _parse_elif_statement(self) -> Optional[ElifStatement]:

        if self._token.type != TokenType.ELIF:
            return None
        position = self._token.position
        self._consume_token()

        if (condition := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.ELIF_INVALID_CONDITION)

        if (body := self._parse_block()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.ELIF_INVALID_BODY)

        return ElifStatement(position, condition, body)

    # else_statement = "else", block;
    def _parse_else_statement(self) -> ElseStatement:

        if self._token.type != TokenType.ELSE:
            return None
        position = self._token.position
        self._consume_token()

        if (body := self._parse_block()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.ELSE_INVALID_BODY)

        return ElseStatement(position, body)

    # assign_or_expr_or_incrdecr = expression, [ '=', expression
    #                            | ( "++" | "--" ) ];
    def _parse_assignment_or_expr_or_incr_decr(self) -> Optional[StatementABC]:

        if (expression := self._parse_expression()) is None:
            return None
        position = expression.position

        match self._token.type:
            case TokenType.EQUALS:
                self._consume_token()

                if (right_expression := self._parse_expression()) is None:
                    self._raise_syntax_error(SyntaxErrorMsg.ASSIGN_INVALID_RIGHT_SIDE)

                return Assignment(position, expression, right_expression)

            case TokenType.PLUS_PLUS:
                self._consume_token()

                return IncrementStatement(position, expression)

            case TokenType.MINUS_MINUS:
                self._consume_token()

                return DecrementStatement(position, expression)

            case _:
                return expression

    # statement = assign_or_incrdecr, ";"
    #           | return, ";"
    #           | cond_statement,
    #           | for_loop
    #           | while_loop;
    def _parse_statement(self) -> Optional[StatementABC]:

        semicolon_statement = (
            self._parse_assignment_or_expr_or_incr_decr()
            or self._parse_return_statement()
        )
        if semicolon_statement is not None:

            self._must_be(
                TokenType.SEMICOLON,
                SyntaxErrorMsg.NO_SEMICOLON
            )
            return semicolon_statement

        no_semicolon_statement = (
            self._parse_conditional_statement()
            or self._parse_for_loop()
            or self._parse_while_loop()
        )
        if no_semicolon_statement is not None:

            return no_semicolon_statement

        return None

    # expression = and_term, { "or", and_term };
    def _parse_expression(self) -> Optional[ExpressionABC]:

        if (left_term := self._parse_and_term()) is None:
            return None
        position = left_term.position

        if self._token.type == TokenType.OR:
            self._consume_token()

            if (right_term := self._parse_expression()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.OR_TERM_INVALID_RIGHT_SIDE
                )

            return OrTerm(position, left_term, right_term)

        else:
            return left_term

    # and_term = not_term, { "and", not_term };
    def _parse_and_term(self) -> Optional[ExpressionABC]:

        if (left_term := self._parse_not_term()) is None:
            return None
        position = left_term.position

        if self._token.type == TokenType.AND:
            self._consume_token()

            if (right_term := self._parse_and_term()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.AND_TERM_INVALID_RIGHT_SIDE
                )

            return AndTerm(position, left_term, right_term)

        else:
            return left_term

    # not_term = [ "not" ], comp_term;
    def _parse_not_term(self) -> Optional[ExpressionABC]:

        if self._token.type == TokenType.NOT:
            position = self._token.position
            self._consume_token()

            if (term := self._parse_comp_term()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.NOT_TERM_INVALID_RIGHT_SIDE
                )

            return NotTerm(position, term)

        elif (term := self._parse_comp_term()) is not None:
            return term

        return None

    # comp_term = add_or_sub_term, [ comp_operator, add_or_sub_term ];
    def _parse_comp_term(self) -> Optional[ExpressionABC]:

        if (left_term := self._parse_add_or_sub_term()) is None:
            return None
        position = left_term.position

        classes = {
            TokenType.GREATER: GreaterTerm,
            TokenType.GREATER_EQUALS: GreaterEqualTerm,
            TokenType.LESS: LessTerm,
            TokenType.LESS_EQUALS: LessEqualTerm,
            TokenType.EQUALS_EQUALS: EqualTerm
        }
        if (right_term_class := classes.get(self._token.type)) is not None:
            self._consume_token()

            if (right_term := self._parse_add_or_sub_term()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.COMP_TERM_INVALID_RIGHT_SIDE)

            return right_term_class(position, left_term, right_term)

        else:
            return left_term

    # add_or_sub_term = mul_or_div_term, { ("+" | "-"), mul_or_div_term };
    def _parse_add_or_sub_term(self) -> Optional[ExpressionABC]:

        if (left_term := self._parse_mul_or_div_term()) is None:
            return None
        position = left_term.position

        classes = {
            TokenType.PLUS: AdditionTerm,
            TokenType.MINUS: SubtractionTerm
        }
        if (right_term_class := classes.get(self._token.type)) is not None:
            self._consume_token()

            if (right_term := self._parse_add_or_sub_term()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.ADD_OR_SUB_TERM_INVALID_RIGHT_SIDE,
                )

            else:
                return right_term_class(position, left_term, right_term)

        else:
            return left_term

    # mul_or_div_term = unary_minus_term, { ("*" | "/"), unary_minus_term };
    def _parse_mul_or_div_term(self) -> Optional[ExpressionABC]:

        if (term := self._parse_unary_minus_term()) is None:
            return None
        position = term.position

        classes = {
            TokenType.MULTIPLY: MultiplicationTerm,
            TokenType.DIVIDE: DivisionTerm
        }
        if (right_term_class := classes.get(self._token.type)) is not None:
            self._consume_token()

            if (right_term := self._parse_mul_or_div_term()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.MINUS_TERM_INVALID_RIGHT_SIDE
                )

            else:
                return right_term_class(position, term, right_term)

        else:
            return term

    # unary_minus_term = [ "-" ], dot_term;
    def _parse_unary_minus_term(self) -> Optional[ExpressionABC]:

        if self._token.type == TokenType.MINUS:
            position = self._token.position
            self._consume_token()

            if (term := self._parse_dot_term()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.NOT_TERM_INVALID_RIGHT_SIDE
                )

            return UnaryMinusTerm(position, term)

        elif (term := self._parse_dot_term()) is not None:
            return term

        return None

    # dot_term = term, { ".", term };
    def _parse_dot_term(self) -> Optional[ExpressionABC]:

        term_list: list[ExpressionABC] = []

        if (term := self._parse_term()) is None:
            return None
        position = term.position
        term_list.append(term)

        if self._token.type != TokenType.DOT:
            return term

        while self._token.type == TokenType.DOT:
            self._consume_token()

            if (term := self._parse_term()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.DOT_TERM_INVALID_TERM)
            term_list.append(term)

        return DotTerm(position, term_list)

    # term = literal
    #      | list
    #      | dict_or_pair
    #      | id_or_fun_call
    #      | nested_expression
    #      | linq_query;
    def _parse_term(self) -> Optional[ExpressionABC]:

        if (literal := self._parse_literal()) is not None:
            return literal

        if (collection := self._parse_list()) is not None:
            return collection

        if (dict_or_pair := self._parse_dict_or_pair()) is not None:
            return dict_or_pair

        if (id_or_fun_call := self._parse_id_or_fun_call()) is not None:
            return id_or_fun_call

        if (expression := self._parse_nested_expression()) is not None:
            return expression

        if (linq_query := self._parse_linq_query()) is not None:
            return linq_query

        return None

    # nested_expression = "(", expression, ")";
    def _parse_nested_expression(self) -> Optional[ExpressionABC]:

        if self._token.type != TokenType.PARENTHESES_LEFT:
            return None
        self._consume_token()

        if (expression := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.NESTED_EXPR_INVALID_EXPR)

        self._must_be(
            TokenType.PARENTHESES_RIGHT,
            SyntaxErrorMsg.NESTED_EXPR_NO_RIGHT_PARENTHESES
        )

        return expression

    def _parse_literal(self) -> Optional[ExpressionABC]:

        position = self._token.position

        classes = {
            TokenType.INT_LITERAL: IntLiteral,
            TokenType.FLOAT_LITERAL: FloatLiteral,
            TokenType.STRING_LITERAL: StringLiteral,
        }
        if (term_class := classes.get(self._token.type)) is not None:
            term = term_class(position, self._token.value)
            self._consume_token()
            return term

        elif self._token.type == TokenType.TRUE:
            self._consume_token()
            return BoolLiteral(position, True)

        elif self._token.type == TokenType.FALSE:
            self._consume_token()
            return BoolLiteral(position, False)

        elif self._token.type == TokenType.NONE:
            self._consume_token()
            return NoneLiteral(position)

        else:
            return None

    # id_or_fun_call = id, [ "(", [ fun_call_args ], ")" ];
    def _parse_id_or_fun_call(self):

        if self._token.type != TokenType.IDENTIFIER:
            return None
        identifier = Identifier(self._token.position, self._token.value)
        self._consume_token()

        if self._token.type != TokenType.PARENTHESES_LEFT:
            return identifier

        else:
            self._consume_token()

            if (args := self._parse_fun_args()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.FUN_CALL_INVALID_ARG)

            self._must_be(
                TokenType.PARENTHESES_RIGHT,
                SyntaxErrorMsg.FUN_NO_RIGHT_PARENTHESES
            )

            return FunctionCall(identifier.position, identifier, args)

    # fun_args = expression, { ",", expression };
    def _parse_fun_args(self) -> Optional[list[ExpressionABC]]:

        arguments: list[ExpressionABC] = []

        if (first_arg := self._parse_expression()) is None:
            return arguments
        arguments.append(first_arg)

        while self._token.type == TokenType.COMMA:
            self._consume_token()

            if (other_arg := self._parse_expression()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.FUN_CALL_INVALID_ARG)
            arguments.append(other_arg)

        return arguments

    # linq_query = "from", expression, "in", expression, "where", expression,
    #            [ "orderby", expression ],
    #            "select", expression, { ",", expression };
    def _parse_linq_query(self) -> Optional[LinqQuery]:

        sorting_function: ExpressionABC = None
        selected_values: list[ExpressionABC] = []

        if self._token.type != TokenType.FROM:
            return None
        position = self._token.position
        self._consume_token()

        iterator_var = Identifier(
            *self._must_be(
                TokenType.IDENTIFIER,
                SyntaxErrorMsg.LINQ_INVALID_ITERATOR_VAR
            )
        )

        self._must_be(
            TokenType.IN,
            SyntaxErrorMsg.LINQ_NO_IN
        )

        if (source := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.LINQ_INVALID_SEQUENCE)

        self._must_be(
            TokenType.WHERE,
            SyntaxErrorMsg.LINQ_NO_WHERE
        )

        if (condition := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.LINQ_INVALID_CONDITION)

        if self._token.type == TokenType.ORDERBY:
            self._consume_token()

            if (sorting_function := self._parse_expression()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.LINQ_NO_ORDERBY_FUN)

        self._must_be(
            TokenType.SELECT,
            SyntaxErrorMsg.LINQ_NO_SELECT
        )

        if (selected_val := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.LINQ_INVALID_SELECTED_VALUES)
        selected_values.append(selected_val)

        while self._token.type == TokenType.COMMA:
            self._consume_token()

            if (selected_val := self._parse_expression()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.LINQ_SELECTED_VALUES_END_WITH_COMMA
                )
            selected_values.append(selected_val)

        return LinqQuery(
            position,
            iterator_var,
            source,
            condition,
            sorting_function,
            selected_values
        )

    # for_loop = "for", id, "in", expression, block;
    def _parse_for_loop(self) -> Optional[ForLoop]:

        if self._token.type != TokenType.FOR:
            return None
        position = self._token.position
        self._consume_token()

        iterator = Identifier(
            *self._must_be(
                TokenType.IDENTIFIER,
                SyntaxErrorMsg.FOR_LOOP_INVALID_ITERATOR_VAR
            )
        )

        self._must_be(
            TokenType.IN,
            SyntaxErrorMsg.FOR_LOOP_NO_IN
        )

        if (sequence := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.FOR_LOOP_INVALID_SEQUENCE)

        if (body := self._parse_block()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.FOR_LOOP_INVALID_BODY)

        return ForLoop(
            position,
            iterator,
            sequence,
            body
        )

    # while_loop = "while", expression, block;
    def _parse_while_loop(self) -> Optional[WhileLoop]:

        if self._token.type != TokenType.WHILE:
            return None
        position = self._token.position
        self._consume_token()

        if (condition := self._parse_expression()) is None:
            self._raise_syntax_error(
                SyntaxErrorMsg.WHILE_LOOP_INVALID_CONDITION
            )

        if (body := self._parse_block()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.WHILE_LOOP_INVALID_BODY)

        return WhileLoop(position, condition, body)

    # return = "return", [ expression ];
    def _parse_return_statement(self) -> Optional[ReturnABC]:

        if self._token.type != TokenType.RETURN:
            return None
        position = self._token.position
        self._consume_token()

        if (ret_val := self._parse_expression()) is None:
            return ReturnNoValue(position)

        else:
            return ReturnWithValue(position, ret_val)

    # dict_or_pair = "{", ( "}"
    #              | (expression, (",", expression
    #              | ":", expression, [ dict_elems ] ), "}" ) );
    def _parse_dict_or_pair(self) -> Optional[Dict | Pair]:

        if self._token.type != TokenType.BRACES_LEFT:
            return None
        position = self._token.position
        self._consume_token()

        if (key := self._parse_expression()) is None:

            self._must_be(
                TokenType.BRACES_RIGHT,
                SyntaxErrorMsg.DICT_NO_RIGHT_BRACES
            )

            return Dict(position, [])

        first_dict_elem_pos = key.position

        if self._token.type == TokenType.COMMA:
            # Pair

            self._consume_token()

            if (value := self._parse_expression()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.PAIR_INVALID_VALUE)

            self._must_be(
                TokenType.BRACES_RIGHT,
                SyntaxErrorMsg.PAIR_NO_RIGHT_BRACES
            )

            return Pair(position, key, value)

        if self._token.type == TokenType.COLON:
            # Dict

            self._consume_token()

            elems: list[DictElement] = []

            if (value := self._parse_expression()) is None:
                self._raise_syntax_error(
                    SyntaxErrorMsg.DICT_ELEM_INVALID_VALUE
                )
            elems.append(DictElement(first_dict_elem_pos, key, value))

            if self._token.type != TokenType.COMMA:

                self._must_be(
                    TokenType.BRACES_RIGHT,
                    SyntaxErrorMsg.DICT_NO_RIGHT_BRACES
                )

                return Dict(position, elems)

            self._consume_token()

            if (other_dict_elems := self._parse_dict_elements()) is not None:
                elems += other_dict_elems

            self._must_be(
                TokenType.BRACES_RIGHT,
                SyntaxErrorMsg.DICT_NO_RIGHT_BRACES
            )

            return Dict(position, elems)

        return None

    # dict_elems = dict_element, { ",", dict_element };
    def _parse_dict_elements(self) -> Optional[list[DictElement]]:

        elems: list[DictElement] = []

        if (element := self._parse_dict_element()) is None:
            return None
        elems.append(element)

        while self._token.type == TokenType.COMMA:
            self._consume_token()

            if (element := self._parse_dict_element()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.INVALID_DICT_ELEM)
            elems.append(element)

        return elems

    # dict_element = expression, ":", expression;
    def _parse_dict_element(self) -> Optional[DictElement]:

        if (key := self._parse_expression()) is None:
            return None
        position = key.position

        self._must_be(
            TokenType.COLON,
            SyntaxErrorMsg.DICT_ELEM_NO_COLON
        )

        if (value := self._parse_expression()) is None:
            self._raise_syntax_error(SyntaxErrorMsg.DICT_ELEM_INVALID_VALUE)

        return DictElement(position, key, value)

    # list = "[", [ list_elems ], "]";
    def _parse_list(self) -> Optional[List]:

        if self._token.type != TokenType.BRACKETS_LEFT:
            return None
        position = self._token.position
        self._consume_token()

        elements = self._parse_list_elements()
        elements = [] if elements is None else elements

        self._must_be(
            TokenType.BRACKETS_RIGHT,
            SyntaxErrorMsg.LIST_NO_RIGHT_BRACKETS
        )

        return List(position, elements)

    # list_elems = list_element, { ",", list_element };
    def _parse_list_elements(self) -> Optional[list[ExpressionABC]]:

        elements: list[ExpressionABC] = []

        if (element := self._parse_expression()) is None:
            return None
        elements.append(element)

        while self._token.type == TokenType.COMMA:
            self._consume_token()

            if (element := self._parse_expression()) is None:
                self._raise_syntax_error(SyntaxErrorMsg.LIST_INVALID_ELEMENT)
            elements.append(element)

        return elements
