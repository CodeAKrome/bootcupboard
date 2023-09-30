#!env python3

from transformers import pipeline

pipe = pipeline("text-generation", model="TheBloke/orca_mini_v2_7B-GGML")
