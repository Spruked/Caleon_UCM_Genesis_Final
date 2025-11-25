from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Phi3Articulator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini-4k-instruct")
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/phi-3-mini-4k-instruct",
            torch_dtype=torch.float32,  # Use float32 for CPU compatibility
            device_map="cpu"  # Force CPU usage
        )

    def articulate(self, text, persona_prompt):
        inputs = self.tokenizer(persona_prompt + text, return_tensors="pt").to("cpu")  # Force CPU
        output = self.model.generate(**inputs, max_new_tokens=300)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

Articulator = Phi3Articulator()