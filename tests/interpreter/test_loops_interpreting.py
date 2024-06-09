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

from project.parser.ast_nodes.list.List import List as AstList

from project.interpreter.nodes.value.LValue import LValue
from project.interpreter.nodes.value.ValueType import ValueType
from project.interpreter.nodes.ValueContainerABC import ValueContainerABC

from project.interpreter.nodes.List import List as InterpreterList
from project.interpreter.nodes.Dict import Dict as InterpreterDict
from project.interpreter.nodes.Pair import Pair as InterpreterPair

from project.parser.ast_nodes.dict.Dict import Dict as AstDict
from project.parser.ast_nodes.dict.DictElement import DictElement
from project.parser.ast_nodes.dict.Pair import Pair as AstPair

from tests.interpreter.interpreter_test_utils import (
    variable_creation_test,
    output_stream_test
)

from project.parser.ast_nodes.incr_decr_statement.DecrementStatement import DecrementStatement


def test_for_loop():
    '''
    a = [1, 2, 3];
    for element in a {
        print(element);
    }
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    left_brackets = NoValToken(TokenType.BRACKETS_LEFT, PositionInCode(1, 5))

    one = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 6))
    two = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(1, 8))
    three = ValueToken(TokenType.INT_LITERAL, 3, PositionInCode(1, 10))

    for_token = NoValToken(TokenType.FOR, PositionInCode(2, 1))
    element = ValueToken(TokenType.IDENTIFIER, 'element', PositionInCode(2, 4))
    second_a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(2, 16))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(2, 18))
    fun = ValueToken(TokenType.IDENTIFIER, 'print', PositionInCode(2, 5))
    second_element = ValueToken(TokenType.IDENTIFIER, 'element', PositionInCode(2, 10))

    body = Block(
        left_braces.position,
        [
            FunctionCall(
                fun.position,
                Identifier(
                    fun.position,
                    fun.value
                ),
                [
                    Identifier(
                        second_element.position,
                        second_element.value
                    )
                ]
            )
        ]
    )

    ast = Code(
        [
            Assignment(
                a.position,
                Identifier(
                    a.position,
                    a.value
                ),
                AstList(
                    left_brackets.position,
                    [
                        IntLiteral(
                            one.position,
                            one.value
                        ),
                        IntLiteral(
                            two.position,
                            two.value
                        ),
                        IntLiteral(
                            three.position,
                            three.value
                        )
                    ]
                )
            ),
            ForLoop(
                for_token.position,
                Identifier(
                    element.position,
                    element.value
                ),
                Identifier(
                    second_a.position,
                    second_a.value
                ),
                body
            )
        ]
    )
    output_stream_test(ast, '1\n2\n3\n')


def test_while_loop():
    '''
    a = 5;
    while a > 0 {
        a--;
        print(a);
    }
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    five = ValueToken(TokenType.INT_LITERAL, 5, PositionInCode(1, 5))

    while_token = NoValToken(TokenType.WHILE, PositionInCode(2, 1))
    second_a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(2, 7))
    zero = ValueToken(TokenType.INT_LITERAL, 0, PositionInCode(2, 10))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(2, 12))
    third_a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(3, 5))
    fun = ValueToken(TokenType.IDENTIFIER, 'print', PositionInCode(4, 5))
    fourth_a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(4, 11))

    body = Block(
        left_braces.position,
        [
            DecrementStatement(
                third_a.position,
                Identifier(
                    third_a.position,
                    third_a.value
                )
            ),
            FunctionCall(
                fun.position,
                Identifier(
                    fun.position,
                    fun.value
                ),
                [
                    Identifier(
                        fourth_a.position,
                        fourth_a.value
                    )
                ]
            )
        ]
    )

    ast = Code(
        [
            Assignment(
                a.position,
                Identifier(
                    a.position,
                    a.value
                ),
                IntLiteral(
                    five.position,
                    five.value
                )
            ),
            WhileLoop(
                while_token.position,
                GreaterTerm(
                    second_a.position,
                    Identifier(
                        second_a.position,
                        second_a.value
                    ),
                    IntLiteral(
                        zero.position,
                        zero.value
                    )
                ),
                body
            )
        ]
    )
    output_stream_test(ast, '4\n3\n2\n1\n0\n')
