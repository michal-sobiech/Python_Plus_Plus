# from project.parser.ast_nodes.conditional_statements.ConditionalStatement import ConditionalStatement
# from project.parser.ast_nodes.conditional_statements.ElifStatement import ElifStatement
# from project.parser.ast_nodes.conditional_statements.ElseStatement import ElseStatement
# from project.parser.ast_nodes.conditional_statements.IfStatement import IfStatement

# from project.parser.ast_nodes.dict.Dict import Dict
# from project.parser.ast_nodes.dict.DictElement import DictElement
# from project.parser.ast_nodes.dict.Pair import Pair

# from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

# from project.parser.ast_nodes.function.call.FunctionCall import FunctionCall

# from project.parser.ast_nodes.function.definition.FunctionDefinition import FunctionDefinition

# from project.parser.ast_nodes.incr_decr_statement.DecrementStatement import DecrementStatement
# from project.parser.ast_nodes.incr_decr_statement.IncrementStatement import IncrementStatement

# from project.parser.ast_nodes.linq.LinqQuery import LinqQuery

# from project.parser.ast_nodes.list.List import List

# from project.parser.ast_nodes.literal.BoolLiteral import BoolLiteral
# from project.parser.ast_nodes.literal.FloatLiteral import FloatLiteral
# from project.parser.ast_nodes.literal.IntLiteral import IntLiteral
# from project.parser.ast_nodes.literal.StringLiteral import StringLiteral

# from project.parser.ast_nodes.node.NodeABC import NodeABC

# from project.parser.ast_nodes.operator_terms.add_or_sub_term.AdditionTerm import AdditionTerm
# from project.parser.ast_nodes.operator_terms.add_or_sub_term.SubtractionTerm import SubtractionTerm

# from project.parser.ast_nodes.operator_terms.and_term.AndTerm import AndTerm

# from project.parser.ast_nodes.operator_terms.comparison_term.CompTermABC import CompTermABC
# from project.parser.ast_nodes.operator_terms.comparison_term.EqualTerm import EqualTerm
# from project.parser.ast_nodes.operator_terms.comparison_term.GreaterEqualTerm import GreaterEqualTerm
# from project.parser.ast_nodes.operator_terms.comparison_term.GreaterTerm import GreaterTerm
# from project.parser.ast_nodes.operator_terms.comparison_term.LessEqualTerm import LessEqualTerm
# from project.parser.ast_nodes.operator_terms.comparison_term.LessTerm import LessTerm

# from project.parser.ast_nodes.operator_terms.mul_or_div_term.MulOrDivTermABC import MulOrDivTermABC
# from project.parser.ast_nodes.operator_terms.mul_or_div_term.MultiplicationTerm import MultiplicationTerm
# from project.parser.ast_nodes.operator_terms.mul_or_div_term.DivisionTerm import DivisionTerm

# from project.parser.ast_nodes.operator_terms.not_term.NotTerm import NotTerm

# from project.parser.ast_nodes.operator_terms.or_term.OrTerm import OrTerm

# from project.parser.ast_nodes.operator_terms.unary_minus_term.UnaryMinusTerm import UnaryMinusTerm

# from project.parser.ast_nodes.operator_terms.DotTerm import DotTerm

# from project.parser.ast_nodes.return_statement.ReturnABC import ReturnABC
# from project.parser.ast_nodes.return_statement.ReturnNoValue import ReturnNoValue
# from project.parser.ast_nodes.return_statement.ReturnWithValue import ReturnWithValue

# from project.parser.ast_nodes.Assignment import Assignment
# from project.parser.ast_nodes.Block import Block
# from project.parser.ast_nodes.Code import Code
# from project.parser.ast_nodes.ForLoop import ForLoop
# from project.parser.ast_nodes.FunDefOrStatementABC import FunDefOrStatementABC
# from project.parser.ast_nodes.Identifier import Identifier
# from project.parser.ast_nodes.StatementABC import StatementABC
# from project.parser.ast_nodes.WhileLoop import WhileLoop


# class AstVisitor:
#     def __init__(self):
#         pass

#     def visit(self, node: NodeABC):
#         nodes_to_functions = {
#             ConditionalStatement: self.visit_conditional_statement,
#             ElifStatement: self.visit
#         }

#     def visit_conditional_statement(self, node):
#         pass

#     def visit_elif_statement(self, node):
#         pass

#     def visit_else_statement(self, node):
#         pass

#     def visit_if_statement(self, node):
#         pass

#     def visit_dict(self, node):
#         pass

#     def visit_dict_element(self, node):
#         pass

#     def visit_pair(self, node):
#         pass

#     def visit_function_call(self, node):
#         pass

#     def visit_function_definition(self, node):
#         pass

#     def visit_decrement_statement(self, node):
#         pass

#     def visit_increment_statement(self, node):
#         pass

#     def visit_linq_query(self, node):
#         pass

#     def visit_list(self, node):
#         pass

#     def visit_literal(self, node):
#         pass

#     def visit_addition_term(self, node):
#         pass

#     def visit_subtraction_term(self, node):
#         pass

#     def visit_and_term(self, node):
#         pass

#     def visit_comp_term(self, node):
#         pass

#     def visit_mul_term(self, node):
#         pass

#     def visit_div_term(self, node):
#         pass

#     def visit_not_term(self, node):
#         pass

#     def visit_or_term(self, node):
#         pass

#     def visit_unary_minus_term(self, node):
#         pass

#     def visit_dot_term(self, node):
#         pass

#     def visit_return_no_value_term(self, node):
#         pass

#     def visit_return_with_value_term(self, node):
#         pass

#     def visit_assignment(self, node):
#         return self.

#     def visit_block(self, node):
#         pass

#     def visit_code(self, node):
#         for fun_def_or_statment in node.fun_defs_and_statements:
#             if type(fun_def_or_statment) is FunctionDefinition:
#                 return self.visit_function_definition(fun_def_or_statment)
#             else:
#                 return self.visit_statement(fun_def_or_statment)

#     def visit_for_loop(self, node):
#         pass

#     def visit_identifier(self, node):
#         pass

#     def visit_statement(self, node):
#         match type(node):
#             case Assignment:
#                 return self.visit_assignment(node)
#             case ConditionalStatement:
#                 return self.visit_conditional_statement(node)
#             case ForLoop:
#                 return self.visit_for_loop(node)
#             case WhileLoop:
#                 return self.visit_while_loop(node)

#         if isinstance(node, ReturnABC):
#             return self.visit_return(node)
#         elif isinstance(node, ExpressionABC):
#             return self.visit_expression(node)
#         elif isinstance(node, IncrDecrStatementABC):
#             return self.visit_incr_decr_statement(node)

#     def visit_while_loop(self, node):
#         pass

