VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

PYC=$(shell find . -name '*.pyc')
OK_REQ=.ok_req
OK_TESTS=.ok_tests

OK=$(OK_REQ)
OK+=$(OK_TESTS)

all: $(OK_TESTS)

clean:
	rm -rf __pycache__
	rm -f $(PYC) $(OK)

envclean:
	rm -rf $(VENV)

$(VENV):
	python3 -m venv $(VENV) && touch $@

$(OK_REQ): $(VENV) requirements.txt
		$(PIP) install -r requirements.txt && touch $@

$(OK_TESTS): $(OK_REQ) *.py app/*.py app/api/*.py tests/*.py
		$(PYTHON) -m unittest discover -s tests && touch $@

run: $(OK_TESTS)
		PATH=$(VENV)/bin:$(PATH) FLASK_DEBUG=1 FLASK_APP=flow.py flask run
