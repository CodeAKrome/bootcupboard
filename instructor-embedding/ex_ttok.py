import tiktoken

# enc = tiktoken.get_encoding("cl100k_base")
# assert enc.decode(enc.encode("hello world")) == "hello world"

# To get the tokeniser corresponding to a specific model in the OpenAI API:
text = "hello there"
enc = tiktoken.encoding_for_model("gpt-4")
dec = enc.encode(text)
print(len(dec))
