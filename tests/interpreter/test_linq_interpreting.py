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

from project.parser.ast_nodes.list.List import List

from project.interpreter.nodes.value.LValue import LValue
from project.interpreter.nodes.value.ValueType import ValueType
from project.interpreter.nodes.ValueContainerABC import ValueContainerABC

from project.interpreter.nodes.List import List as InterpreterList
from project.interpreter.nodes.Dict import Dict as InterpreterDict
from project.interpreter.nodes.Pair import Pair as InterpreterPair

from project.parser.ast_nodes.dict.Dict import Dict as AstDict
from project.parser.ast_nodes.dict.DictElement import DictElement
from project.parser.ast_nodes.dict.Pair import Pair as AstPair

from tests.interpreter.interpreter_test_utils import variable_creation_test


def test_linq():
    '''
    def compare(first, second) {
        return first.value() < second.value();
    }
    a = {'a': 1, 'b': 3, 'c': 2};
    b = from tuple in a where True orderby compare select tuple.key();
    '''

    def_token = NoValToken(TokenType.DEF, PositionInCode(1, 1))
    fun_def_name = ValueToken(TokenType.IDENTIFIER, 'compare', PositionInCode(1, 5))
    first_first = ValueToken(TokenType.IDENTIFIER, 'first', PositionInCode(1, 1))
    first_second = ValueToken(TokenType.IDENTIFIER, 'second', PositionInCode(1, 1))
    left_braces = NoValToken(TokenType.BRACES_LEFT, PositionInCode(1, 9))
    return_token = NoValToken(TokenType.RETURN, PositionInCode(2, 4))

    second_first = ValueToken(TokenType.IDENTIFIER, 'first', PositionInCode(1, 1))
    first_value_call = ValueToken(TokenType.IDENTIFIER, 'value', PositionInCode(1, 1))

    second_second = ValueToken(TokenType.IDENTIFIER, 'second', PositionInCode(1, 1))
    second_value_call = ValueToken(TokenType.IDENTIFIER, 'value', PositionInCode(1, 1))

    a = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1))
    left_braces = NoValToken(TokenType.BRACKETS_LEFT, PositionInCode(1, 5))

    first_element_key = ValueToken(TokenType.STRING_LITERAL, 'a', PositionInCode(3, 6))
    first_element_value = ValueToken(TokenType.INT_LITERAL, 1, PositionInCode(3, 6))

    second_element_key = ValueToken(TokenType.STRING_LITERAL, 'b', PositionInCode(3, 8))
    second_element_value = ValueToken(TokenType.INT_LITERAL, 3, PositionInCode(3, 10))

    third_element_key = ValueToken(TokenType.STRING_LITERAL, 'c', PositionInCode(3, 13))
    third_element_value = ValueToken(TokenType.INT_LITERAL, 2, PositionInCode(3, 16))

    b = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(4, 1))
    from_token = NoValToken(TokenType.FROM, PositionInCode(4, 1))
    tuple = ValueToken(TokenType.IDENTIFIER, 'tuple', PositionInCode(4, 6))
    src = ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(4, 15))
    true = NoValToken(TokenType.TRUE, PositionInCode(4, 26))
    second_fun = ValueToken(TokenType.IDENTIFIER, 'compare', PositionInCode(4, 36))
    second_tuple = ValueToken(TokenType.IDENTIFIER, 'tuple', PositionInCode(4, 48))
    key_call = ValueToken(TokenType.IDENTIFIER, 'key', PositionInCode(4, 48))

    body = Block(
        left_braces.position,
        [
            ReturnWithValue(
                return_token.position,
                LessTerm(
                    second_first.position,
                    DotTerm(
                        second_first.position,
                        [
                            Identifier(
                                second_first.position,
                                second_first.value
                            ),
                            FunctionCall(
                                first_value_call.position,
                                Identifier(
                                    first_value_call.position,
                                    first_value_call.value,
                                ),
                                []
                            )
                        ]
                    ),
                    DotTerm(
                        second_second.position,
                        [
                            Identifier(
                                second_second.position,
                                second_second.value
                            ),
                            FunctionCall(
                                second_value_call.position,
                                Identifier(
                                    second_value_call.position,
                                    second_value_call.value
                                ),
                                []
                            )
                        ]
                    )
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
                [
                    Identifier(
                        first_first.position,
                        first_first.value
                    ),
                    Identifier(
                        first_second.position,
                        first_second.value
                    )
                ],
                body
            ),
            Assignment(
                a.position,
                Identifier(
                    a.position,
                    a.value
                ),
                AstDict(
                    left_braces.position,
                    [
                        DictElement(
                            first_element_key.position,
                            StringLiteral(
                                first_element_key.position,
                                first_element_key.value
                            ),
                            IntLiteral(
                                first_element_value.position,
                                first_element_value.value
                            )
                        ),
                        DictElement(
                            second_element_key.position,
                            StringLiteral(
                                second_element_key.position,
                                second_element_key.value
                            ),
                            IntLiteral(
                                second_element_value.position,
                                second_element_value.value
                            )
                        ),
                        DictElement(
                            third_element_key.position,
                            StringLiteral(
                                third_element_key.position,
                                third_element_key.value
                            ),
                            IntLiteral(
                                third_element_value.position,
                                third_element_value.value
                            )
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
                LinqQuery(
                    from_token.position,
                    Identifier(
                        tuple.position,
                        tuple.value
                    ),
                    Identifier(
                        src.position,
                        src.value
                    ),
                    BoolLiteral(
                        true.position,
                        true.type == TokenType.TRUE
                    ),
                    Identifier(
                        second_fun.position,
                        second_fun.value
                    ),
                    [
                        DotTerm(
                            second_tuple.position,
                            [
                                Identifier(
                                    second_tuple.position,
                                    second_tuple.value
                                ),
                                FunctionCall(
                                    key_call.position,
                                    Identifier(
                                        key_call.position,
                                        key_call.value
                                    ),
                                    []
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )

    variable_creation_test(ast, Variable(
        b.value,
        ValueType.LIST,
        InterpreterList(
            [
                LValue(
                    ValueType.LIST,
                    InterpreterList(
                        [
                            LValue(
                                ValueType.STRING,
                                first_element_key.value
                            )
                        ]
                    )
                ),
                LValue(
                    ValueType.LIST,
                    InterpreterList(
                        [
                            LValue(
                                ValueType.STRING,
                                third_element_key.value
                            )
                        ]
                    )
                ),
                LValue(
                    ValueType.LIST,
                    InterpreterList(
                        [
                            LValue(
                                ValueType.STRING,
                                second_element_key.value
                            )
                        ]
                    )
                )
            ]
        )
    ))
