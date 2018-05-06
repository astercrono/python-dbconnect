init:
	virtualenv --no-site-packages --distribute -p python3 env
	. env/bin/activate; pip install -r requirements.txt
test:
	. env/bin/activate; py.test tests
clean:
	rm -rf env
