#!env python
import ollama
import sys
import fire

def main(
    query: str,
    llm="llama2",
    sysmsg="You are a helpful research assistant. You are accurate, concise and thorough. Your conclusions are supported by evidence.",
    rag="Base your reply on the following information:",
):
    modelfile = f"FROM {llm}\nSYSTEM {sysmsg}"
    text = sys.stdin.read()
    ollama.create(model="custom", modelfile=modelfile)
    content = f"{query}\n{rag}\n{text}"
    response = ollama.chat(
        model="custom",
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
    )
    print(response['message']['content'])

if __name__ == "__main__":
    fire.Fire(main)
    