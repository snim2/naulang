from rply import ParserGenerator
from rply.errors import ParsingError

from naulang.compiler import ast
from naulang.compiler.lexer import get_tokens, get_lexer

tokentypes, _ = zip(*get_tokens())

pg = ParserGenerator(tokentypes,
                     precedence=[
                         ("right", ["UMINUS"]),
                         ("right", ["NEGATE"]),
                         ("left", ["CHAN_IN"]),
                         ("right", ["CHAN_OUT"]),
                         ("left", ["OR", "AND"]),
                         ("nonassoc", ["IS", "DOUBLE_EQ"]),
                         ("nonassoc", ["LT", "GT", "LTEQ", "GTEQ"]),
                         ("left", ["PLUS", "MINUS"]),
                         ("left", ["MUL", "DIV", "MOD"]),
                     ], cache_id="naulang-parser-test")

@pg.production("main : statement_block")
def main(p):
    return p[0]

@pg.production("statement_block : statement_block statement")
def statement_list(p):
    if p[0] is None:
        return ast.Block([p[1]], p[1].getsourcepos())

    return ast.Block(p[0].get_statements() + [p[1]], p[0].getsourcepos())

@pg.production("statement_block : none")
def statement_list_none(p):
    return p[0]

@pg.production("statement : expression")
def statement_expression(p):
    return p[0]

@pg.production("statement : BREAK")
def statement_break(p):
    return ast.BreakStatement(p[0].getsourcepos())

@pg.production("statement : CONTINUE")
def statement_continue(p):
    return ast.ContinueStatement(p[0].getsourcepos())

@pg.production("statement : PRINT expression")
def statement_print(p):
    return ast.PrintStatement(p[1], p[0].getsourcepos())

@pg.production("statement : RETURN expression")
def statement_return(p):
    return ast.ReturnStatement(p[1], p[0].getsourcepos())

@pg.production("statement : RETURN none")
def statement_return_none(p):
    return ast.ReturnStatement(p[1], p[0].getsourcepos())

@pg.production("statement : IF expression LBRACE statement_block RBRACE")
def statement_if(p):
    return ast.IfStatement(p[1], p[3], p[0].getsourcepos())


@pg.production("statement : WHILE expression LBRACE statement_block RBRACE")
def statement_while(p):
    return ast.WhileStatement(p[1], p[3], p[0].getsourcepos())

@pg.production("expression : array_access")
def expression_array_access(p):
    return p[0]

@pg.production("array_access : expression LBRACK expression RBRACK")
def statement_array_access(p):
    return ast.ArrayAccess(p[0], p[2], p[0].getsourcepos())

@pg.production("statement : IDENTIFIER EQUAL expression")
def statement_assignment(p):
    return ast.Assignment(p[0].getstr(), p[2], p[1].getsourcepos())

@pg.production("statement : LET IDENTIFIER EQUAL expression")
def statement_scope_assignment(p):
    return ast.ScopedAssignment(p[1].getstr(), p[3], p[0].getsourcepos())

