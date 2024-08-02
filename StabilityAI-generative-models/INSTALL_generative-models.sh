# create conda environment clone and install the repo
conda create -n stability-genmod python=3.10
conda activate stability-genmod
gh repo clone Stability-AI/generative-models
cd generative-models
python3 -m venv .pt2
source .pt2/bin/activate
pip3 install -r requirements/pt2.txt
pip3 install .
cd ..
pip install -r requirements.txt
