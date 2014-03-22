from rpythonex.rcircular import CircularArray
from rpythonex.ratomic import compare_and_swap
from rpython.rtyper.lltypesystem import llmemory, lltype, rffi
import ctypes


def _malloc_signed(initial_value):
        SIGNEDP = lltype.Array(lltype.Signed, hints={'nolength': True})
        value = lltype.malloc(SIGNEDP, 1, flavor='raw')
        value[0] = initial_value
        return value


class CircularWorkStealingDeque(object):
    def __init__(self, log_initial_size):
        self.bottom = _malloc_signed(0)
        self.top = _malloc_signed(0)
        self.active_array = CircularArray(log_initial_size)


    def _cas_top(self, oldval, newval):
        return compare_and_swap(self.top, oldval, newval)

    def push_bottom(self, value):
        bottom = self.bottom[0]
        top = self.top[0]
        array = self.active_array

        size = bottom - top

        if size >= array.size() - 1:
            array = array.grow(bottom, top)
            self.active_array = array

        array.put(bottom, value)
        self.bottom[0] = bottom + 1

    def steal(self):
        top = self.top[0]
        bottom = self.bottom[0]
        array = self.active_array
        size = bottom - top

        if size <= 0:
            return None

        value = array.get(top)

        if not self._cas_top(top, top + 1):
            return None

        return value

    def pop_bottom(self):
        bottom = self.bottom[0]
        array = self.active_array
        bottom -= 1
        self.bottom[0] = bottom
        top = self.top[0]
        size = bottom - top
        if size < 0:
            self.bottom[0] = top
            return None
        value = array.get(bottom)
        if size > 0:
            return value

        if not self._cas_top(top, top + 1):
            value = None

        self.bottom[0] = top + 1
        return value