from wlvlang.interpreter.objectspace.primitive_object import PrimitiveObject
from wlvlang.interpreter.objectspace.number import Number

class Integer(Number, PrimitiveObject):

    _immutable_ = True
    _immutable_fields = ["value"]

    def __init__(self, value):
        self.value = value

    def get_integer_value(self):
        return self.value

    def get_as_string(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "int(%s)" % (self.get_as_string())

    def __eq__(self, other):
        return isinstance(other, Integer) and self.value == other.value
