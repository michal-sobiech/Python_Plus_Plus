from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.function.call.FunctionCall import FunctionCall

from project.parser.ast_nodes.function.definition.FunctionDefinition import FunctionDefinition

from project.parser.ast_nodes.literal.IntLiteral import IntLiteral

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_fun_call_no_args():
    '''
    test();
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER,        'test', PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,          PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_RIGHT,         PositionInCode(1, 6)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(1, 7))
    ]

    function_name = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        function_call = FunctionCall(
            function_name.position,
            Identifier(function_name.position, function_name.value),
            []
        )

        expected_ast = Code(
            [function_call]
        )
        assert expected_ast == actual_ast


def test_fun_call_with_one_arg():
    '''
    test(1);
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER,        'test', PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,          PositionInCode(1, 5)),
        ValueToken(TokenType.INT_LITERAL,       1,      PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_RIGHT,         PositionInCode(1, 6)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(1, 7))
    ]

    function_name = tokens[0]
    arg_1 = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        function_call = FunctionCall(
            function_name.position,
            Identifier(function_name.position, function_name.value),
            [
                IntLiteral(
                    arg_1.position,
                    arg_1.value
                )
            ]
        )

        expected_ast = Code(
            [function_call]
        )
        assert expected_ast == actual_ast


def test_fun_call_with_many_args():
    '''
    test(1, 2, 3);
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER,        'test', PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,          PositionInCode(1, 5)),
        ValueToken(TokenType.INT_LITERAL,       1,      PositionInCode(1, 1)),
        NoValToken(TokenType.COMMA,                     PositionInCode(1, 6)),
        ValueToken(TokenType.INT_LITERAL,       2,      PositionInCode(1, 1)),
        NoValToken(TokenType.COMMA,                     PositionInCode(1, 6)),
        ValueToken(TokenType.INT_LITERAL,       3,      PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_RIGHT,         PositionInCode(1, 6)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(1, 7))
    ]

    function_name = tokens[0]
    arg_1 = tokens[2]
    arg_2 = tokens[4]
    arg_3 = tokens[6]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        function_call = FunctionCall(
            function_name.position,
            Identifier(function_name.position, function_name.value),
            [
                IntLiteral(
                    arg_1.position,
                    arg_1.value
                ),
                IntLiteral(
                    arg_2.position,
                    arg_2.value
                ),
                IntLiteral(
                    arg_3.position,
                    arg_3.value
                )
            ]
        )

        expected_ast = Code(
            [function_call]
        )
        assert expected_ast == actual_ast


def test_def_of_fun_with_no_params():
    '''
    def test() {}
    '''

    tokens = [
        NoValToken(TokenType.DEF,                     PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'test',      PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,        PositionInCode(1, 9)),
        NoValToken(TokenType.PARENTHESES_RIGHT,       PositionInCode(1, 10)),
        NoValToken(TokenType.BRACES_LEFT,             PositionInCode(1, 12)),
        NoValToken(TokenType.BRACES_RIGHT,            PositionInCode(3, 1))
    ]

    def_token = tokens[0]
    function_name = tokens[1]
    left_braces = tokens[4]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [FunctionDefinition(
                def_token.position,
                Identifier(
                    function_name.position,
                    function_name.value
                ),
                [],
                Block(
                    left_braces.position,
                    []
                )
            )],
        )

        assert expected_ast == actual_ast


def test_def_of_fun_with_one_param():
    '''
    def test(param_one) {}
    '''

    tokens = [
        NoValToken(TokenType.DEF,                     PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'test',      PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,        PositionInCode(1, 9)),
        ValueToken(TokenType.IDENTIFIER, 'param_one', PositionInCode(1, 10)),
        NoValToken(TokenType.PARENTHESES_RIGHT,       PositionInCode(1, 19)),
        NoValToken(TokenType.BRACES_LEFT,             PositionInCode(1, 21)),
        NoValToken(TokenType.BRACES_RIGHT,            PositionInCode(3, 1))
    ]

    def_token = tokens[0]
    function_name = tokens[1]
    param_1 = tokens[3]
    left_braces = tokens[5]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [FunctionDefinition(
                def_token.position,
                Identifier(
                    function_name.position,
                    function_name.value
                ),
                [
                    Identifier(
                        param_1.position,
                        param_1.value
                    )
                ],
                Block(
                    left_braces.position,
                    []
                )
            )],
        )

        assert expected_ast == actual_ast


def test_def_of_fun_with_multiple_params():
    '''
    def test(param_one, param_two) {}
    '''

    tokens = [
        NoValToken(TokenType.DEF,                     PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'test',      PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,        PositionInCode(1, 9)),
        ValueToken(TokenType.IDENTIFIER, 'param_one', PositionInCode(1, 10)),
        NoValToken(TokenType.COMMA,                   PositionInCode(1, 19)),
        ValueToken(TokenType.IDENTIFIER, 'param_two', PositionInCode(1, 21)),
        NoValToken(TokenType.PARENTHESES_RIGHT,       PositionInCode(1, 30)),
        NoValToken(TokenType.BRACES_LEFT,             PositionInCode(1, 32)),
        NoValToken(TokenType.BRACES_RIGHT,            PositionInCode(3, 1))
    ]

    def_token = tokens[0]
    function_name = tokens[1]
    param_1 = tokens[3]
    param_2 = tokens[5]
    left_braces = tokens[7]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [FunctionDefinition(
                def_token.position,
                Identifier(
                    function_name.position,
                    function_name.value
                ),
                [
                    Identifier(
                        param_1.position,
                        param_1.value
                    ),
                    Identifier(
                        param_2.position,
                        param_2.value
                    )
                ],
                Block(
                    left_braces.position,
                    []
                )
            )],
        )

        assert expected_ast == actual_ast