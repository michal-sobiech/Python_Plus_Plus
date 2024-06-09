from unittest.mock import patch

from project.parser.Parser import Parser

from project.interpreter.Interpreter import Interpreter

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.Parser import Parser

from project.parser.ast_nodes.Identifier import Identifier

from project.parser.ast_nodes.literal.IntLiteral import IntLiteral

from project.parser.ast_nodes.function.call.FunctionCall import FunctionCall

from project.parser.ast_nodes.operator_terms.add_or_sub_term.AdditionTerm import AdditionTerm

from project.parser.ast_nodes.Code import Code

from typing import Type

from enum import Enum, auto

from typing import Type

from enum import Enum, auto

from project.interpreter.nodes.function.EmbeddedFunction import EmbeddedFunction
from project.interpreter.nodes.function.FunctionABC import FunctionABC
from project.interpreter.nodes.function.InterpretedFunction import InterpretedFunction

from project.interpreter.nodes.variable.Variable import Variable

from project.interpreter.nodes.Context import Context
from project.interpreter.nodes.StructABC import StructABC
from project.interpreter.nodes.variable.Variable import Variable
from project.interpreter.nodes.ObjectName import ObjectName

from project.parser.Parser import Parser

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
from project.parser.ast_nodes.incr_decr_statement.IncrDecrStatementABC import IncrDecrStatementABC
from project.parser.ast_nodes.incr_decr_statement.IncrementStatement import IncrementStatement

from project.parser.ast_nodes.linq.LinqQuery import LinqQuery

from project.parser.ast_nodes.literal.LiteralABC import LiteralABC
from project.parser.ast_nodes.literal.BoolLiteral import BoolLiteral
from project.parser.ast_nodes.literal.FloatLiteral import FloatLiteral
from project.parser.ast_nodes.literal.IntLiteral import IntLiteral
from project.parser.ast_nodes.literal.StringLiteral import StringLiteral

from project.parser.ast_nodes.node.NodeABC import NodeABC

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

from project.parser.ast_nodes.list.List import List

from project.interpreter.nodes.value.LValue import LValue
from project.interpreter.nodes.value.ValueType import ValueType
from project.interpreter.nodes.ValueContainerABC import ValueContainerABC

from project.interpreter.InterpreterError import InterpreterError
from project.interpreter.InterpreterErrorMsg import InterpreterErrorMsg

from tests.interpreter.interpreter_test_utils import (
    variable_creation_test,
    function_definition_test,
    output_stream_test,
    stack_size_test,
    error_raising_test
)

from io import StringIO


def test_def_of_function_without_params() -> None:
    '''
    def a() {}
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))

    body = Block(
        left_braces.position,
        []
    )

    ast = Code(
        [FunctionDefinition(
            def_token.position,
            Identifier(
                a.position,
                a.value,
            ),
            [],
            body
        )]
    )

    function_definition_test(
        ast,
        InterpretedFunction(
            a.value,
            [],
            body
        )
    )


def test_def_of_function_with_params() -> None:
    '''
    def a(b, c) {}
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    b = ValueToken(TokenType.IDENTIFIER, 'b', PositionInCode(1, 7))
    c = ValueToken(TokenType.IDENTIFIER, 'c', PositionInCode(1, 10))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 13))

    body = Block(
        left_braces.position,
        []
    )

    ast = Code(
        [FunctionDefinition(
            def_token.position,
            Identifier(
                a.position,
                a.value,
            ),
            [
                Identifier(
                    b.position,
                    b.value
                ),
                Identifier(
                    c.position,
                    c.value
                )
            ],
            body
        )]
    )

    function_definition_test(
        ast,
        InterpretedFunction(
            a.value,
            [b.value, c.value],
            body
        )
    )


