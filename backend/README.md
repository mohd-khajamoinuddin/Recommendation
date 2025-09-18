## Project Structure

```
backend/
│
├── app.py               # Main FastAPI application
├── requirements.txt     # Python dependencies
├── config.py            # Configuration (add your API keys here)
├── data/
│   └── products.json    # Sample product catalog
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py   # Service for LLM interactions (implement this)
│   └── product_service.py  # Service for product data operations
│
└── README.md            # This file
```

## Setup Instructions

1. Create a virtual environment:
   ```
   by anaconda : conda create -n venvname python=3.10.18 -y
   or you can create a virtual environment by using : `python -m venv venvname` but here you have to use the python 3.10.18 is must another version may cause issue
   ```

2. Activate the virtual environment:
   - Anaconda : `conda activate venvname`
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with your OpenAI API key:
   ```
    GEMINI_API_KEY=your_gemini_api_key_her
    MODEL_NAME=gemini-1.5-flash-latest
    MAX_TOKENS=1000
    TEMPERATURE=0.7
    DATA_PATH=data/products.json
   ```

6. Run the application:
   ```
   uvicorn app:app --reload --port 5000
   ```
