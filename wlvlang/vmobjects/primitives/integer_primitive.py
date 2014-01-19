from wlvlang.vmobjects.integer import Integer
from wlvlang.vmobjects.boolean import Boolean

def _mul(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() * right.get_value()
    activation_record.push(Integer(result))

def _add(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() + right.get_value()
    activation_record.push(Integer(result))

def _sub(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() - right.get_value()
    activation_record.push(Integer(result))

def _div(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    if (right.get_value() == 0):
        pass
        #TODO: Division by zero, exception

    result = left.get_value() / right.get_value()
    activation_record.push(Integer(result))

def _mod(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_value() % right.get_value()
    activation_record.push(Integer(result))

def _eq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() == right.get_value()

    activation_record.push(Boolean(result))

def _lt(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() < right.get_value()
    activation_record.push(Boolean(result))


def _gt(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left  = activation_record.pop()

    result = left.get_value() > right.get_value()

    activation_record.push(Boolean(result))
