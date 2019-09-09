HOST_PYTHON=$(shell which python3.8 || which python3.7 || which python3.6)
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

PYC=$(shell find . -name '*.pyc')
OK_PIP=.ok_pip
OK_REQ=.ok_req
OK_TESTS=.ok_tests
OK_VENV=.ok_venv

OK+=$(OK_PIP)
OK+=$(OK_REQ)
OK+=$(OK_TESTS)
OK+=$(OK_VENV)

all: $(OK_TESTS)

clean:
	rm -rf __pycache__
	rm -f $(PYC) $(OK)

envclean:
	rm -rf $(VENV)

$(VENV):
	$(HOST_PYTHON) -m venv $(VENV) && touch $@

$(OK_PIP): $(VENV)
	$(PIP) install --upgrade pip && touch $@

$(OK_REQ): $(OK_PIP) requirements.txt
	$(PIP) install -r requirements.txt && touch $@

$(OK_TESTS): $(OK_REQ) *.py app/*.py app/api/v1/*.py tests/*.py
		$(PYTHON) -m unittest discover -s tests && touch $@

run: $(OK_TESTS)
	PATH=$(VENV)/bin:$(PATH) FLASK_DEBUG=1 FLASK_APP=flow.py flask run
