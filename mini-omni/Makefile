init:
	conda create -n mini-omni python=3.10
activate:
	conda activate mini-omni
deactivate:
	conda deactivate
clone:
	git clone https://github.com/gpt-omni/mini-omni.git
install:
	cd mini-omni; pip install -r requirements.txt
server:
	cd mini-omni; python3 server.py --ip '0.0.0.0' --port 60808
streamlit:
	cd mini-omni; API_URL=http://0.0.0.0:60808/chat streamlit run webui/omni_streamlit.py
gradio:
	cd mini-omni; API_URL=http://0.0.0.0:60808/chat python3 webui/omni_gradio.py
testrun:
	cd mini-omni; python inference.py
