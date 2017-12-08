VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
OK_VENV=.ok_venv
OK_REQ=.ok_req
OK_TESTS=.ok_tests

OK=$(OK_VENV)
OK+=$(OK_REQ)
OK+=$(OK_TESTS)

all: $(OK_TESTS)

clean:
	rm -rf __pycache__ $(OK)

$(OK_VENV):
	python3 -m venv $(VENV) && touch $@

$(OK_REQ): $(OK_VENV) requirements.txt
		$(PIP) install -r requirements.txt && touch $@

$(OK_TESTS): $(OK_REQ) app/tests/*.py *.py
		$(PYTHON) -m unittest discover -s app/unittests && touch $@
