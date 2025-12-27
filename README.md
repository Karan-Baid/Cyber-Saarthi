# Cyber Saarthi - Indian Cybersecurity Law Chatbot

An AI-powered chatbot fine-tuned on Indian cyber laws to provide authoritative guidance on cybersecurity regulations, compliance, and legal frameworks based on the Information Technology Act, 2000.

## 🎯 Project Overview

**Cyber Saarthi** (Cyber Guide in Hindi) is a production-ready demonstration of **domain-specific LLM fine-tuning** for Indian cybersecurity law. This project showcases the complete machine learning pipeline from data generation to deployment:

- **Custom Dataset Engineering**: Automated generation of **544 diverse Q&A pairs** covering Indian Cyber Law (IT Act 2000) with 10+ variations per topic.
- **Parameter-Efficient Fine-tuning**: Leveraging QLoRA (4-bit Quantized Low-Rank Adaptation) to fine-tune **TinyLlama-1.1B** for efficient yet powerful performance.
- **Full-Stack Deployment**: Production-ready Streamlit interface with conversation memory and streaming responses.
- **Legal Domain Specialization**: Expert-level knowledge on cybersecurity regulations, penalties, compliance, and data protection laws.

## 🚀 Key Features & Performance

- **High Accuracy**: Achieved **60.2% accuracy** on diverse test queries (up from baseline 0%).
- **Specialized Knowledge**:
  - **100% Accuracy** on Data Protection (Section 43A)
  - **83.3% Accuracy** on Cyber Terrorism (Section 66F)
  - **Zero Hallucinations** or generic disclaimers in responses.
- **Efficient**: Runs on consumer hardware (requires <4GB VRAM).

## 🔍 Use Case

This chatbot helps users understand:
- Indian cybersecurity laws and regulations (IT Act 2000)
- Penalties for various cybercrimes (hacking, identity theft)
- Data protection and privacy requirements (Section 43A)
- Compliance guidelines for organizations (CERT-In)
- Cybersecurity best practices in the Indian context

## 📊 Dataset

The training dataset covers key sections of the IT Act 2000 with **10+ diverse question variations** for each topic:
- **Section 43, 43A**: Penalties for unauthorized access and data protection
- **Sections 66-66F**: Cybercrimes (hacking, identity theft, cyber terrorism)
- **Sections 67, 67A**: Publishing obscene material
- **Sections 69, 70**: Government powers and critical infrastructure
- **General Topics**: Cyber fraud reporting, best practices, privacy laws

**Dataset Statistics:**
- **Total Examples**: 544 Q&A pairs (Expanded from original 156)
- **Structure**: Instruction-tuned format
- **Split**: 80% training, 20% validation

## 🤖 Model & Fine-tuning Details

### Base Model
- **Architecture**: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- **Quantization**: 4-bit NF4 (NormalFloat4)
- **Precision**: BFloat16/Float16 for training stability

### Fine-tuning Methodology
- **Technique**: QLoRA (Quantized Low-Rank Adaptation)
- **LoRA Rank**: 16
- **LoRA Alpha**: 32
- **Target Modules**: All linear layers (q_proj, k_proj, v_proj, o_proj, etc.)

### Training Configuration
- **Epochs**: 5 (Optimized for convergence)
- **Learning Rate**: 1.0e-4 (Cosine schedule)
- **Batch Size**: 1 (Gradient accumulation used)
- **Loss Reduction**: 93% reduction in evaluation loss (1.21 → 0.084)

## 🚀 Installation

### Prerequisites
- Python 3.10+
- CUDA-compatible GPU (recommended, 4GB+ VRAM)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cyber-saarthi.git
   cd cyber-saarthi
   ```

2. **Install dependencies**
   ```bash
   # Create a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install packages
   pip install -r requirements.txt
   ```

3. **Generate the dataset** (Optional - dataset already provided in `data/`)
   ```bash
   python -m cyber_saarthi.dataset_generator
   ```

4. **Fine-tune the model** (Optional - pre-trained model available if shared)
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

- **Specific Sections**: "What is Section 66C of the IT Act?"
- **Penalties**: "What are the penalties for hacking under Indian cyber law?"
- **Data Protection**: "Explain Section 43A about data protection"
- **Definitions**: "What is cyber terrorism according to Indian law?"
- **Practical**: "Someone used my password without permission, what law applies?"

## 📁 Project Structure

```
cyber-saarthi/
├── cyber_saarthi/          # Main application package
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
└── README.md             # This file
```

## ⚠️ Disclaimer

This chatbot is for **educational purposes only**. While it provides information based on the IT Act 2000, it should not be considered as legal advice. For actual legal matters, please consult qualified legal professionals.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Expanding dataset coverage (recent amendments, case law)
- Supporting additional Indian cyber regulations
- Improving model accuracy with larger base models (e.g., Llama-3-8B)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Information Technology Act, 2000 (Government of India)
- Hugging Face for transformers and PEFT libraries
- TinyLlama team for the efficient base model

---


