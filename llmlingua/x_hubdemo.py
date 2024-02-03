from llmlingua import PromptCompressor
import torch

TEST_PROMPT = """Question: Sam bought a dozen boxes, each with 30 highlighter pens inside, for $10 each box. He reanged five of boxes into packages of sixlters each and sold them $3 per. He sold the rest theters separately at the of three pens $2. How much did make in total, dollars?\nLets think step step\nSam bought 1 boxes x00 oflters.\nHe bought 12 * 300ters in total\nSam then took 5 boxes 6ters0ters.\nHe sold these boxes for 5 *5\nAfterelling these  boxes there were 3030 highlighters remaining.\nThese form 330 / 3 = 110 groups of three pens.\nHe sold each of these groups for $2 each, so made 110 * 2 = $220 from them.\nIn total, then, he earned $220 + $15 = $235.\nSince his original cost was $120, he earned $235 - $120 = $115 in profit.\nThe answer is 115"""
TEST_PROMPT = """Amateur radio came into being after radio waves (proved to exist by Heinrich Rudolf Hertz in 1888) were adapted into a communication system in the 1890s by the Italian inventor Guglielmo Marconi. In the late 19th century there had been amateur wired telegraphers setting up their own interconnected telegraphic systems. Following Marconi's success many people began experimenting with this new form of "wireless telegraphy". Information on "Hertzian wave" based wireless telegraphy systems (the name "radio" would not come into common use until several years later) was sketchy, with magazines such as the November, 1901 issue of Amateur Work showing how to build a simple system based on Hertz' early experiments. Magazines show a continued progress by amateurs including a 1904 story on two Boston, Massachusetts 8th graders constructing a transmitter and receiver with a range of eight miles and a 1906 story about two Rhode Island teenagers building a wireless station in a chicken coop. In the US the first commercially produced wireless telegraphy transmitter / receiver systems became available to experimenters and amateurs in 1905. In 1908, students at Columbia University formed the Wireless Telegraph Club of Columbia University, now the Columbia University Amateur Radio Club. This is the earliest recorded formation of an amateur radio club, collegiate or otherwise. In 1910, the Amateurs of Australia formed, now the Wireless Institute of Australia."""

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

print(f"Device: {device}")

#llm_lingua = PromptCompressor()

# /Users/kyle/hub/bootcupboard/llmlingua/.venv/lib/python3.11/site-packages/transformers/generation/configuration_utils.py:392: UserWarning: `do_sample` is set to `False`. However, `temperature` is set to `0.9` -- this flag is only used in sample-based generation modes. You should set `do_sample=True` or unset `temperature`. This was detected when initializing the generation config instance, which means the corresponding file may hold incorrect parameterization and should be fixed.
#   warnings.warn(
# /Users/kyle/hub/bootcupboard/llmlingua/.venv/lib/python3.11/site-packages/transformers/generation/configuration_utils.py:397: UserWarning: `do_sample` is set to `False`. However, `top_p` is set to `0.6` -- this flag is only used in sample-based generation modes. You should set `do_sample=True` or unset `top_p`. This was detected when initializing the generation config instance, which means the corresponding file may hold incorrect parameterization and should be fixed.
# Attempt to fix:
# 'do_sample':True



llm_lingua = PromptCompressor(
    model_name="NousResearch/Llama-2-7b-hf",  # Default model
    device_map=device,  # Device environment (e.g., 'cuda', 'cpu', 'mps')
    model_config={'do_sample':True},  # Configuration for the Huggingface model
    open_api_config={},  # Configuration for OpenAI Embedding in coarse-level prompt compression.
)

compressed_prompt = llm_lingua.compress_prompt(
    TEST_PROMPT, instruction="", question="", target_token=100, 
)

# > {'compressed_prompt': 'Question: Sam bought a dozen boxes, each with 30 highlighter pens inside, for $10 each box. He reanged five of boxes into packages of sixlters each and sold them $3 per. He sold the rest theters separately at the of three pens $2. How much did make in total, dollars?\nLets think step step\nSam bought 1 boxes x00 oflters.\nHe bought 12 * 300ters in total\nSam then took 5 boxes 6ters0ters.\nHe sold these boxes for 5 *5\nAfterelling these  boxes there were 3030 highlighters remaining.\nThese form 330 / 3 = 110 groups of three pens.\nHe sold each of these groups for $2 each, so made 110 * 2 = $220 from them.\nIn total, then, he earned $220 + $15 = $235.\nSince his original cost was $120, he earned $235 - $120 = $115 in profit.\nThe answer is 115',
#  'origin_tokens': 2365,
#  'compressed_tokens': 211,
#  'ratio': '11.2x',
#  'saving': ', Saving $0.1 in GPT-4.'}

## Or use the phi-2 model,
## Before that, you need to update the transformers to the github version, like pip install -U git+https://github.com/huggingface/transformers.git

#llm_lingua = PromptCompressor("microsoft/phi-2")

## Or use the quantation model, like TheBloke/Llama-2-7b-Chat-GPTQ, only need <8GB GPU memory.
## Before that, you need to pip install optimum auto-gptq

# llm_lingua = PromptCompressor(
#     "TheBloke/Llama-2-7b-Chat-GPTQ", model_config={"revision": "main"}
# )

print(compressed_prompt)