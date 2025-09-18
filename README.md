# i95dev AI Engineering Intern - Take-Home Assignment
## AI-Powered Product Recommendation Engine

### Overview

This project is designed to evaluate skills in working with LLMs, prompt engineering, and full-stack development in an eCommerce context.

In is we build a simplified product recommendation system that leverages LLMs to generate personalized recommendations based on user preferences and browsing history. 

#### Backend Structure

```
backend/
│
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── config.py            # Configuration (add your API keys here)
├── data/
│   └── products.json    # Sample product catalog
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py   # Service for LLM interactions 
│   └── product_service.py  # Service for product data operations
│
└── README.md            # Backend setup instructions
```

#### Frontend Structure
```
frontend/
│
├── public/
│   └── index.html
│
├── src/
│   ├── App.js           # Main application component
│   ├── index.js         # Entry point
│   ├── components/
│   │   ├── Catalog.js   # Product catalog display
│   │   ├── UserPreferences.js  # Preference form
│   │   ├── Recommendations.js  # Recommendations display
│   │   └── BrowsingHistory.js  # Browsing history component
│   │
│   ├── services/
│   │   └── api.js       # API client for backend communication
│   │
│   └── styles/
│       └── App.css      # Styling
│
├── package.json         # NPM dependencies
└── README.md            # Frontend setup instructions
```
### Key Implementation 

#### LLM Integration
- In This we use the Gemini flash 1.5 Api
- Implement proper error handling for API calls
- Use appropriate context windows and token limits

### Overview of Prompt Engineering Documentation for Gemini 

#### Overview
- Model used: Gemini 1.5 Flash
- Capabilities: multimodal inputs (text, images, audio, video, PDF), large context windows, function calling, structured output, etc.
- Limitations / deprecated status: Gemini 1.5 Flash is noted as a “legacy model” in some contexts; there may be restrictions or eventual migration needed.
#### Gemini 1.5 Flash Specifics
- Token limits & context: Input size up to ~1,048,576 tokens. Output default max ~8,192 tokens.
- Supported input types: text, code, images, audio, video, PDF. 
- Parameter defaults / settings: temperature range, topP, topK etc.
#### How Prompting Works in Project
- From Backend data is send to frontend using api
- In Backend prompt are written to get the data
- we set tokens = 1000 and temperature = 0.7

### Setup Instructions

#### Backend Setup
1. Navigate to the `backend` directory
2. Create a virtual environment: conda create -n venvname python=3.10.18 -y
   or you can create a virtual environment by using : `python -m venv venvname` but here you have to use the python 3.10.18 is must another version may cause issue
3. Activate the virtual environment:
   - through Anaconda : `conda activate venvname`
   - Windows: `venvname\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. 5. Create a `.env` file based on `.env.example` and add your LLM API key
6. Run the application: `uvicorn app:app --reload --port 5000`

#### Frontend Setup
1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Start the development server: `npm start`
4. The application should open at `http://localhost:3000`

### Resources

- [Gemini Flash] (https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/1-5-flash)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
