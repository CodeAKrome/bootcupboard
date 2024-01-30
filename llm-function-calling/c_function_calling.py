from local_llm_function_calling import Generator

# Define a function and models
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                    "maxLength": 20,
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

# Initialize the generator with the Hugging Face model and our functions
generator = Generator.hf(functions, "gpt2")

# Generate text using a prompt
function_call = generator.generate("What is the weather like today in Brooklyn?")
print(function_call)
