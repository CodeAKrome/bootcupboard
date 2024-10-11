import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class Phi2Inference:
    def __init__(self, model_name="microsoft/phi-2", device="cuda" if torch.cuda.is_available() else "mps"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate(self, prompt, max_length=100, temperature=0.7, top_p=0.9):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def __call__(self, prompt, **kwargs):
        return self.generate(prompt, **kwargs)

# Example usage
if __name__ == "__main__":
    phi2 = Phi2Inference()
    prompt = "Explain the concept of machine learning in simple terms:"
    response = phi2(prompt)
    print(response)
