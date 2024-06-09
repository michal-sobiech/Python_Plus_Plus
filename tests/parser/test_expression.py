from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.operator_terms.add_or_sub_term.AdditionTerm import AdditionTerm
from project.parser.ast_nodes.operator_terms.add_or_sub_term.SubtractionTerm import SubtractionTerm

from project.parser.ast_nodes.operator_terms.and_term.AndTerm import AndTerm

from project.parser.ast_nodes.operator_terms.comparison_term.GreaterTerm import GreaterTerm

from project.parser.ast_nodes.operator_terms.mul_or_div_term.MultiplicationTerm import MultiplicationTerm
from project.parser.ast_nodes.operator_terms.mul_or_div_term.DivisionTerm import DivisionTerm

from project.parser.ast_nodes.operator_terms.not_term.NotTerm import NotTerm

from project.parser.ast_nodes.operator_terms.or_term.OrTerm import OrTerm

from project.parser.ast_nodes.operator_terms.unary_minus_term.UnaryMinusTerm import UnaryMinusTerm

from project.parser.ast_nodes.operator_terms.and_term.AndTerm import AndTerm
from project.parser.ast_nodes.operator_terms.DotTerm import DotTerm

from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_no_operators_term():
    '''
    a;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 2)),
    ]

    a_token = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [Identifier(
               a_token.position,
               a_token.value
            )]
        )
        assert expected_ast == actual_ast


def test_or_operator():
    '''
    a or b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.OR,                PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 6)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 7)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [OrTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_and_operator():
    '''
    a and b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.AND,               PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 7)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 8)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [AndTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_not_operator():
    '''
    not a;
    '''

    tokens = [
        NoValToken(TokenType.NOT,               PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 3)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 4)),
    ]

    not_token = tokens[0]
    a_token = tokens[1]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [NotTerm(
                not_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_comp_operator():
    '''
    a > b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.GREATER,           PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 6)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [GreaterTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_addition():
    '''
    a + b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.PLUS,              PositionInCode(1, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 10)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [AdditionTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_subtraction():
    '''
    a - b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.MINUS,             PositionInCode(1, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 10)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [SubtractionTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_multiplication_operator():
    '''
    a * b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.MULTIPLY,          PositionInCode(1, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 10)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [MultiplicationTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_division_operator():
    '''
    a / b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.DIVIDE,            PositionInCode(1, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 10)),
    ]

    a_token = tokens[0]
    b_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [DivisionTerm(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                ),
                Identifier(
                    b_token.position,
                    b_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_unary_minus_operator():
    '''
    -a;
    '''

    tokens = [
        NoValToken(TokenType.MINUS,             PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 2)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 3)),
    ]

    minus_token = tokens[0]
    a_token = tokens[1]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [UnaryMinusTerm(
                minus_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_dot_term():
    '''
    a.a;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.DOT,               PositionInCode(1, 2)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 3)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 4)),
    ]

    first_var = tokens[0]
    second_var = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [DotTerm(
                first_var.position,
                [
                    Identifier(
                        first_var.position,
                        first_var.value
                    ),
                    Identifier(
                        second_var.position,
                        second_var.value
                    )
                ]
            )]
        )
        assert expected_ast == actual_ast
