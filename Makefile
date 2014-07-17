all: .venv

.venv:
	virtualenv .venv
	.venv/bin/pip install -r requirements.txt

server: .venv
	.venv/bin/python backend/server.py passcodes-example.txt

door: .venv
	.venv/bin/python doordaemon/doordaemon.py

clean:
	-rm -rf .venv