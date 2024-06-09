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

from tests.interpreter.interpreter_test_utils import variable_creation_test


def test_plus_operator():
    '''
    a = 1 + 2;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1,   PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 1,   PositionInCode(1, 9))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            AdditionTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.INT, first.value + second.value))


def test_minus_operator():
    '''
    a = 1 - 2;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1,   PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 2,   PositionInCode(1, 9))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            SubtractionTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.INT, first.value - second.value))


def test_multiplication_operator():
    '''
    a = 2 * 3;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 3, PositionInCode(1, 9))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            MultiplicationTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.INT, first.value * second.value))


def test_division_operator():
    '''
    a = 1 / 1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(1, 9))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            DivisionTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.FLOAT, first.value / second.value))


def test_not_operator():
    '''
    a = not True;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    not_token = NoValToken(TokenType.NOT, PositionInCode(1, 5))
    boolean = NoValToken(TokenType.TRUE, PositionInCode(1, 9))

    bool_val = boolean.type == TokenType.TRUE

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            NotTerm(
                not_token.position,
                BoolLiteral(
                    boolean.position,
                    bool_val
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, not bool_val))


def test_or_operator():
    '''
    a = True or False;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = NoValToken(TokenType.TRUE, PositionInCode(1, 9))
    second = NoValToken(TokenType.FALSE, PositionInCode(1, 13))

    first_value = first.type == TokenType.TRUE
    second_value = second.type == TokenType.TRUE

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            OrTerm(
                first.position,
                BoolLiteral(
                    first.position,
                    first_value
                ),
                BoolLiteral(
                    second.position,
                    second_value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first_value or second_value))


def test_and_operator():
    '''
    a = True and False;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = NoValToken(TokenType.TRUE, PositionInCode(1, 9))
    second = NoValToken(TokenType.FALSE, PositionInCode(1, 14))

    first_value = first.type == TokenType.TRUE
    second_value = second.type == TokenType.TRUE

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            AndTerm(
                first.position,
                BoolLiteral(
                    first.position,
                    first_value
                ),
                BoolLiteral(
                    second.position,
                    second_value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first_value and second_value))


def test_unary_minus():
    '''
    a = -1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    minus = NoValToken(TokenType.MINUS, PositionInCode(1, 5))
    number = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 6))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            UnaryMinusTerm(
                minus.position,
                IntLiteral(
                    number.position,
                    number.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.INT, -number.value))


def test_equals_equals_operator():
    '''
    a = 1 == 1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 10))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            EqualTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first.value == second.value))


def test_greater_operator():
    '''
    a = 1 > 1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 10))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            GreaterTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first.value > second.value))


def test_greater_equals_operator():
    '''
    a = 1 >= 1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 10))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            GreaterEqualTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first.value >= second.value))


def test_less_operator():
    '''
    a = 1 < 1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 10))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            LessTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first.value < second.value))


def test_less_equals_operator():
    '''
    a = 1 < 1;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    first = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 5))
    second = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 10))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            LessEqualTerm(
                first.position,
                IntLiteral(
                    first.position,
                    first.value
                ),
                IntLiteral(
                    second.position,
                    second.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.BOOL, first.value <= second.value))


def test_dot_operator():
    '''
    a = [1];
    b = a.at(0);
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    left_brackets = NoValToken(TokenType.BRACKETS_LEFT, PositionInCode(1, 5))
    element = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 6))
    b = ValueToken(TokenType.IDENTIFIER, 'b', PositionInCode(2, 1))
    second_a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(2, 5))
    at = ValueToken(TokenType.IDENTIFIER, 'at', PositionInCode(2, 7))
    index = ValueToken(TokenType.INT_LITERAL, 0, PositionInCode(2, 9))

    ast = Code(
        [
            Assignment(
                a.position,
                Identifier(
                    a.position,
                    a.value
                ),
                List(
                    left_brackets.position,
                    [
                        IntLiteral(
                            element.position,
                            element.value
                        )
                    ]
                )
            ),
            Assignment(
                b.position,
                Identifier(
                    b.position,
                    b.value
                ),
                DotTerm(
                    second_a.position,
                    [
                        Identifier(
                            second_a.position,
                            second_a.value
                        ),
                        FunctionCall(
                            at.position,
                            Identifier(
                                at.position,
                                at.value
                            ),
                            [
                                IntLiteral(
                                    index.position,
                                    index.value
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )

    variable_creation_test(ast, Variable(
        b.value, ValueType.INT, element.value))
