#!/bin/bash

python3 src/par.py ./test/ass4_tests/testCode$1.txt 2> debug
tac debug > debug2
python3 ./src/htmlgenerator.py debug2
rm debug
rm debug2
