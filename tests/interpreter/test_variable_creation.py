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

from project.parser.ast_nodes.dict.Dict import Dict as AstDict
from project.parser.ast_nodes.dict.DictElement import DictElement
from project.parser.ast_nodes.dict.Pair import Pair as AstPair

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

from tests.interpreter.interpreter_test_utils import variable_creation_test

from project.interpreter.nodes.List import List as InterpreterList

from project.interpreter.nodes.Dict import Dict as InterpreterDict
from project.interpreter.nodes.List import List as InterpreterList
from project.interpreter.nodes.Pair import Pair as InterpreterPair


def test_function_call():
    '''
    a = 123;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    number = ValueToken(TokenType.INT_LITERAL, 123,   PositionInCode(1, 5))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            IntLiteral(
                number.position,
                number.value
            )
        )]
    )

    variable_creation_test(ast, Variable(a.value, ValueType.INT, number.value))


def test_float_variable_creation():
    '''
    a = 0.123;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    number = ValueToken(TokenType.FLOAT_LITERAL, 0.123, PositionInCode(1, 5))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            FloatLiteral(
                number.position,
                number.value
            )
        )]
    )

    variable_creation_test(ast, Variable(a.value, ValueType.FLOAT, number.value))


def test_bool_variable_creation():
    '''
    a = True;
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    boolean = NoValToken(TokenType.TRUE, PositionInCode(1, 5))

    bool_val = boolean.type == TokenType.TRUE

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            BoolLiteral(
                boolean.position,
                bool_val
            )
        )]
    )

    variable_creation_test(ast, Variable(a.value, ValueType.BOOL, bool_val))


def test_string_variable_creation():
    '''
    a = 'test';
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    string = ValueToken(TokenType.STRING_LITERAL, 'test', PositionInCode(1, 5))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            StringLiteral(
                string.position,
                string.value
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value, ValueType.STRING, string.value))


def test_list_variable_creations():
    '''
    a = [1, 2, 3];
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 5))
    one = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 6))
    two = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(1, 8))
    three = ValueToken(TokenType.INT_LITERAL, 3, PositionInCode(1, 10))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            AstList(
                left_braces.position,
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
        )]
    )

    variable_creation_test(ast, Variable(
        a.value,
        ValueType.LIST,
        InterpreterList([
            LValue(
                ValueType.INT,
                one.value
            ),
            LValue(
                ValueType.INT,
                two.value
            ),
            LValue(
                ValueType.INT,
                three.value
            )
        ])
    ))


def test_dict_variable_creation():
    '''
    a = {
        'b': 1,
        'c': 2
    };
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 5))
    b = ValueToken(TokenType.STRING_LITERAL, 'b', PositionInCode(1, 6))
    c = ValueToken(TokenType.STRING_LITERAL, 'c', PositionInCode(1, 10))
    one = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 8))
    two = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(1, 12))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            AstDict(
                left_braces.position,
                [
                    DictElement(
                        b.position,
                        StringLiteral(
                            b.position,
                            b.value
                        ),
                        IntLiteral(
                            one.position,
                            one.value
                        )
                    ),
                    DictElement(
                        c.position,
                        StringLiteral(
                            c.position,
                            c.value
                        ),
                        IntLiteral(
                            two.position,
                            two.value
                        )
                    )
                ]
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value,
        ValueType.DICT,
        InterpreterDict(
            [
                (
                    LValue(
                        ValueType.STRING,
                        b.value
                    ),
                    LValue(
                        ValueType.INT,
                        one.value
                    )
                ),
                (
                    LValue(
                        ValueType.STRING,
                        c.value
                    ),
                    LValue(
                        ValueType.INT,
                        two.value
                    )
                )
            ]
        )
    ))


def test_pair_variable_creation():
    '''
    a = {'b', 1};
    '''

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 5))
    b = ValueToken(TokenType.STRING_LITERAL, 'b', PositionInCode(1, 6))
    one = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(1, 8))

    ast = Code(
        [Assignment(
            a.position,
            Identifier(
                a.position,
                a.value
            ),
            AstPair(
                left_braces.position,
                StringLiteral(
                    b.position,
                    b.value
                ),
                IntLiteral(
                    one.position,
                    one.value
                )
            )
        )]
    )

    variable_creation_test(ast, Variable(
        a.value,
        ValueType.PAIR,
        InterpreterPair(
            LValue(ValueType.STRING, b.value),
            LValue(ValueType.INT, one.value)
        )
    ))