@pg.production("statement : array_access EQUAL expression")
def statement_array_assignment(p):
    return ast.ArrayAssignment(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : FN LPAREN parameter_list RPAREN LBRACE statement_block RBRACE")
def expression_function(p):
    return ast.FunctionExpression(p[2], p[5], p[0].getsourcepos())

@pg.production("expression : IDENTIFIER LPAREN argument_list RPAREN")
def statement_function_invocation(p):
    return ast.FunctionCall(ast.IdentifierExpression(p[0].getstr()), p[2], p[0].getsourcepos())

@pg.production("expression : ASYNC IDENTIFIER LPAREN argument_list RPAREN")
def statement_async_function_invocation(p):
    return ast.AsyncFunctionCall(ast.IdentifierExpression(p[1].getstr()), p[3], p[0].getsourcepos())

@pg.production("expression : FN IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_block RBRACE")
def statement_function(p):
    return ast.FunctionStatement(p[1].getstr(), p[3], p[6], p[0].getsourcepos())

@pg.production("expression : CHAN_OUT IDENTIFIER")
def statement_chanout(p):
    return ast.ChannelOut(ast.IdentifierExpression(p[1].getstr(), p[1].getsourcepos()), p[0].getsourcepos())

@pg.production("expression : IDENTIFIER CHAN_IN expression")
def statement_chanin(p):
    return ast.ChannelIn(ast.IdentifierExpression(p[0].getstr(), p[0].getsourcepos()), p[2], p[1].getsourcepos())

@pg.production("argument_list : arg_opt expression comma_elision")
def argument_list(p):
    if p[0] is None:
        return ast.ArgumentList([p[1]], p[1].getsourcepos())

    return ast.ArgumentList(p[0].get_argument_list() + [p[1]], p[0].getsourcepos())

@pg.production("argument_list : none")
def arg_list_none(p):
    return ast.ArgumentList([], None)

@pg.production("arg_opt : arg_opt expression COMMA")
def arg_opt(p):
    if p[0] is None:
        return ast.ArgumentList([p[1]], p[1].getsourcepos())

    return ast.ArgumentList(p[0].get_argument_list() + [p[1]], p[0].getsourcepos())

@pg.production("arg_opt : none")
def arg_opt_none(p):
    return p[0]

@pg.production("parameter_list : param_opt IDENTIFIER comma_elision")
def param_list(p):
    if p[0] is None:
        return ast.ParameterList([p[1].getstr()], p[1].getsourcepos())

    return ast.ParameterList(p[0].get_parameter_list() + [p[1].getstr()], p[0].getsourcepos())

@pg.production("parameter_list : none")
def param_list_none(p):
    return ast.ParameterList([], None)

@pg.production("param_opt : param_opt IDENTIFIER COMMA")
def param_opt(p):
    if p[0] is None:
        return ast.ParameterList([p[1].getstr()], p[1].getsourcepos())

    return ast.ParameterList(p[0].get_parameter_list() + [p[1].getstr()], p[0].getsourcepos())

@pg.production("param_opt : none")
def param_opt_none(p):
    return p[0]

@pg.production("comma_elision : COMMA")
@pg.production("comma_elision : none")
def comma_elision(p):
    return None

@pg.production("expression : INTEGER")
def expression_integer_literal(p):
    return ast.IntegerConstant(int(p[0].getstr()), p[0].getsourcepos())

@pg.production("expression : FLOAT")
def expression_float_literal(p):
    return ast.FloatConstant(float(p[0].getstr()), p[0].getsourcepos())

@pg.production("expression : TRUE")
@pg.production("expression : FALSE")
def expression_literal_bool(p):
    if p[0].gettokentype() == "TRUE":
        return ast.BooleanConstant(True, p[0].getsourcepos())

    return ast.BooleanConstant(False, p[0].getsourcepos())

@pg.production("expression : STRING")
def expression_string(p):
    string = p[0].getstr()
    if string.startswith('"') and string.endswith('"'):
            string = string[:-1]
            string = string[1:]
    return ast.StringConstant(string, p[0].getsourcepos())

@pg.production("expression : expression AND expression")
def expression_and(p):
    return ast.And(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression OR expression")
def expression_or(p):
    return ast.Or(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression LT expression")
def expression_lt(p):
    return ast.LessThan(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression GT expression")
def expression_gt(p):
    return ast.GreaterThan(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression LTEQ expression")
def expression_lteq(p):
    return ast.LessThanOrEqual(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression GTEQ expression")
def expression_gteq(p):
    return ast.GreaterThanOrEqual(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression PLUS expression")
def expression_plus(p):
    return ast.Add(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression MINUS expression")
def expression_minus(p):
    return ast.Subtract(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : MINUS expression", precedence="UMINUS")
def expression_negate(p):
    return ast.UnaryNegate(p[1], p[0].getsourcepos())

@pg.production("expression : expression MUL expression")
def expression_multiply(p):
    return ast.Multiply(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression DIV expression")
def expression_divide(p):
    return ast.Divide(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression MOD expression")
def expression_mod(p):
    return ast.Mod(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : LPAREN expression RPAREN")
def expression_parens(p):
    return p[1]

@pg.production("expression : NOT expression")
def expression_unary_not(p):
    return ast.UnaryNot(p[1], p[0].getsourcepos())

@pg.production("expression : expression IS expression")
@pg.production("expression : expression DOUBLE_EQ expression")
def expression_equality(p):
    return ast.Equals(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : expression NOT_EQ expression")
def expression_notequals(p):
    return ast.NotEquals(p[0], p[2], p[1].getsourcepos())

@pg.production("expression : IDENTIFIER")
def expression_identifier(p):
    return ast.IdentifierExpression(p[0].getstr(), p[0].getsourcepos())

@pg.production("none : ")
def none(p):
    return None

@pg.error
def error_handler(token):
    raise ParsingError("Ran into a '%s' where it was't expected" % token.getstr(), token.getsourcepos())

PARSER = pg.build()

def create_parser():
    return PARSER

def create_lexer():
    return get_lexer()
