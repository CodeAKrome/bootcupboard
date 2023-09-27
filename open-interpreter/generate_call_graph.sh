HOME=`pwd`
cd ../../../github/open-interpreter/interpreter; pycg $(find . -name "*.py" -type f -and ! -path "./archive/*") -o $HOME/CG.json
../generate_call_graph.py setup_local_text_llm CG.json CG.html
scp CG.html harpo.local:
