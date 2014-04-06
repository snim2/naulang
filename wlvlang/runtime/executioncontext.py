from wlvlang.interpreter.interpreter import Interpreter
from wlvlang.interpreter.frame import Frame
from wlvlang.interpreter.bytecode import bytecode_names
from rpythonex.rdequeue import CircularWorkStealingDeque
from rpythonex.rcircular import CircularArray

from rpython.rlib import jit, rrandom


def get_printable_location(pc, sched, method):
    return "%d: %s" % (pc, bytecode_names[method.get_bytecode(pc)])

jitdriver = jit.JitDriver(
        greens=['pc', 'sched', 'method'],
        reds=['frame', 'task'],
        virtualizables=['frame'],
        get_printable_location=get_printable_location
    )

def get_printable_location_taskdriver(sched):
    return "TODO"

taskjitdriver = jit.JitDriver(
        greens=['sched'],
        reds='auto',
        get_printable_location=get_printable_location_taskdriver)

class Universe(object):
    def __init__(self, thread_count, space):
        self._rand = rrandom.Random(9)
        self._thread_count = thread_count + 1
        self._thread_local_scheds = [None] * (self._thread_count + 1)
        self.space = space


    def register_scheduler(self, identifier, scheduler):
        index = int(identifier) % self._thread_count
        self._thread_local_scheds[index] = scheduler

    def start(self, main_method, arg_local, arg_array):
        self.main_scheduler = ThreadLocalSched(self.space, self)
        self._bootstrap(main_method, arg_local, arg_array)

        self.register_scheduler(0, self.main_scheduler)
        self._main_sched()


    def _bootstrap(self, main_method, arg_local, arg_array):
        frame = Frame(method=main_method)
        frame.set_local_at(arg_local, arg_array)

        main_task = Task(self.main_scheduler)
        main_task.set_top_frame(frame)

        self.main_scheduler.add_ready_task(main_task)


    def _main_sched(self):
        self.main_scheduler.run()


    @staticmethod
    def run(args, space):
        assert len(args) == 1
        scheduler = ThreadLocalSched(space, args[0])
        scheduler.run()

class TaskCircularArray(CircularArray):
    def _create_new_instance(self, new_size):
        return TaskCircularArray(new_size)

class TaskDequeue(CircularWorkStealingDeque):
    def _initialise_array(self, log_initial_size):
        return TaskCircularArray(log_initial_size)

class ThreadLocalSched(object):
    """ Describes a scheduler for a number of tasks multiplexed onto a single OS Thread """
    _immutable_fields_ = ["interpreter", "universe", "ready_tasks", "yielding_tasks"]

    def __init__(self, space, universe):
        self.ready_tasks = TaskDequeue(8)
        self.yielding_tasks = TaskDequeue(8)

        # Interpreters are mostly stateless (they simply contain code and a
        # reference to a space), they can be shared between local tasks in an
        # execution context
        self.interpreter = Interpreter(space)

        self.universe = universe


    def add_ready_task(self, task):
        self.ready_tasks.push_bottom(task)

    def _reload_yielding_tasks(self):
        while True:
            yielding_task = self.yielding_tasks.steal()
            if yielding_task is None:
                break
            self.ready_tasks.push_bottom(yielding_task)

    def _get_next_task(self):
        task = self.ready_tasks.pop_bottom()

        if task is not None: return task

        self._reload_yielding_tasks()
        return self.ready_tasks.pop_bottom()


    def _can_enter_jit(self, pc, method, task, frame):
        jitdriver.can_enter_jit(
            pc=pc,
            sched=self,
            method=method,
            task=task,
            frame=frame,
        )

    @jit.unroll_safe
    def run_task(self, task):
        assert task is not None

        last_pc = 0
        last_frame = None

        while True:
            pc = task.get_top_frame().get_pc()
            method = task.get_current_method()
            frame = task.get_top_frame()

            still_in_frame = frame is last_frame
            if pc < last_pc and still_in_frame:
                self._can_enter_jit(pc, method, task, frame)

            jitdriver.jit_merge_point(
                    pc=pc,
                    sched=self,
                    method=method,
                    task=task,
                    frame=frame,
                )

            last_pc = pc
            last_frame = frame

            should_continue = self.interpreter.interpreter_step(pc, method, frame, task)

            if not should_continue:
                return


    def run(self):
        while True:
            taskjitdriver.jit_merge_point(sched=self)

            task = self._get_next_task()
            if task is None:
                return

            self.run_task(task)

            if task.get_state() == Interpreter.YIELD:
                self.yielding_tasks.push_bottom(task)
            if task.get_state() == Interpreter.SUSPEND:
                continue
            elif task.get_state() is not Interpreter.HALT:
                self.ready_tasks.push_bottom(task)


class Task(object):
    _immutable_fields_ = ["parent"]

    def __init__(self, owning_scheduler, parent=None):
        """ Create a new task

            kwargs:
                parent  -- The task that spawned this task.
        """
        self._state = Interpreter.CONTINUE
        self.top_frame = None
        self.parent = parent
        self.sched = owning_scheduler

    def get_top_frame(self):
        return self.top_frame

    def set_top_frame(self, frame):
        # Then set the top frame, this context
        # will then continue from the method call
        top_frame = self.get_top_frame()

        if top_frame is not None:
            frame.set_previous_frame(top_frame)

        self.top_frame = frame

    def restore_previous_frame(self):
        self.top_frame = self.get_top_frame().get_previous_frame()

    def get_current_method(self):
        return self.top_frame.method

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def reschedule(self):
        self.sched.add_ready_task(self)

    def __eq__(self, other):
        return self._state == other._state and self.top_frame == other.top_frame and self.parent == other.parent
