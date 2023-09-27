#!env python
from litellm import completion
import sys
import time

task = None

if len(sys.argv) > 1:
    model = "huggingface/" + sys.argv[1]
    text = sys.argv[2]
else:
    model = "huggingface/PygmalionAI/metharme-1.3b"
    text = "Hello, how are you?"

messages = [{ "content": text,"role": "user"}]

def retry(func, iterations=13, naptime=3):
    """Retries a function until it succeeds or the number of iterations is reached.
    
    Args:
      func: The function to retry.
      iterations: The number of times to retry the function.

    Returns:
      The result of the function, or None if the function failed to succeed after
      the specified number of iterations.
    """
    for i in range(iterations):
        try:
            return func()
        except Exception as e:
            print(f"Exception: {e}")
            time.sleep(naptime)
    return None

def closure_completion(model, messages, task):
    """Creates a closure for the function `completion()` to a function with no parameters.

    Args:
      model: The model to use for completion.
      messages: array of dicts [{ "content": text,"role": "user"}] 
      task: should be set to None, for some cryptic reason
    Returns:
      A function that takes no parameters and returns the result of calling the
      `completion()` function with the given model a list of messages and a task, which should be None.
    """
    def completion_closure():
        return (completion(model=model, messages=messages, task=task))
    return completion_closure

print(f"model: {model}\n{retry(closure_completion(model, messages, task))}")

