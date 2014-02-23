from wlvlang.vmobjects.object import Object

class Array(Object):

    def __init__(self, initial_size):
        self._list = [None] * int(initial_size)

    def get_value_at(self, index):
        return self._list[int(index)]

    def set_value_at(self, index, value):
        self._list[int(index)] = value

    def get_class(self, universe):
        return universe.arrayClass

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return "vmobject.Array(%r)" % self._list

    def __eq__(self, other):
        return isinstance(other, Array) and self._list is other._list
