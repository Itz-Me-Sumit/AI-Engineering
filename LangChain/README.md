# LangChain Tutorials

This repository contains all the source code used throughout the LangChain YouTube series.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a `.env` file.

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

### 5. Select Model

Edit `config.json` and choose the provider and model.

Happy Learning 🚀