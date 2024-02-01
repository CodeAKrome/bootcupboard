from diffusers import DiffusionPipeline
import torch

# https://huggingface.co/docs/diffusers/tutorials/using_peft_for_inference
# Adapters for
# https://huggingface.co/models?other=base_model:stabilityai/stable-diffusion-xl-base-1.0


prompt = "toy_face of a hacker with a hoodie"
prompt = "toy_face of a ham radio operator in front of a radio making a transmission"
# Special prompt with keywords to trigger adapters
# toy = toy_face
# pixel = pixel art
#prompt = "toy_face of a ham radio operator in front of a radio making a transmission, pixel art"
prompt = "Drawing of Mickey toy_face as a ham radio operator in front of a radio making a transmission"

lora_scale = 0.9
torch_manual_seed = 0
ni_steps = 30
filename = "test.png"
pipe_id = "stabilityai/stable-diffusion-xl-base-1.0"



#pipe = DiffusionPipeline.from_pretrained(pipe_id, torch_dtype=torch.float16).to("cuda")
pipe = DiffusionPipeline.from_pretrained(pipe_id, torch_dtype=torch.float16).to("mps")


# adapters
pipe.load_lora_weights("CiroN2022/toy-face", weight_name="toy_face_sdxl.safetensors", adapter_name="toy")
#pipe.load_lora_weights("nerijs/pixel-art-xl", weight_name="pixel-art-xl.safetensors", adapter_name="pixel")


adapter = "Pclanglais/Mickey-1928"
weight_name = "pytorch_lora_weights.safetensors"
adapter_name="mickey"
pipe.load_lora_weights(adapter, weight_name=weight_name, adapter_name=adapter_name)


#pipe.set_adapters("pixel")
#pipe.set_adapters(["pixel", "toy"], adapter_weights=[0.5, 1.0])
pipe.set_adapters(["mickey", "toy"], adapter_weights=[0.5, 1.0])
#pipe.set_adapters("mickey")

image = pipe(

#    prompt, num_inference_steps=30, cross_attention_kwargs={"scale": lora_scale}, generator=torch.manual_seed(0)
    prompt, num_inference_steps=ni_steps, cross_attention_kwargs={"scale": lora_scale}, generator=torch.manual_seed(torch_manual_seed)

).images[0]

#image
image.save(filename)
