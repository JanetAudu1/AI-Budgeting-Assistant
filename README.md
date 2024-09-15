# AI-Powered Budgeting Assistant

## Overview
This AI-Powered Budgeting Assistant is a web application that provides personalized financial advice using OpenAI's GPT model. It analyzes user-provided financial data to generate tailored budgeting and savings recommendations.

## Features
- User-friendly interface for inputting financial data
- Bank statement analysis and expense categorization
- Visual representation of expenses and income
- AI-generated personalized financial advice

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/AI-Budgeting-Assistant.git
   cd AI-Budgeting-Assistant
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Running the Application

1. Start the backend server:
   ```
   uvicorn backEnd.api:app --reload
   ```

2. In a new terminal, run the Streamlit app:
   ```
   streamlit run frontEnd/app.py
   ```

3. Open your web browser and go to http://localhost:8501

## How to Use

1. Navigate to the "Financial Analysis" section.
2. Upload your bank statement (CSV format).
3. Fill in your financial information and goals.
4. Click "Generate Analysis" to receive AI-powered financial advice.

## Project Structure

AI-Budgeting-Assistant/
├── frontEnd/
│ ├── app.py
│ ├── layout.py
│ ├── input_handlers.py
│ ├── advice.py
│ └── charts.py
├── backEnd/
│ ├── api.py
│ ├── data_validation.py
│ └── recommender.py
├── requirements.txt
└── README.md

## Technology Stack
- Frontend: Streamlit
- Backend: FastAPI
- Data Processing: Pandas
- AI Model: OpenAI GPT-4
- Language: Python 3.9+
