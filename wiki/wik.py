import wikipedia as wiki
#from icecream import ic
import sys
import ollama

MODEL = "llama3.1"

res = wiki.search("Trump")
dex = {}

for rec in res:
    print(rec)
    try:
        dex[rec] = wiki.summary(rec)
    except Exception as e:
        sys.stderr.write(f"Error: {e}")
        
#ic(dex)

    
