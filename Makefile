all: src/lex.py src/printer.py src/tokenizer.py
	mkdir bin/
	cp src/printer.py bin/lexer
	chmod +x bin/lexer

clean:
	rm -rf bin/* src/{*.pyc,__pycache__,lextab.py} includes/{*.pyc,__pycache__}
