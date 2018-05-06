init:
	virtualenv --no-site-packages --distribute -p python3 env
	pip install -r requirements.txt
test:
	. env/bin/activate; py.test tests
clean:
	rm -rf env
