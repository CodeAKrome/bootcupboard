# cp lib from brew
mkdir -p /Users/kyle/hub/bootcupboard/stable-audio/.venv/lib/python3.11/site-packages/_soundfile_data
cp /opt/homebrew/lib/libsndfile.dylib /Users/kyle/hub/bootcupboard/stable-audio/.venv/lib/python3.11/site-packages/_soundfile_data
pip install -r requirements.txt
PytorchNightly.sh
export TOKENIZERS_PARALLELISM=false
