# 📝 LangChain Text Summarizer

A powerful text summarization tool built with LangChain and Streamlit that transforms long texts into concise summaries using AI.

## ✨ Features

- **Multiple Summary Types**: Choose between standard summaries and bullet-point format
- **Flexible Input**: Type/paste text directly or upload text files (.txt, .md)
- **Smart Text Processing**: Automatically handles long texts with chunking and map-reduce summarization
- **Real-time Statistics**: View character count, word count, and compression ratios
- **Download Summaries**: Save your summaries as text files
- **User-friendly Interface**: Clean, intuitive Streamlit web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- OpenRouter API account (or compatible OpenAI API)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain-text-summarizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   API_KEY=your_api_key_here
   MODEL_NAME=mistralai/mistral-small-3.1-24b-instruct:free
   BASE_URL=https://openrouter.ai/api/v1
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
langchain-text-summarizer/
├── app.py              # Main Streamlit application
├── summarizer.py       # Text summarization logic
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # Project documentation
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_KEY` | Your AI model API key | `sk-...` |
| `MODEL_NAME` | AI model identifier | `mistralai/mistral-small-3.1-24b-instruct:free` |
| `BASE_URL` | API endpoint URL | `https://openrouter.ai/api/v1` |

### Supported Models

This project is configured to work with OpenRouter's free models, but can be adapted for:
- OpenAI GPT models
- Anthropic Claude
- Other LangChain-compatible models

## 💡 Usage

1. **Choose Summary Type**: Select between "Standard Summary" or "Bullet Points"
2. **Input Text**: Either paste text directly or upload a file
3. **Generate Summary**: Click the "Generate Summary" button
4. **Review Results**: View your summary with compression statistics
5. **Download**: Save your summary as a text file


## 📄 License

This project is open source and available under the [MIT License](LICENSE).