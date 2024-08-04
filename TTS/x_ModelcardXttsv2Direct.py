from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

import torch
#import os
#os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = 1

config = XttsConfig()
config.load_json("xtts/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="xtts/", eval=True)

#model.cuda()
#mps_device = torch.device("mps")
#model.to(mps_device)
model.to("cpu")

outputs = model.synthesize(
    "It took me quite a long time to develop a voice and now that I have it I am not going to be silent.",
    config,
    speaker_wav="gandalf.wav",
    gpt_cond_len=3,
    language="en",
)
