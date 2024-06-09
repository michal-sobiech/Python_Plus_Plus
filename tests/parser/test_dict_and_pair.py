from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.Token import Token
from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.SpecialToken import SpecialToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

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

from project.parser.ast_nodes.operator_terms.unary_minus_term.UnaryMinusTerm import UnaryMinusTerm

from project.parser.ast_nodes.operator_terms.and_term.AndTerm import AndTerm
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
from project.parser.ast_nodes.node.NodeABC import NodeABC
from project.parser.ast_nodes.StatementABC import StatementABC
from project.parser.ast_nodes.WhileLoop import WhileLoop

from project.parser.exceptions.SyntaxError import SyntaxError

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_many_elems_dict():
    '''
    {
        'a': 1,
        'b': 2
    };
    '''

    tokens = [
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 1)),

        ValueToken(TokenType.STRING_LITERAL, 'a',   PositionInCode(2, 5)),
        NoValToken(TokenType.COLON,                 PositionInCode(2, 8)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(2, 10)),
        NoValToken(TokenType.COMMA,                 PositionInCode(2, 11)),

        ValueToken(TokenType.STRING_LITERAL, 'b',   PositionInCode(3, 5)),
        NoValToken(TokenType.COLON,                 PositionInCode(3, 8)),
        ValueToken(TokenType.INT_LITERAL, 2,        PositionInCode(3, 10)),

        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(5, 1)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(5, 2))
    ]

    left_braces = tokens[0]

    first_element_key = tokens[1]
    first_element_value = tokens[3]

    second_element_key = tokens[5]
    second_element_value = tokens[7]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        dict_elements = [
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
            )
        ]

        dictionary = Dict(
            left_braces.position,
            dict_elements
        )

        expected_ast = Code(
            [dictionary]
        )

        assert expected_ast == actual_ast


def test_one_elem_dict():
    '''
    {
        'a': 1
    };
    '''

    tokens = [
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 1)),

        ValueToken(TokenType.STRING_LITERAL, 'a',   PositionInCode(2, 5)),
        NoValToken(TokenType.COLON,                 PositionInCode(2, 8)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(2, 10)),

        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(5, 1)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(5, 2))
    ]

    left_braces = tokens[0]

    first_element_key = tokens[1]
    first_element_value = tokens[3]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        dict_elements = [
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
            )
        ]

        dictionary = Dict(
            left_braces.position,
            dict_elements
        )

        expected_ast = Code(
            [dictionary]
        )

        assert expected_ast == actual_ast


def test_zero_elem_dict():
    '''
    {};
    '''

    tokens = [
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 1)),
        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(5, 1)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(5, 2))
    ]

    left_braces = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        dict_elements = []

        dictionary = Dict(
            left_braces.position,
            dict_elements
        )

        expected_ast = Code(
            [dictionary]
        )

        assert expected_ast == actual_ast


def test_pair_parsing():
    '''
    {1, 2};
    '''

    tokens = [
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 1)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(1, 2)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, 2,        PositionInCode(1, 5)),
        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(1, 6)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 7)),
    ]

    left_braces = tokens[0]
    first_element = tokens[1]
    second_element = tokens[3]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        key = IntLiteral(
            first_element.position,
            first_element.value
        )
        value = IntLiteral(
            second_element.position,
            second_element.value
        )

        pair = Pair(
            left_braces.position,
            key,
            value
        )

        expected_ast = Code(
            [pair]
        )

        assert expected_ast == actual_ast
