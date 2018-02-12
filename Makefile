ass1: src/lex.py src/printer.py src/tokenizer.py
	mkdir bin/
	cp src/printer.py bin/lexer
	chmod +x bin/lexer

ass2: src/codegen.py
	mkdir bin/
	cp src/codegen.py bin/codegen
	chmod +x bin/codegen

clean:
	rm -rf bin src/{*.pyc,__pycache__,lextab.py} includes/{*.pyc,__pycache__}