def test_call_of_function_returning_nothing() -> None:
    '''
    def a() {
        return;
    }
    a();
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    fun_def_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))
    return_token = NoValToken(TokenType.RETURN, PositionInCode(2, 4))
    fun_call_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(4, 1))

    body = Block(
        left_braces.position,
        [
            ReturnNoValue(
                return_token.position
            )
        ]
    )

    ast = Code(
        [
            FunctionDefinition(
                def_token.position,
                Identifier(
                    fun_def_name.position,
                    fun_def_name.value,
                ),
                [],
                body
            ),
            FunctionCall(
                fun_call_name.position,
                Identifier(
                    fun_call_name.position,
                    fun_call_name.value
                ),
                []
            )
        ]
    )
    stack_size_test(ast, 1)


def test_call_of_function_returning_a_value() -> None:
    '''
    def a() {
        return 1;
    }
    b = a();
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    fun_def_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))
    return_token = NoValToken(TokenType.RETURN, PositionInCode(2, 4))
    ret_val = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(2, 12))
    b = ValueToken(TokenType.IDENTIFIER, 'b', PositionInCode(4, 1))
    fun_call_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(4, 5))

    body = Block(
        left_braces.position,
        [
            ReturnWithValue(
                return_token.position,
                IntLiteral(
                    ret_val.position,
                    ret_val.value
                )
            )
        ]
    )

    ast = Code(
        [
            FunctionDefinition(
                def_token.position,
                Identifier(
                    fun_def_name.position,
                    fun_def_name.value,
                ),
                [],
                body
            ),
            Assignment(
                b.position,
                Identifier(
                    b.position,
                    b.value
                ),
                FunctionCall(
                    fun_call_name.position,
                    Identifier(
                        fun_call_name.position,
                        fun_call_name.value
                    ),
                    []
                )
            )
        ]
    )

    variable_creation_test(
        ast,
        Variable(
            b.value,
            ValueType.INT,
            ret_val.value
        )
    )


def test_call_of_function_with_no_return_stmt() -> None:
    '''
    def a() {}
    a();
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    fun_def_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))
    fun_call_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(2, 1))

    body = Block(
        left_braces.position,
        []
    )

    ast = Code(
        [
            FunctionDefinition(
                def_token.position,
                Identifier(
                    fun_def_name.position,
                    fun_def_name.value,
                ),
                [],
                body
            ),
            FunctionCall(
                fun_call_name.position,
                Identifier(
                    fun_call_name.position,
                    fun_call_name.value
                ),
                []
            )
        ]
    )
    stack_size_test(ast, 1)


def test_call_of_function_with_multiple_params() -> None:
    '''
    def a(b, c) {}
    a(1, 2);
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    fun_def_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    b = ValueToken(TokenType.IDENTIFIER, 'b', PositionInCode(1, 7))
    c = ValueToken(TokenType.IDENTIFIER, 'c', PositionInCode(1, 10))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))
    fun_call_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(2, 1))
    one = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(2, 3))
    two = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(2, 6))

    body = Block(
        left_braces.position,
        []
    )

    ast = Code(
        [
            FunctionDefinition(
                def_token.position,
                Identifier(
                    fun_def_name.position,
                    fun_def_name.value,
                ),
                [
                    Identifier(
                        b.position,
                        b.value
                    ),
                    Identifier(
                        c.position,
                        c.value
                    )
                ],
                body
            ),
            FunctionCall(
                fun_call_name.position,
                Identifier(
                    fun_call_name.position,
                    fun_call_name.value
                ),
                [
                    IntLiteral(
                        one.position,
                        one.value
                    ),
                    IntLiteral(
                        two.position,
                        two.value
                    )
                ]
            )
        ]
    )
    stack_size_test(ast, 1)


def test_call_of_function_with_invalid_param_count() -> None:
    '''
    def a(b) {}
    a();
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    fun_def_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 5))
    b = ValueToken(TokenType.IDENTIFIER, 'b', PositionInCode(1, 7))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))
    fun_call_name = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(2, 1))

    body = Block(
        left_braces.position,
        []
    )

    ast = Code(
        [
            FunctionDefinition(
                def_token.position,
                Identifier(
                    fun_def_name.position,
                    fun_def_name.value,
                ),
                [
                    Identifier(
                        b.position,
                        b.value
                    )
                ],
                body
            ),
            FunctionCall(
                fun_call_name.position,
                Identifier(
                    fun_call_name.position,
                    fun_call_name.value
                ),
                []
            )
        ]
    )
    error_raising_test(ast, InterpreterErrorMsg.INVALID_ARG_COUNT)


def test_embedded_function_call() -> None:
    '''
    print(1);
    '''

    print_token = ValueToken(TokenType.IDENTIFIER, 'print', PositionInCode(1, 1))
    number = ValueToken(TokenType.INT_LITERAL, 1,   PositionInCode(1, 7))

    ast = Code(
        [FunctionCall(
            print_token.position,
            Identifier(
                print_token.position,
                print_token.value
            ),
            [
                IntLiteral(
                    number.position,
                    number.value
                ),
            ]
        )]
    )
    output_stream_test(ast, str(number.value) + '\n')
