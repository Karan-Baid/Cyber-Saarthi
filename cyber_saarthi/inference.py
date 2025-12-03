import os
import yaml
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline
)
from peft import PeftModel, PeftConfig


class CyberSaarthiModel:
    
    def __init__(self, model_path, load_in_4bit=True):
        self.model_path = model_path
        self.load_in_4bit = load_in_4bit
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading Cyber Saarthi model from {model_path}...")
        self._load_model()
        print(f"✓ Model loaded successfully on {self.device}")
    
    def _load_model(self):

        if os.path.exists(os.path.join(self.model_path, "adapter_config.json")):
            peft_config = PeftConfig.from_pretrained(self.model_path)
            
            if self.load_in_4bit and self.device == "cuda":
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_use_double_quant=True,
                )
                
                base_model = AutoModelForCausalLM.from_pretrained(
                    peft_config.base_model_name_or_path,
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                )
            else:
                base_model = AutoModelForCausalLM.from_pretrained(
                    peft_config.base_model_name_or_path,
                    device_map="auto",
                    trust_remote_code=True,
                )
            
            self.model = PeftModel.from_pretrained(base_model, self.model_path)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        else:
            if self.load_in_4bit and self.device == "cuda":
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_use_double_quant=True,
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    device_map="auto",
                    trust_remote_code=True,
                )
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.eval()
    
    def format_prompt(self, instruction, input_text=""):
        if input_text:
            prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

{instruction}

{input_text}

"""
        else:
            prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

{instruction}

"""
        return prompt
    
    def generate(
        self,
        instruction,
        input_text="",
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.1,
        do_sample=True,
    ):

        prompt = self.format_prompt(instruction, input_text)
        

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        

        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        

        if "### Response:" in full_response:
            response = full_response.split("### Response:")[-1].strip()
        else:
            response = full_response
        
        return response
    
    def chat(self, instruction, **kwargs):
        return self.generate(instruction, **kwargs)


def load_config(config_path="config.yaml"):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def test_inference(model_path):

    model = CyberSaarthiModel(model_path)
    

    test_queries = [
        "What is Section 66C of the IT Act?",
        "What are the penalties for hacking in India?",
        "How do I report a cybercrime?",
        "What is identity theft under Indian cyber law?",
        "Explain Section 43A about data protection",
    ]
    
    print("\n" + "=" * 70)
    print("Testing Cyber Saarthi Model")
    print("=" * 70)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 70)
        response = model.generate(query, max_new_tokens=300, temperature=0.7)
        print(f"🤖 Response: {response}")
        print("=" * 70)


def interactive_mode(model_path):
    model = CyberSaarthiModel(model_path)
    

    config = load_config()
    gen_config = config.get("generation", {})
    
    print("\n" + "=" * 70)
    print("Cyber Saarthi - Interactive Mode")
    print("=" * 70)
    print("Ask me anything about Indian cyber laws!")
    print("Type 'exit' or 'quit' to end the conversation")
    print("=" * 70 + "\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using Cyber Saarthi! Stay safe online! 🛡️")
                break
            
            if not query:
                continue
            
            print("\nCyber Saarthi: ", end="", flush=True)
            response = model.generate(
                query,
                max_new_tokens=gen_config.get("max_new_tokens", 512),
                temperature=gen_config.get("temperature", 0.7),
                top_p=gen_config.get("top_p", 0.9),
                top_k=gen_config.get("top_k", 50),
                repetition_penalty=gen_config.get("repetition_penalty", 1.1),
                do_sample=gen_config.get("do_sample", True),
            )
            print(response + "\n")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using Cyber Saarthi! Stay safe online! 🛡️")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Cyber Saarthi Inference")
    parser.add_argument("--model-path", default="./models/cyber-saarthi/final", 
                        help="Path to the fine-tuned model")
    parser.add_argument("--test", action="store_true", help="Run test queries")
    parser.add_argument("--interactive", action="store_true", help="Interactive chat mode")
    args = parser.parse_args()
    
    if not os.path.exists(args.model_path):
        print(f"Error: Model not found at {args.model_path}")
        print("Please train the model first using: python -m cyber_saarthi.fine_tune")
        return
    
    if args.test:
        test_inference(args.model_path)
    elif args.interactive:
        interactive_mode(args.model_path)
    else:
        print("Please specify --test or --interactive mode")
        print("Example: python -m cyber_saarthi.inference --interactive")


if __name__ == "__main__":
    main()
