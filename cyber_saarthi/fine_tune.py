import os
import yaml
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel
)
from tqdm import tqdm


def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def format_instruction(example):
    if example["input"]:
        prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

{example["instruction"]}

{example["input"]}

{example["output"]}"""
    else:
        prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

{example["instruction"]}

{example["output"]}"""
    
    return {"text": prompt}


def prepare_dataset(config):
    data_dir = config["dataset"]["data_dir"]
    train_file = os.path.join(data_dir, config["dataset"]["train_file"])
    val_file = os.path.join(data_dir, config["dataset"]["validation_file"])
    
    dataset = load_dataset('json', data_files={
        'train': train_file,
        'validation': val_file
    })
    
    dataset = dataset.map(format_instruction, remove_columns=["instruction", "input", "output"])
    
    print(f"Training examples: {len(dataset['train'])}")
    print(f"Validation examples: {len(dataset['validation'])}")
    
    return dataset


def setup_model_and_tokenizer(config):
    model_name = config["model"]["name"]
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config["model"]["load_in_4bit"],
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    
    model = prepare_model_for_kbit_training(model)
    
    lora_config = LoraConfig(
        r=config["lora"]["r"],
        lora_alpha=config["lora"]["lora_alpha"],
        target_modules=config["lora"]["target_modules"],
        lora_dropout=config["lora"]["lora_dropout"],
        bias=config["lora"]["bias"],
        task_type=config["lora"]["task_type"],
    )
    
    model = get_peft_model(model, lora_config)
    
    print(f"Model loaded: {model_name}")
    model.print_trainable_parameters()
    
    return model, tokenizer


def tokenize_function(examples, tokenizer, max_length=2048):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=max_length,
        padding=False,  # Use dynamic padding via data collator
    )


def train_model(config):
    print("Starting training...")
    
    dataset = prepare_dataset(config)
    model, tokenizer = setup_model_and_tokenizer(config)
    
    print("\nTokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer, config["model"]["max_length"]),
        batched=True,
        remove_columns=["text"]
    )
    

    training_args = TrainingArguments(
        output_dir=config["training"]["output_dir"],
        num_train_epochs=config["training"]["num_train_epochs"],
        per_device_train_batch_size=config["training"]["per_device_train_batch_size"],
        per_device_eval_batch_size=config["training"]["per_device_eval_batch_size"],
        gradient_accumulation_steps=config["training"]["gradient_accumulation_steps"],
        learning_rate=config["training"]["learning_rate"],
        weight_decay=config["training"]["weight_decay"],
        warmup_steps=config["training"]["warmup_steps"],
        logging_steps=config["training"]["logging_steps"],
        eval_steps=config["training"]["eval_steps"],
        save_steps=config["training"]["save_steps"],
        save_total_limit=config["training"]["save_total_limit"],
        fp16=config["training"]["fp16"],
        bf16=config["training"]["bf16"],
        optim=config["training"]["optim"],
        lr_scheduler_type=config["training"]["lr_scheduler_type"],
        max_grad_norm=config["training"]["max_grad_norm"],
        logging_dir=f"{config['training']['output_dir']}/logs",
        eval_strategy="steps",  # Changed from evaluation_strategy for transformers 4.57+
        save_strategy="steps",
        load_best_model_at_end=True,
        report_to="none",  # Disable wandb/tensorboard
        push_to_hub=False,
    )
    

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=data_collator,
    )
    
    print("\nTraining...")
    
    trainer.train()
    
    output_dir = f"{config['training']['output_dir']}/final"
    print(f"\nSaving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print("\nTraining complete!")
    
    return trainer


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Fine-tune Cyber Saarthi model")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--test-mode", action="store_true", help="Run a quick test with minimal training")
    args = parser.parse_args()
    

    config = load_config(args.config)
    

    if args.test_mode:
        print("Running in TEST MODE - minimal training")
        config["training"]["num_train_epochs"] = 1
        config["training"]["save_steps"] = 1000
        config["training"]["eval_steps"] = 1000
        config["dataset"]["max_samples"] = 50
    

    if not torch.cuda.is_available():
        print("WARNING: CUDA not available. Training will be very slow on CPU.")
        print("Consider using Google Colab or a machine with GPU for training.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    trainer = train_model(config)
    

    metrics = trainer.state.log_history
    if metrics:
        print("\nFinal Training Metrics:")
        for key in ['train_loss', 'eval_loss']:
            values = [m[key] for m in metrics if key in m]
            if values:
                print(f"  {key}: {values[-1]:.4f}")


if __name__ == "__main__":
    main()
