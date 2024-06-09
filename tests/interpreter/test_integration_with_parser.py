from unittest.mock import patch

from io import StringIO
from textwrap import dedent

from project.lexer.Lexer import Lexer

from project.parser.Parser import Parser

from project.code_source.CodeSource import CodeSource

from project.interpreter.Interpreter import Interpreter

from project.interpreter.ErrorHandler import ErrorHandler

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
    output_stream_test
)


def test_integration():
    code = dedent('''\
    a = 1;
    print(a);
    ''')

    fake_file_handle = StringIO(code)
    code_source = CodeSource(fake_file_handle)
    error_handler = ErrorHandler()
    parser = Parser(
        Lexer(code_source, error_handler),
        error_handler
    )
    ast = parser.parse_code()
    output_stream_test(ast, '1\n')
