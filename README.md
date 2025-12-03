# Cyber Saarthi - Indian Cybersecurity Law Chatbot

An AI-powered chatbot fine-tuned on Indian cyber laws to provide authoritative guidance on cybersecurity regulations, compliance, and legal frameworks based on the Information Technology Act, 2000.

## 🎯 Project Overview

**Cyber Saarthi** (Cyber Guide in Hindi) demonstrates the complete workflow of fine-tuning a Large Language Model (LLM) for a specialized domain. This project showcases:

- **Dataset Generation**: Creating a comprehensive Q&A dataset covering Indian cyber laws
- **Model Fine-tuning**: Using QLoRA (Quantized Low-Rank Adaptation) for efficient fine-tuning
- **Interactive Interface**: A user-friendly Streamlit chatbot for querying cybersecurity regulations
- **Legal Domain Expertise**: Specialized knowledge of IT Act 2000 and related amendments

## 🔍 Use Case

This chatbot helps users understand:
- Indian cybersecurity laws and regulations (IT Act 2000)
- Penalties for various cybercrimes
- Data protection and privacy requirements
- Compliance guidelines for organizations
- Cybersecurity best practices in the Indian context

## 📊 Dataset

The training dataset covers key sections of the IT Act 2000:
- **Section 43, 43A**: Penalties for unauthorized access and data protection
- **Sections 66-66F**: Cybercrimes (hacking, identity theft, cyber terrorism)
- **Sections 67, 67A**: Publishing obscene material
- **Sections 69, 70**: Government powers and critical infrastructure
- **Sections 72, 75**: Privacy breaches and jurisdiction

Dataset Statistics:
- **Total Examples**: 400-500 Q&A pairs
- **Format**: JSONL (instruction-based)
- **Split**: 80% training, 20% validation

## 🤖 Model Information

- **Base Model**: Llama 3.2 (3B) or Mistral-7B
- **Fine-tuning Method**: QLoRA (4-bit quantization)
- **Framework**: Hugging Face Transformers + PEFT
- **Training**: Supervised fine-tuning on domain-specific Q&A pairs

## 🚀 Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended, 8GB+ VRAM)
- 10GB+ disk space for models

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cyber-saarthi.git
   cd cyber-saarthi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the dataset**
   ```bash
   python -m cyber_saarthi.dataset_generator
   ```

4. **Fine-tune the model** (optional - can use pre-trained weights)
   ```bash
   python -m cyber_saarthi.fine_tune
   ```

## 💬 Usage

### Running the Chatbot

```bash
streamlit run cyber_saarthi/chatbot_app.py
```

Open your browser and navigate to `http://localhost:8501`

### Example Queries

- "What is Section 66 of the IT Act?"
- "What are the penalties for hacking under Indian cyber law?"
- "Explain data protection requirements under IT Act 2000"
- "What is cyber terrorism according to Indian law?"
- "What are the punishments for identity theft in India?"

### Using the Model Programmatically

```python
from cyber_saarthi.inference import CyberSaarthiModel

# Load the model
model = CyberSaarthiModel("models/cyber-saarthi-final")

# Generate response
response = model.generate(
    "What are the penalties for unauthorized access to computer systems?"
)
print(response)
```

## 📁 Project Structure

```
cyber-saarthi/
├── cyber_saarthi/          # Main application package
│   ├── __init__.py
│   ├── dataset_generator.py   # Dataset creation script
│   ├── fine_tune.py           # Model training script
│   ├── inference.py           # Model inference utilities
│   └── chatbot_app.py         # Streamlit chatbot interface
├── data/                   # Dataset files
│   ├── cyber_laws_qa.jsonl
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── dataset_stats.json
├── models/                 # Trained models (gitignored)
├── config.yaml            # Training configuration
├── requirements.txt       # Python dependencies
├── DATASET.md            # Dataset documentation
├── TRAINING.md           # Training methodology
└── README.md             # This file
```

## 🎓 Learning Outcomes

This project demonstrates:
1. **Data Engineering**: Creating domain-specific datasets for LLM training
2. **Model Fine-tuning**: Using modern techniques (QLoRA) for efficient training
3. **Prompt Engineering**: Structuring instructions for optimal model responses
4. **Deployment**: Building interactive interfaces for ML models
5. **Domain Specialization**: Adapting general models to specific use cases

## 🔧 Configuration

Edit `config.yaml` to customize:
- Model selection and parameters
- Training hyperparameters (learning rate, batch size, epochs)
- LoRA configuration (rank, alpha, dropout)
- Dataset paths and splits

## 📚 Documentation

- **[DATASET.md](DATASET.md)**: Detailed dataset documentation
- **[TRAINING.md](TRAINING.md)**: Fine-tuning methodology and results

## ⚠️ Disclaimer

This chatbot is for **educational purposes only**. While it provides information based on the IT Act 2000, it should not be considered as legal advice. For actual legal matters, please consult qualified legal professionals.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Expanding dataset coverage (recent amendments, case law)
- Supporting additional Indian cyber regulations
- Improving model accuracy
- Adding multilingual support

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Information Technology Act, 2000 (Government of India)
- Hugging Face for transformers and PEFT libraries
- Open-source LLM community

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for cybersecurity education and awareness**
