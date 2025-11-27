from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Phi3Articulator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-3-mini-4k-instruct", trust_remote_code=True)
        self.model = None  # Lazy load

    def _load_model(self):
        if self.model is None:
            print("Loading Phi-3 model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                "microsoft/phi-3-mini-4k-instruct",
                torch_dtype=torch.float16,  # Use float16 to reduce memory usage
                trust_remote_code=True,
                attn_implementation='eager'  # Use eager attention for CPU
            )
            print("Model loaded successfully")

    def articulate(self, text, persona_prompt):
        self._load_model()
        inputs = self.tokenizer(persona_prompt + text, return_tensors="pt").to("cpu")  # Force CPU
        output = self.model.generate(**inputs, max_new_tokens=300)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

Articulator = Phi3Articulator()