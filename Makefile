PYPYPATH?=~/code/python/pypy/
PYTEST?=py.test
PYTESTARGS=
RPYTHON?=$(PYPYPATH)/rpython/bin/rpython

all: test_compiler test_interpreter test_vmobjects test_vm

compile: debugger bin/wlvlang-python wlvlang-no-jit

debugger: bin/wlvdbg

wlvlang-no-jit:
	@mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch wlvlang/targetstandalone.py
	@mv ./wlvlang-nojit ./bin/

wlvlang-jit:
	@mkdir -p bin/
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(RPYTHON) --batch -Ojit wlvlang/targetstandalone.py
	@mv ./wlvlang-jit ./bin/

bin/wlvlang-python:
	@mkdir -p bin/
	@cat ./wlvlang/wlvlang-python | sed 's,{PYTHON_PATH},$(PYTHONPATH):$(PYPYPATH):.,g' > ./bin/wlvlang-python
	@chmod +x bin/wlvlang-python

bin/wlvdbg:
	@mkdir -p bin/
	@cat ./wlvlang/wlvdbg | sed 's,{PYTHON_PATH},$(PYTHONPATH):$(PYPYPATH):.,g' > ./bin/wlvdbg
	@chmod +x bin/wlvlang-python

createdist:
	python setup.py sdist

test_compiler:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/compiler/test_*.py

test_interpreter:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/interpreter/test_*.py

test_objectspace:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/objectspace/test_*.py

test_runtime:
	@PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. $(PYTEST) $(PYTESTARGS) tests/runtime/test_*.py

test_full_run:
	PYTHONPATH=$(PYTHONPATH):$(PYPYPATH):. python wlvlang/targetstandalone.py tests/sources/test_simple_function.wl

test_functional: bin/wlvlang-python
	@tests/functional/wlvtest.py --xml ./bin/wlvlang-python ./tests/functional


clean:
	rm -rf MANIFEST
	rm -rf dist/
	rm -rf build/

.PHONY: createdist
