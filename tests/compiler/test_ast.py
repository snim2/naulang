from wlvlang.compiler import ast
from wlvlang.compiler.context import MethodCompilerContext

from wlvlang.vm.vm_universe import VM_Universe
from wlvlang.interpreter.bytecode import Bytecode

from wlvlang.vmobjects.boolean import Boolean
from wlvlang.vmobjects.integer import Integer

class DummyNode(ast.Node):

    def __init__(self, value):
        self.value = value

    def compile(self, context):
        pass

    def __repr__(self):
        return "DummyNode(%r)" % self.value


def test_ast_integer_constant():
    assert ast.IntegerConstant(10) == ast.IntegerConstant(10)
    assert ast.IntegerConstant(1231) != ast.IntegerConstant(123231)


def test_ast_boolean_constant():
    assert ast.BooleanConstant(True) == ast.BooleanConstant(True)
    assert ast.BooleanConstant(False) == ast.BooleanConstant(False)

def test_ast_assignment():
    assert ast.Assignment('a', DummyNode(100)) == ast.Assignment('a', DummyNode(100))
    assert ast.Assignment('a', DummyNode(10)) != ast.Assignment('a', DummyNode(100))

def test_ast_statement():
    assert ast.Statement(DummyNode(True)) == ast.Statement(DummyNode(True))
    assert ast.Statement(DummyNode(False)) != ast.Statement(DummyNode(True))

def test_ast_or():
    assert ast.Or(DummyNode(True), DummyNode(True)) == ast.Or(DummyNode(True), DummyNode(True))
    assert ast.Or(DummyNode(False), DummyNode(True)) != ast.Or(DummyNode(True), DummyNode(True))

def test_ast_and():
    assert ast.And(DummyNode(True), DummyNode(True)) == ast.And(DummyNode(True), DummyNode(True))
    assert ast.And(DummyNode(False), DummyNode(True)) != ast.And(DummyNode(True), DummyNode(True))

def test_ast_equals():
    assert ast.Equals(DummyNode(True), DummyNode(True)) == ast.Equals(DummyNode(True), DummyNode(True))
    assert ast.Equals(DummyNode(False), DummyNode(True)) != ast.Equals(DummyNode(True), DummyNode(True))

def test_ast_notequals():
    assert ast.NotEquals(DummyNode(True), DummyNode(True)) == ast.NotEquals(DummyNode(True), DummyNode(True))
    assert ast.NotEquals(DummyNode(False), DummyNode(True)) != ast.NotEquals(DummyNode(True), DummyNode(True))

def test_ast_lessthan():
    assert ast.LessThan(DummyNode(True), DummyNode(True)) == ast.LessThan(DummyNode(True), DummyNode(True))
    assert ast.LessThan(DummyNode(False), DummyNode(True)) != ast.LessThan(DummyNode(True), DummyNode(True))

def test_ast_lessthanorequal():
    assert ast.LessThanOrEqual(DummyNode(True), DummyNode(True)) == ast.LessThanOrEqual(DummyNode(True), DummyNode(True))
    assert ast.LessThanOrEqual(DummyNode(False), DummyNode(True)) != ast.LessThanOrEqual(DummyNode(True), DummyNode(True))

def test_ast_greaterthanorequal():
    assert ast.GreaterThanOrEqual(DummyNode(True), DummyNode(True)) == ast.GreaterThanOrEqual(DummyNode(True), DummyNode(True))
    assert ast.GreaterThanOrEqual(DummyNode(False), DummyNode(True)) != ast.GreaterThanOrEqual(DummyNode(True), DummyNode(True))

def test_ast_greaterthan():
    assert ast.GreaterThan(DummyNode(True), DummyNode(True)) == ast.GreaterThan(DummyNode(True), DummyNode(True))
    assert ast.GreaterThan(DummyNode(False), DummyNode(True)) != ast.GreaterThan(DummyNode(True), DummyNode(True))

def test_ast_addop():
    assert ast.AddOp(DummyNode(True), DummyNode(True)) == ast.AddOp(DummyNode(True), DummyNode(True))
    assert ast.AddOp(DummyNode(False), DummyNode(True)) != ast.AddOp(DummyNode(True), DummyNode(True))

def test_ast_subtractop():
    assert ast.SubtractOp(DummyNode(True), DummyNode(True)) == ast.SubtractOp(DummyNode(True), DummyNode(True))
    assert ast.SubtractOp(DummyNode(False), DummyNode(True)) != ast.SubtractOp(DummyNode(True), DummyNode(True))

def test_ast_mulop():
    assert ast.MulOp(DummyNode(True), DummyNode(True)) == ast.MulOp(DummyNode(True), DummyNode(True))
    assert ast.MulOp(DummyNode(False), DummyNode(True)) != ast.MulOp(DummyNode(True), DummyNode(True))
