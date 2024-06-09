from typing import Type, Optional

from enum import Enum, auto

import copy

import sys

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
from project.interpreter.nodes.Result import Result, ResultType

from project.interpreter.nodes.List import List as InterpreterList
from project.interpreter.nodes.Dict import Dict as InterpreterDict
from project.interpreter.nodes.Pair import Pair as InterpreterPair

from project.interpreter.ErrorHandler import ErrorHandler
from project.interpreter.InterpreterError import InterpreterError
from project.interpreter.InterpreterErrorMsg import InterpreterErrorMsg
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.literal.NoneLiteral import NoneLiteral

from project.parser.ast_nodes.node.PositionNodeABC import PositionNodeABC


class TwoExprMathOperator(Enum):
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()


class TwoExprLogicOperator(Enum):
    EQUALS_EQUALS = auto()
    AND = auto()
    OR = auto()


class TwoExprCompOperator(Enum):
    EQUALS_EQUALS = auto()
    GREATER = auto()
    GREATER_EQUALS = auto()
    LESS = auto()
    LESS_EQUALS = auto()


class Interpreter:
    def __init__(
        self,
        code: Code,
        output_stream,
        error_handler: ErrorHandler
    ) -> None:
        self.code = code
        self._output_stream = output_stream
        self._error_handler = error_handler

        self._current_position = PositionInCode(1, 1)
        self._context_stack: list[Context] = [
            Context(None, self._current_position)
        ]
        self._result: Result = None
        self._current_struct: Optional[LValue] = None

        self._max_context_stack_length = 100

        self._functions = {
            'print': EmbeddedFunction('print', ['object'], self.global_print),
            'bool': EmbeddedFunction('bool', ['object'], self.global_bool),
            'int': EmbeddedFunction('int', ['object'], self.global_int),
            'float': EmbeddedFunction('float', ['object'], self.global_float),
            'string': EmbeddedFunction('string', ['object'], self.global_string),
        }

        self._struct_methods = {
            ValueType.LIST: {
                'at': EmbeddedFunction('at', ['index'], self.list_at),
                'length': EmbeddedFunction('length', [], self.list_length),
                'append': EmbeddedFunction('append', ['value'], self.list_append),
                'pop': EmbeddedFunction('pop', [], self.list_pop)
            },
            ValueType.DICT: {
                'has_key': EmbeddedFunction('has_key', ['key'], self.dict_has_key),
                'sort': EmbeddedFunction('sort', ['function'], self.dict_sort),
                'by_index': EmbeddedFunction('by_index', ['index'], self.dict_by_index),
                'by_key': EmbeddedFunction('by_key', ['key'], self.dict_by_key),
                'length': EmbeddedFunction('length', [], self.dict_length),
                'append': EmbeddedFunction('append', ['value'], self.dict_append),
                'pop': EmbeddedFunction('pop', [], self.dict_pop)
            },
            ValueType.PAIR: {
                'key': EmbeddedFunction('key', [], self.pair_key),
                'value': EmbeddedFunction('value', [], self.pair_value)
            }
        }

    def raise_error(self, error_description: InterpreterErrorMsg) -> None:
        raise InterpreterError(
            self._current_position,
            error_description,
            self._context_stack[1:]
        )

    def _add_scope(self) -> None:
        self._context_stack[-1].add_scope()

    def _pop_scope(self) -> None:
        self._context_stack[-1].pop_scope()

    def _add_context(self, function_name: str) -> None:
        if len(self._context_stack) < self._max_context_stack_length:
            self._context_stack.append(Context(
                function_name, self._current_position
            ))
        else:
            self.raise_error(InterpreterErrorMsg.STACK_OVERFLOW)

    def _pop_context(self) -> None:
        self._context_stack.pop()

    def get_lvalue_from_result(self) -> LValue:
        if self._result.type == ResultType.LVALUE:
            return self._result.value
        elif self._result.type == ResultType.OBJECT_NAME:
            if (var := self.get_variable(self._result.value)) is not None:
                return LValue(var.type, var.value)
            elif (self._result.value in self._functions.keys()):
                return LValue(ValueType.FUNCTION_NAME, self._result.value)
            else:
                self.raise_error(InterpreterErrorMsg.NO_SUCH_OBJECT)
        else:
            # TODO error msg
            self.raise_error(InterpreterErrorMsg.INVALID_VALUE)

    def get_object_name_from_result(self) -> str:
        if self._result.type == ResultType.OBJECT_NAME:
            return self._result.value
        else:
            self.raise_error(InterpreterErrorMsg.NO_SUCH_RVALUE)

    def get_variable(self, name: str) -> Variable:
        for call_frame in reversed(self._context_stack):
            if (var := call_frame.get_variable(name)) is not None:
                return var
        return None

    def has_variable(self, name: str) -> bool:
        return self.get_variable(name) is not None

    def _create_variable_in_last_scope(
        self,
        name: str,
        type: ValueType,
        value
    ) -> None:
        '''
        Creates a variable in the last scope of the last context
        '''
        new_var = copy.deepcopy(Variable(name, type, value))
        self._context_stack[-1].scope_stack[-1].variables.append(new_var)

    def _assign_variable(
        self,
        name: str,
        type: ValueType,
        value
    ) -> None:
        if (var := self.get_variable(name)) is not None:
            var.type = copy.deepcopy(type)
            var.value = copy.deepcopy(value)
        else:
            if name in self._functions.keys():
                self.raise_error(InterpreterErrorMsg.NAME_TAKEN_BY_FUNCTION)
            self._create_variable_in_last_scope(name, type, value)

    def interpret(self) -> None:
        try:
            self.code.accept(self)
        except InterpreterError as error:
            self._error_handler.handle_interpreter_error(error)

    def visit_code(self, node: Code) -> None:
        for fundef_or_stmt in node.fun_defs_and_statements:
            self.accept_node_and_set_pos(fundef_or_stmt)

            if self._result.type == ResultType.RETURN:
                return

    def visit_function_definition(self, node: FunctionDefinition) -> None:
        self.accept_node_and_set_pos(node.name)
        function_name = self.get_object_name_from_result()
        if function_name in self._functions.keys():
            self.raise_error(InterpreterErrorMsg.FUNCTION_ALREADY_EXISTS)
        elif self.has_variable(function_name):
            self.raise_error(InterpreterErrorMsg.NAME_TAKEN_BY_VAR)

        parameters = [id.value for id in node.parameters]

        body = node.body

        self._functions[function_name] = InterpretedFunction(
            function_name, parameters, body)

    def visit_assignment(self, node: Assignment) -> None:
        self.accept_node_and_set_pos(node.left_expression)
        left_var_name = self.get_object_name_from_result()

        self.accept_node_and_set_pos(node.right_expression)
        right = self.get_lvalue_from_result()
        self._assign_variable(left_var_name, right.type, right.value)

    def visit_identifier(self, node: Identifier) -> None:
        self._result = Result(ResultType.OBJECT_NAME, node.value)

    def visit_dict(self, node: AstDict) -> None:
        dict_elems: list[tuple] = []
        for ast_dict_element in node.elements:

            self.accept_node_and_set_pos(ast_dict_element.key)
            key = self.get_lvalue_from_result()

            self.accept_node_and_set_pos(ast_dict_element.value)
            value = self.get_lvalue_from_result()

            dict_elems.append((key, value))

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.DICT, InterpreterDict(dict_elems))
        )

    def visit_pair(self, node: AstPair) -> None:
        self.accept_node_and_set_pos(node.key)
        key = self.get_lvalue_from_result()

        self.accept_node_and_set_pos(node.value)
        value = self.get_lvalue_from_result()

        self._result = Result(
            ResultType.LVALUE,
            LValue(
                ValueType.PAIR,
                InterpreterPair(key, value)
            )
        )

    def visit_function_call(self, node: FunctionCall) -> None:
        self.accept_node_and_set_pos(node.function_name)
        function_name = self.get_object_name_from_result()

        if self._current_struct is not None:
            struct_type = self._current_struct.type

            struct_methods = self._struct_methods.get(struct_type)
            if struct_methods is None:
                self.raise_error(InterpreterErrorMsg.NO_SUCH_FUNCTION)

            if (fun := struct_methods.get(function_name)) is None:
                self.raise_error(InterpreterErrorMsg.NO_SUCH_FUNCTION)
        else:
            if (fun := self._functions.get(function_name)) is None:
                self.raise_error(InterpreterErrorMsg.NO_SUCH_FUNCTION)

        if len(node.args) != fun.get_parameter_count():
            self.raise_error(InterpreterErrorMsg.INVALID_ARG_COUNT)

        self._add_context(fun.name)

        for param_name, ast_arg in zip(fun.parameters, node.args):
            self.accept_node_and_set_pos(ast_arg)
            arg = self.get_lvalue_from_result()
            self._create_variable_in_last_scope(
                param_name, arg.type, arg.value
            )

        fun.accept(self)
        self._pop_context()

    def visit_embedded_function(self, fun: EmbeddedFunction) -> None:
        args = self._context_stack[-1].get_variables()

        if (obj := self._current_struct) is not None:
            ret = fun.function(obj, *args)
        else:
            ret = fun.function(*args)

        self._result = Result(ResultType.LVALUE, ret)

    def visit_interpreted_function(self, fun: InterpretedFunction) -> None:
        fun.body.accept(self)

        if self._result.type == ResultType.RETURN:
            self._result = Result(
                ResultType.LVALUE,
                self._result.value
            )
        else:
            lvalue = LValue(ValueType.NONE, None)
            self._result = Result(ResultType.LVALUE, lvalue)

    def visit_block(self, node: Block) -> None:
        for statement in node.statements:
            self.accept_node_and_set_pos(statement)

            if self._result.type == ResultType.RETURN:
                return

        self._result = Result(ResultType.BLOCK_EXITED, None)

    def visit_linq_query(self, node: LinqQuery) -> None:
        self.accept_node_and_set_pos(node.iterator_var)
        iterator_var_name = self.get_object_name_from_result()

        self.accept_node_and_set_pos(node.source)
        src_deep_copy = copy.deepcopy(self.get_lvalue_from_result())
        if src_deep_copy.type != ValueType.DICT:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        if node.sorting_function is not None:
            self.accept_node_and_set_pos(node.sorting_function)
            sorting_function_name = self.get_object_name_from_result()

            self._current_struct = src_deep_copy

            self._add_context(sorting_function_name)
            self._create_variable_in_last_scope(
                'function',
                ValueType.FUNCTION_NAME,
                sorting_function_name
            )
            fun = self._struct_methods[ValueType.DICT]['sort']
            fun.accept(self)

            self._pop_context()

            self._current_struct = None

        self._add_scope()

        all_selected_values = []
        for i, tuple in enumerate(src_deep_copy.value.elements):
            if i == 0:
                self._create_variable_in_last_scope(
                    iterator_var_name,
                    ValueType.PAIR,
                    InterpreterPair(*tuple)
                )
            else:
                self._assign_variable(
                    iterator_var_name,
                    ValueType.PAIR,
                    InterpreterPair(*tuple)
                )

            self.accept_node_and_set_pos(node.condition)
            is_condition_met = self.get_lvalue_from_result()
            if is_condition_met.type != ValueType.BOOL:
                self.raise_error(InterpreterErrorMsg.INVALID_TYPE)
            if is_condition_met.value is False:
                continue

            row_elements = []
            for ast_selected_value in node.selected_values:
                self.accept_node_and_set_pos(ast_selected_value)
                row_elem = self.get_lvalue_from_result()
                row_elements.append(row_elem)

            all_selected_values.append(LValue(
                ValueType.LIST,
                InterpreterList(row_elements)
            ))

        self._result = Result(
            ResultType.LVALUE,
            LValue(
                ValueType.LIST,
                InterpreterList(all_selected_values)
            )
        )

        self._pop_scope()

    def visit_list(self, node: AstList) -> None:
        elements: list[LValue] = []
        for ast_elem in node.elements:
            self.accept_node_and_set_pos(ast_elem)
            elements.append(self.get_lvalue_from_result())

        self._result = Result(
            ResultType.LVALUE,
            LValue(
                ValueType.LIST,
                InterpreterList(elements)
            )
        )

    def visit_dot_term(self, node: DotTerm) -> None:
        prev_struct = self._current_struct
        for i, ast_term in enumerate(node.terms):
            self.accept_node_and_set_pos(ast_term)
            if i != len(node.terms) - 1:
                struct = self.get_lvalue_from_result()
                self._current_struct = struct
                if struct.type not in [
                    ValueType.LIST,
                    ValueType.DICT,
                    ValueType.PAIR
                ]:
                    self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        self._current_struct = prev_struct

    def two_operand_operation_type_check(
        self,
        node,
        allowed_types: list[ValueType]
    ) -> tuple[LValue, LValue]:
        self.accept_node_and_set_pos(node.left_term)
        left = self.get_lvalue_from_result()
        if left.type not in allowed_types:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        self.accept_node_and_set_pos(node.right_term)
        right = self.get_lvalue_from_result()
        if right.type not in allowed_types:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        if not left.type == right.type:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        return left, right

    def visit_addition_term(self, node: AdditionTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT, ValueType.STRING]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(left.type, left.value + right.value)
        )

    def visit_subtraction_term(self, node: SubtractionTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(left.type, left.value - right.value)
        )

    def visit_multiplication_term(self, node: MultiplicationTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(left.type, left.value * right.value)
        )

    def visit_division_term(self, node: DivisionTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        if right.value == 0:
            self.raise_error(InterpreterErrorMsg.DIVISION_BY_ZERO)

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.FLOAT, float(left.value) / float(right.value))
        )

    def visit_and_term(self, node: AndTerm) -> None:
        self.accept_node_and_set_pos(node.left_term)
        left = self.get_lvalue_from_result()
        if left.type != ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        if left.value is False:
            self._result = Result(
                ResultType.LVALUE,
                LValue(ValueType.BOOL, False)
            )
            return

        self.accept_node_and_set_pos(node.right_term)
        right = self.get_lvalue_from_result()
        if right.type != ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value and right.value)
        )

    def visit_or_term(self, node: OrTerm) -> None:
        self.accept_node_and_set_pos(node.left_term)
        left = self.get_lvalue_from_result()
        if left.type != ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        if left.value is True:
            self._result = Result(
                ResultType.LVALUE,
                LValue(ValueType.BOOL, True)
            )
            return

        self.accept_node_and_set_pos(node.right_term)
        right = self.get_lvalue_from_result()
        if right.type != ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value or right.value)
        )

    def visit_greater_term(self, node: GreaterTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value > right.value)
        )

    def visit_greater_equal_terms(self, node: GreaterEqualTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value >= right.value)
        )

    def visit_less_term(self, node: LessTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value < right.value)
        )

    def visit_less_equal_terms(self, node: LessEqualTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value <= right.value)
        )

    def visit_equal_term(self, node: EqualTerm) -> None:
        left, right = self.two_operand_operation_type_check(
            node, [ValueType.INT, ValueType.FLOAT, ValueType.BOOL]
        )

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, left.value == right.value)
        )

    def visit_not_term(self, node: NotTerm) -> None:
        self.accept_node_and_set_pos(node.term)
        result_lvalue = self.get_lvalue_from_result()
        if result_lvalue.type is not ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, not result_lvalue.value)
        )

    def visit_unary_minus_term(self, node: UnaryMinusTerm) -> None:
        self.accept_node_and_set_pos(node.term)
        result_lvalue = self.get_lvalue_from_result()
        if result_lvalue.type not in [ValueType.INT, ValueType.FLOAT]:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        self._result = Result(
            ResultType.LVALUE,
            LValue(result_lvalue.type, -result_lvalue.value)
        )

    def visit_bool_literal(self, node: BoolLiteral) -> None:
        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.BOOL, node.value)
        )

    def visit_float_literal(self, node: FloatLiteral) -> None:
        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.FLOAT, node.value)
        )

    def visit_int_literal(self, node: IntLiteral) -> None:
        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.INT, node.value)
        )

    def visit_string_literal(self, node: StringLiteral) -> None:
        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.STRING, node.value)
        )

    def visit_none_literal(self, node: NoneLiteral) -> None:
        self._result = Result(
            ResultType.LVALUE,
            LValue(ValueType.NONE, None)
        )

    def visit_return_no_value(self, node: ReturnNoValue) -> None:
        self._result = Result(
            ResultType.RETURN,
            LValue(ValueType.NONE, None)
        )

    def visit_return_with_value(self, node: ReturnWithValue) -> None:
        self.accept_node_and_set_pos(node.value)
        self._result = Result(
            ResultType.RETURN,
            self.get_lvalue_from_result()
        )

    def visit_conditional_statement(self, node: ConditionalStatement) -> None:
        self.accept_node_and_set_pos(node.if_statement)

        if (
            self._result.type == ResultType.RETURN
            or (
                self._result.type == ResultType.COND_STMT_ENTERED
                and self._result.value is True
            )
        ):
            return

        for ast_elif_stmt in node.elif_statements:
            self.accept_node_and_set_pos(ast_elif_stmt)

            if (
                self._result.type == ResultType.RETURN
                or (
                    self._result.type == ResultType.COND_STMT_ENTERED
                    and self._result.value is True
                )
            ):
                return

        if (ast_else_stmt := node.else_statement) is not None:
            self.accept_node_and_set_pos(ast_else_stmt)

    def visit_for_loop(self, node: ForLoop) -> None:
        self.accept_node_and_set_pos(node.iterator_var)
        iterator_var_name = self.get_object_name_from_result()

        self.accept_node_and_set_pos(node.sequence)
        sequence = self.get_lvalue_from_result()
        if sequence.type not in [ValueType.LIST, ValueType.DICT]:
            self.raise_error(InterpreterErrorMsg.UNITERABLE_OBJECT)

        for element in sequence.value.elements:
            self._add_scope()

            if sequence.type == ValueType.LIST:
                self._create_variable_in_last_scope(
                    iterator_var_name,
                    element.type,
                    element.value
                )
            elif sequence.type == ValueType.DICT:
                self._create_variable_in_last_scope(
                    iterator_var_name,
                    ValueType.PAIR,
                    InterpreterPair(element[0], element[1])
                )

            self.accept_node_and_set_pos(node.body)
            if self._result.type == ResultType.RETURN:
                return
            else:
                self._pop_scope()

    def visit_while_loop(self, node: WhileLoop) -> None:
        self.accept_node_and_set_pos(node.condition)
        is_condition_met = self.get_lvalue_from_result()
        if is_condition_met.type != ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

        while is_condition_met.value is True:
            self._add_scope()
            self.accept_node_and_set_pos(node.body)
            if self._result.type == ResultType.RETURN:
                return
            else:
                self._pop_scope()

            self.accept_node_and_set_pos(node.condition)
            is_condition_met = self.get_lvalue_from_result()
            if is_condition_met.type != ValueType.BOOL:
                self.raise_error(InterpreterErrorMsg.INVALID_TYPE)

    def _handle_if_or_elif_statement(self, node) -> None:
        self.accept_node_and_set_pos(node.condition)
        condition_is_met = self.get_lvalue_from_result()
        if condition_is_met.type != ValueType.BOOL:
            self.raise_error(InterpreterErrorMsg.INVALID_TYPE)
        if condition_is_met.value is False:
            self._result = Result(
                ResultType.COND_STMT_ENTERED,
                False
            )
            return

        self._add_scope()
        self.accept_node_and_set_pos(node.body)
        self._pop_scope()

        if self._result.type == ResultType.RETURN:
            return
        else:
            self._result = Result(
                ResultType.COND_STMT_ENTERED,
                True
            )

    def visit_if_statement(self, node: IfStatement) -> None:
        self._handle_if_or_elif_statement(node)

    def visit_elif_statement(self, node: ElifStatement) -> None:
        self._handle_if_or_elif_statement(node)

    def visit_else_statement(self, node: ElseStatement) -> None:
        self.accept_node_and_set_pos(node.body)

    def visit_increment_statement(self, node: IncrementStatement) -> None:
        self.accept_node_and_set_pos(node.expression)

        var_name = self.get_object_name_from_result()

        if (var := self.get_variable(var_name)) is None:
            raise Exception

        var.value += 1

    def visit_decrement_statement(self, node: IncrementStatement) -> None:
        self._current_position = node.position
        self.accept_node_and_set_pos(node.expression)

        var_name = self.get_object_name_from_result()

        if (var := self.get_variable(var_name)) is None:
            raise Exception

        var.value -= 1

    def accept_node_and_set_pos(self, node: PositionNodeABC) -> None:
        self._current_position = node.position
        node.accept(self)

    def list_at(self, obj: LValue, index: Variable) -> LValue:
        if index.type != ValueType.INT:
            self.raise_error(InterpreterErrorMsg.ARG_INVALID_TYPE)

        if index.value in range(0, len(obj.value.elements)):
            return obj.value.elements[index.value]
        else:
            self.raise_error(InterpreterErrorMsg.INVALID_INDEX)

    def list_length(self, obj: LValue) -> LValue:
        return LValue(ValueType.INT, len(obj.value.elements))

    def list_append(self, obj: LValue, element: Variable) -> None:
        obj.value.elements.append(LValue(element.type, element.value))

    def list_pop(self, obj: LValue) -> None:
        if len(obj.value.elements) > 0:
            obj.value.elements.pop()
        else:
            self.raise_error(InterpreterErrorMsg.LIST_IS_EMPTY)

    def pair_key(self, obj: LValue) -> LValue:
        return obj.value.key

    def pair_value(self, obj: LValue) -> LValue:
        return obj.value.value

    def dict_has_key(
        self,
        obj: LValue,
        wanted_key: Variable
    ) -> LValue:
        for element in obj.value.elements:
            if element[0] == LValue(wanted_key.type, wanted_key.value):
                return LValue(ValueType.BOOL, True)
        return LValue(ValueType.BOOL, False)

    def dict_sort(
        self,
        obj: LValue,
        sorting_function_name: Variable
    ) -> None:
        if sorting_function_name.type != ValueType.FUNCTION_NAME:
            self.raise_error(InterpreterErrorMsg.ARG_INVALID_TYPE)
        sorting_function = self._functions[sorting_function_name.value]

        n = len(obj.value.elements)
        if n <= 1:
            self._result = Result(ResultType.LVALUE, obj)
            return

        for i in range(n):
            swap_took_place = False
            for j in range(n - i - 1):
                first_pair = Variable(
                    sorting_function.parameters[0],
                    ValueType.PAIR,
                    InterpreterPair(
                        obj.value.elements[j][0],
                        obj.value.elements[j][1]
                    )
                )
                second_pair = Variable(
                    sorting_function.parameters[1],
                    ValueType.PAIR,
                    InterpreterPair(
                        obj.value.elements[j + 1][0],
                        obj.value.elements[j + 1][1]
                    )
                )

                self._add_context(sorting_function_name)
                for var in [first_pair, second_pair]:
                    self._create_variable_in_last_scope(
                        var.name, var.type, var.value)
                sorting_function.accept(self)
                self._pop_context()

                should_not_swap = self.get_lvalue_from_result().value
                if should_not_swap is False:
                    obj.value.elements[j], obj.value.elements[j + 1] = (
                        obj.value.elements[j + 1], obj.value.elements[j]
                    )
                    swap_took_place = True

            if not swap_took_place:
                break

    def dict_by_index(self, obj: LValue, index: Variable) -> LValue:
        if index.type != ValueType.INT:
            self.raise_error(InterpreterErrorMsg.ARG_INVALID_TYPE)
        if index.value in range(0, len(obj.value.elements)):
            return LValue(
                ValueType.PAIR,
                InterpreterPair(*obj.value.elements[index.value])
            )
        else:
            self.raise_error(InterpreterErrorMsg.INVALID_INDEX)

    def dict_by_key(self, obj: LValue, key: Variable) -> LValue:
        for pair in obj.value.elements:
            if pair[0] == LValue(key.type, key.value):
                return pair[1]
        self.raise_error(InterpreterErrorMsg.NO_SUCH_KEY_IN_DICT)

    def dict_length(self, obj: LValue) -> LValue:
        return LValue(ValueType.INT, len(obj.value.elements))

    def dict_append(self, obj: LValue, new_pair: Variable) -> None:
        if new_pair.type != ValueType.PAIR:
            self.raise_error(InterpreterErrorMsg.ARG_INVALID_TYPE)

        for pair in obj.value.elements:
            if pair[0] == new_pair.value.key:
                self.raise_error(InterpreterErrorMsg.DICT_KEY_EXISTS)
        obj.value.elements.append((new_pair.value.key, new_pair.value.value))

    def dict_pop(self, obj: LValue) -> None:
        if len(obj.value.elements) > 0:
            obj.value.elements.pop()
        else:
            self.raise_error(InterpreterErrorMsg.DICT_IS_EMPTY)

    def global_print(self, what: Variable) -> None:
        obj_as_str = str(LValue(what.type, what.value))
        self._output_stream.write(obj_as_str + '\n')

    def global_bool(self, what: Variable) -> LValue:
        match what.type:
            case ValueType.BOOL:
                value = what.value
            case (ValueType.INT | ValueType.FLOAT | ValueType.STRING):
                value = bool(what.value)
            case ValueType.DICT | ValueType.LIST:
                value = len(what.value.elements) != 0
            case ValueType.PAIR | ValueType.FUNCTION_NAME:
                value = True
        return LValue(ValueType.BOOL, value)

    def global_int(self, what: Variable) -> LValue:
        match what.type:
            case ValueType.BOOL:
                value = 1 if what.value is True else 0
            case ValueType.INT:
                value = what.value
            case ValueType.FLOAT:
                value = int(what.value)
            case ValueType.STRING:
                try:
                    value = int(what.value)
                except ValueError:
                    self.raise_error(InterpreterErrorMsg.INVALID_VALUE)
            case (ValueType.DICT
                  | ValueType.LIST
                  | ValueType.PAIR
                  | ValueType.FUNCTION_NAME):
                self.raise_error(InterpreterErrorMsg.INVALID_VALUE)
        return LValue(ValueType.INT, value)

    def global_float(self, what: Variable) -> LValue:
        match what.type:
            case ValueType.BOOL:
                value = 1.0 if what.value is True else 0.0
            case ValueType.INT:
                value = float(what.value)
            case ValueType.FLOAT:
                value = what.value
            case ValueType.STRING:
                try:
                    value = float(what.value)
                except ValueError:
                    self.raise_error(InterpreterErrorMsg.INVALID_VALUE)
            case (ValueType.DICT
                  | ValueType.LIST
                  | ValueType.PAIR
                  | ValueType.FUNCTION_NAME):
                self.raise_error(InterpreterErrorMsg.INVALID_VALUE)
        return LValue(ValueType.FLOAT, value)

    def global_string(self, what: Variable) -> LValue:
        return LValue(
            ValueType.STRING,
            str(LValue(what.type, what.value))
        )

# TODO te same klucze slownika?