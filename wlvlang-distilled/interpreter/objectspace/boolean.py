from wlvlang.interpreter.objectspace.object import Object

class Boolean(Object):
    """ Represents a Boolean object """

    def __init__(self, value):
        self.value = value

    def get_boolean_value(self):
        return self.value

    def get_as_string(self):
        return str(self)

    def __str__(self):
        return "true" if self._value else "false"

    def __eq__(self, other):
        return isinstance(other, Boolean) and other._value == self._value

    def get_class(self, space):
        return space.booleanClass
