# AI-Powered Product Recommendation Engine
*i95dev AI Engineering Intern - Take-Home Assignment*

### Overview

Welcome to the i95dev AI Engineering Intern take-home assignment! This project is designed to evaluate your skills in working with LLMs, prompt engineering, and full-stack development in an eCommerce context.

Your task is to build a simplified product recommendation system that leverages LLMs to generate personalized recommendations based on user preferences and browsing history. This system should demonstrate your ability to effectively engineer prompts, build APIs, and create a functional frontend interface.

### Project Requirements

#### Backend (Python)
- Develop a REST API using Flask that interfaces with an LLM (OpenAI GPT-3.5-turbo or similar)
- Implement prompt engineering to optimize product recommendations based on user preferences
- Create endpoints for:
  - Accepting user preference data
  - Processing browsing history
  - Returning personalized product recommendations with explanations

#### Frontend (React)
- Build a clean interface showing the product catalog
- Implement a user preference form to capture interests (e.g., preferences for categories, price ranges, styles)
- Create a browsing history simulation (users can click on products to add them to history)
- Display personalized recommendations with reasoning from the LLM

### Starter Kit

We've provided a starter kit to help you focus on the core technical challenges rather than boilerplate setup. The kit includes:

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
│   ├── llm_service.py   # Service for LLM interactions (implement this)
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
│   │   ├── Catalog.js   # Product catalog display (implement this)
│   │   ├── UserPreferences.js  # Preference form (implement this)
│   │   ├── Recommendations.js  # Recommendations display (implement this)
│   │   └── BrowsingHistory.js  # Browsing history component (implement this)
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

### Sample Dataset

We've provided a sample product catalog (`products.json`) that contains 50 products across various categories. Each product has the following structure:

```json
{
  "id": "product123",
  "name": "Ultra-Comfort Running Shoes",
  "category": "Footwear",
  "subcategory": "Running",
  "price": 89.99,
  "brand": "SportsFlex",
  "description": "Lightweight running shoes with responsive cushioning and breathable mesh upper.",
  "features": ["Responsive cushioning", "Breathable mesh", "Durable outsole"],
  "rating": 4.7,
  "inventory": 45,
  "tags": ["running", "athletic", "comfortable", "lightweight"]
}
```

The dataset includes products from categories such as:
- Electronics (smartphones, laptops, headphones, etc.)
- Clothing (shirts, pants, dresses, etc.)
- Home goods (furniture, kitchenware, decor, etc.)
- Beauty & Personal Care (skincare, makeup, fragrances, etc.)
- Sports & Outdoors (equipment, apparel, accessories, etc.)

### Key Implementation Guidelines

#### LLM Integration
- You should use OpenAI's API (GPT-3.5-turbo is sufficient) or another LLM API of your choice
- Implement proper error handling for API calls
- Use appropriate context windows and token limits

#### Prompt Engineering
- Design prompts that effectively leverage product metadata and user preferences
- Ensure your prompts provide reasoning for recommendations
- Consider how to handle context limitations for larger product catalogs

#### API Design
- Create RESTful endpoints with proper request/response formats
- Implement appropriate error handling
- Consider performance and optimization

#### React Frontend
- Focus on clean, functional UI rather than elaborate designs
- Implement responsive components that adapt to different screen sizes
- Use React state management appropriately (useState, useContext, etc.)

### Stretch Goals (Optional)

If you complete the core requirements and want to demonstrate additional skills, consider implementing one or more of these stretch goals:

1. Add user authentication and profile persistence
2. Implement caching for LLM responses to improve performance
3. Add filtering and sorting options to the product catalog
4. Create A/B testing for different prompt strategies
5. Add unit and/or integration tests

### Evaluation Criteria

Your submission will be evaluated based on:

1. **Prompt Engineering Quality (30%)**
   - Effectiveness of prompts in generating relevant recommendations
   - Context handling and optimization
   - Clarity and usefulness of recommendation explanations

2. **API Design and Implementation (25%)**
   - RESTful API design and implementation
   - Error handling and edge cases
   - Code organization and structure

3. **Frontend Implementation (25%)**
   - Component architecture and organization
   - User experience and interface design
   - State management and data flow

4. **Code Quality (20%)**
   - Code readability and documentation
   - Proper use of version control (commit messages, organization)
   - Error handling and edge cases

---

## Submission & Documentation

### How to Submit

Submit by **replying to the original assessment email** with:
- **GitHub repository link**
- **Brief overview of your approach** (1-2 paragraphs)
- **Any challenges you faced and how you overcame them**
- **Time spent on the assignment**


---

## My Approach

I built a full-stack AI-powered product recommendation engine using FastAPI (Python) for the backend and React for the frontend. The backend integrates with OpenRouter LLMs (Google Gemini, Llama) to generate personalized recommendations based on user preferences and browsing history. The frontend provides a clean, responsive UI for catalog browsing, preference selection, and viewing recommendations. The system demonstrates advanced prompt engineering, robust API design, and a professional user experience.

### Prompt Engineering & Token Management
- **Prompt Design:** Prompts include user preferences (price, categories, brands), last 5 browsed products, and a filtered catalog (up to 30 relevant products). This ensures the LLM receives enough context for high-quality, personalized recommendations.
- **Token Usage:** Each LLM request typically uses ~903 prompt tokens and ~309 completion tokens (total ~1200 tokens/request). See screenshot below for a real example.
- **Context Limitation Handling:** To avoid exceeding token limits, I implemented a filtering strategy that selects only the most relevant products for the prompt, regardless of catalog size.

---

## Challenges & Solutions
- **API Rate Limiting:** I hit OpenRouter’s free tier rate limits during testing. To ensure reliability, I built a fallback system that provides rule-based recommendations when the LLM is unavailable.
- **Malformed LLM Output:** The LLM sometimes returned invalid JSON. I solved this by making the prompt instructions more explicit and adding robust response parsing and error handling.
- **Efficient Data Flow:** Managed state and API calls in React to ensure a smooth user experience, even when the backend is slow or the LLM is unavailable.

---

## Setup Instructions

### Backend
1. Clone the repo and navigate to the backend directory:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create environment file and add your OpenRouter/OpneAi API key:
   ```bash
  
   OPENAI_API_KEY=your api key 
   MODEL_NAME=your model name
   MAX_TOKENS=1000
   TEMPERATURE=0.7
   DATA_PATH=data/products.json
   OPENAI_BASE_URL=https://api.openai.com/v1
   ```
5. Run the backend server:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 5000
   ```

### Frontend
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## How to Use
- Browse the product catalog, set your preferences, and click products to add to your browsing history.
- Click “Get Personalized Recommendations” to receive AI-powered suggestions with explanations and confidence scores.

---

## Version Control & Commit History
- The repository uses clean, descriptive commits for each major feature and fix.
- Sensitive files (e.g., `.env`) are excluded via `.gitignore`.

---

## Token Usage Example
- Example request: 903 prompt tokens, 309 completion tokens (total ~1200 tokens/request).
- (![Token Usage Screenshot](./Screenshot%202025-06-28%20225608.png)
)

---

## Contact
For questions, email recruiting@i95dev.com with "Question: AI Intern Take-Home" as the subject.

---
