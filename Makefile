
code:
	code ./workspace.code-workspace &

getprimes:
	wget http://www.naturalnumbers.org/P-10000.txt -O ./_data/P-10000.txt

Rsa:
	pipenv run python3 ./rsa_tests.py

Sha:
	pipenv run python3 ./sha_tests.py 6 64
