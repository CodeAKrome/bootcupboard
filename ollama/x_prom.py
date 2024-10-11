import ollama
import fire
from typing import List, Optional

class OllamaLLM():
    def __init__(self, models: Optional[list] = None, system_message: Optional[str] = None) -> None:
        self.models = {}
        if models is not None:
            for model in models:
                self.create_model(model['name'], model['file'])
            
            
#        modelfile = """
#FROM llava:34b
#SYSTEM You are a pirate. You will answer with answer with pirate slang.
#        """
    def create_model(self, model_name: str, modelfile: str) -> None:
        """
        Create a custom Ollama model from a model file.

        Args:
        model_name (str): The name of the model.
        modelfile (str): The model file contents.
        Returns:
        None
        """
        ollama.create(model=model_name, modelfile=modelfile)
        self.models[model_name] = modelfile

    def list_models(self) -> List[str]:
        """
        List the currently available Ollama models.

        Returns:
        list: A list of available model names.
        """
        return list(self.models.keys()) + ollama.list_models()

    def answer_prompt(self, model_name: str, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Use the Ollama LLM to answer a prompt.

        Args:
        model_name (str): The name of the model to use.
        prompt (str): The prompt to answer.
        system_message (str, optional): The system message to use. Defaults to None.

        Returns:
        str: The answer to the prompt.
        """
        if system_message:
            return ollama.call(query=prompt, model=model_name, system_message=system_message)
        else:
            return ollama.call(query=prompt, model=model_name)


def main() -> None:
    ollama_llm = OllamaLLM()
    fire.Fire(ollama_llm)


if __name__ == "__main__":
    main()
