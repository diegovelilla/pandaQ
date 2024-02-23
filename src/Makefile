run: pandaQ.py
	antlr4 -Dlanguage=Python3 -no-listener -visitor pandaQ.g4
	streamlit run pandaQ.py

setup: 
	pip install antlr4-tools
	pip install antlr4-python3-runtime
	pip install streamlit

clear:
	rm -rf *.interp *.tokens pandaQLexer* pandaQVisitor* pandaQParser*