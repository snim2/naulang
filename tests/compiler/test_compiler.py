from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.integer import Integer


class DummyCompilationUnit(ast.Node):
    def __init__(self, code_to_emit):
        self.code_to_emit = chr(code_to_emit)

    def compile(self, context):
        context.emit(self.code_to_emit)

    def __repr__(self):
        return "DummyCompilationUnit(%r)" % self.code_to_emit

def create_interpreter_context():
    universe = VM_Universe()
    ctx = MethodCompilerContext(universe)
    return ctx

def test_ast_integer_compile():
    ctx = create_interpreter_context()
    node = ast.IntegerConstant(100)
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Integer(100)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0)]

def test_ast_boolean_constant_compiler():
    ctx = create_interpreter_context()
    node = ast.BooleanConstant(True)
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0 (as this was a new context)
    assert ctx._literals[0] == Boolean(True)

    # Expect the byte code to be [Bytecode.LOAD_CONST, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0)]

def test_ast_assignment_compiler():
    ctx = create_interpreter_context()
    node = ast.Assignment('a', ast.BooleanConstant(True))
    node.compile(ctx)

    # Expect the constant to be stored in the literals area at position 0
    assert ctx._literals[0] == Boolean(True)

    # Expect the bytecode to be [Bytecode.LOAD_CONST, 0, Bytecode.STORE, 0]
    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0), Bytecode.STORE, chr(0)]

def test_ast_or_compiler():
    ctx = create_interpreter_context()
    node = ast.Or(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    # Expect bytecode: [91, 90, Bytecode.OR]
    assert ctx.bytecode == [chr(91), chr(90), Bytecode.OR]

def test_ast_and_compiler():
    ctx = create_interpreter_context()
    node = ast.And(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.AND]

def test_ast_equals_compiler():
    ctx = create_interpreter_context()
    node = ast.Equals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.EQUAL]

def test_ast_not_equals_compiler():
    ctx = create_interpreter_context()
    node = ast.NotEquals(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.NOT_EQUAL]

def test_ast_lessthan_compiler():
    ctx = create_interpreter_context()
    node = ast.LessThan(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.LESS_THAN]

def test_ast_lessthanorequal_compiler():
    ctx = create_interpreter_context()
    node = ast.LessThanOrEqual(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.LESS_THAN_EQ]

def test_ast_greaterthanorequal_compiler():
    ctx = create_interpreter_context()
    node = ast.GreaterThanOrEqual(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.GREATER_THAN_EQ]

def test_ast_greaterthan_compiler():
    ctx = create_interpreter_context()
    node = ast.GreaterThan(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.GREATER_THAN]

def test_ast_addop_compiler():
    ctx = create_interpreter_context()
    node = ast.AddOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.ADD]

def test_ast_subtractop_compiler():
    ctx = create_interpreter_context()
    node = ast.SubtractOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.SUB]

def test_ast_mulop_compiler():
    ctx = create_interpreter_context()
    node = ast.MulOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.MUL]

def test_ast_divop_compiler():
    ctx = create_interpreter_context()
    node = ast.DivOp(DummyCompilationUnit(91), DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(91), chr(90), Bytecode.DIV]

def test_ast_unarynot_compiler():
    ctx = create_interpreter_context()
    node = ast.UnaryNot(DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(90), Bytecode.NOT]

def test_ast_unarynegate_compiler():
    ctx = create_interpreter_context()
    node = ast.UnaryNegate(DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(90), Bytecode.NEG]

def test_ast_whilestatement_compiler():
    ctx = create_interpreter_context()

    # Add padding to bytecodes to test non-zero based context (this is more realistic)
    ctx.emit(chr(100))
    node = ast.WhileStatement(DummyCompilationUnit(90), ast.Block([DummyCompilationUnit(91)]))
    node.compile(ctx)

    assert ctx.bytecode == [chr(100), chr(90), Bytecode.JUMP_IF_FALSE, chr(7), chr(91), Bytecode.JUMP_BACK, chr(1)]

def test_ast_ifstatement_compiler():
    ctx = create_interpreter_context()

    # Add padding to bytecodes to test non-zero based context (this is more realistic)
    ctx.emit(chr(100))
    node = ast.IfStatement(DummyCompilationUnit(90), ast.Block([DummyCompilationUnit(91)]))
    node.compile(ctx)

    assert ctx.bytecode == [chr(100), chr(90), Bytecode.JUMP_IF_FALSE, chr(5), chr(91)]

def test_ast_printstatement():
    ctx = create_interpreter_context()

    node = ast.PrintStatement(DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(90), Bytecode.PRINT]

def test_ast_functionstatement():
    ctx = create_interpreter_context()

    node = ast.FunctionStatement(['a'], ast.Block([DummyCompilationUnit(90)]))
    node.compile(ctx)

    assert ctx.bytecode == [Bytecode.LOAD_CONST, chr(0)]
    assert len(ctx._inner_contexts) == 1
    assert ctx._inner_contexts[0].bytecode == [chr(90)]
    assert ctx._inner_contexts[0].has_local('a') == True

def test_ast_functioncall():
    ctx = create_interpreter_context()

    node = ast.FunctionCall('a', [DummyCompilationUnit(90), DummyCompilationUnit(91)])
    node.compile(ctx)

    assert ctx.bytecode == [chr(90), chr(91), Bytecode.INVOKE, chr(0)]

def test_ast_returnstatement():
    ctx = create_interpreter_context()

    node = ast.ReturnStatement(DummyCompilationUnit(90))
    node.compile(ctx)

    assert ctx.bytecode == [chr(90), Bytecode.RETURN]
