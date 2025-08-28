from transformers import AutoModelForCausalLM, AutoTokenizer

class LargeLanguageModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=max_length, num_return_sequences=1)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def load_model(self):
        # Additional logic for loading the model can be added here if needed
        pass

# Example usage:
# llm = LargeLanguageModel("gpt2")
# response = llm.generate_text("Once upon a time")
# print(response)