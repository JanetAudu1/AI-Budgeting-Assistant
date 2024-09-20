# AI-Powered Budgeting Assistant

## Overview
This AI-Powered Budgeting Assistant is a web application that provides personalized financial advice using OpenAI's GPT model. It analyzes user-provided financial data to generate tailored budgeting and savings recommendations.

## Features
- **Expense Tracking**: Visualize spending habits with intuitive charts
- **Financial Insights**: Receive personalized advice based on financial data and proposed budgets
- **Goal Setting**: Set and track financial objectives over time


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
   
3a. Get OpenAI API key 
```
https://platform.openai.com/docs/quickstart
```

3b. Set up your OpenAI API key as an environment variable:
```
 export OPENAI_API_KEY='your-api-key-here'
```

## Running the Application
Open two different tabs on your terminal and in each one, run the following commands
1. Start the backend server:
   ```
   uvicorn app.api.main:app --reload
   ```

2. In a new terminal, run the Streamlit app:
   ```
   streamlit run app/ui/app.py
   ```

3. Open your web browser and go to http://localhost:8501

## How to Use

1. Navigate to the "Budget Analysis" section.
2. Upload your bank statement (CSV format).
3. Fill in your financial information and goals.
4. Click "Generate Analysis" to receive AI-powered budgetting advice.


## Technology Stack
- Frontend: Streamlit
- Backend: FastAPI
- Data Processing: Pandas   
- AI Model: OpenAI GPT-4
- Language: Python 3.9+


## Project Structure

```
AI-Budgeting-Assistant/
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── layout.py
│   │   ├── input_handlers.py
│   │   ├── charts.py
│   │   └── advice.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── data_validation.py
│   └── services/
│       ├── __init__.py
│       └── recommender.py
├── tests/
│   ├── __init__.py
│   ├── test_ui.py
│   ├── test_api.py
│   └── test_recommender.py
├── requirements.txt
├── README.md
└── .gitignore
```

```
File Descriptions: 

Frontend (frontEnd/):

app.py: Main Streamlit application orchestrating UI components and user interactions.

layout.py: Renders different sections/pages like Home and Financial Analysis.

input_handlers.py: Manages user data input, including bank statement uploads and financial details.

advice.py: Handles the generation and display of AI-powered financial advice.

charts.py: Creates and displays visual charts for financial data visualization.


Backend (backEnd/):


api.py: FastAPI server connecting the frontend to the backend 

recommender.py: Core logic used in interfacing with OpenAI's GPT-4 to produce personalized advice.

data_validation.py: Defines data models to ensure incoming data is valid and well-structured.

init_.py: Marks the directory as a Python package, enabling proper module imports.


Root Directory:

requirements.txt: Lists all Python dependencies required for the project.

README.md: Provides an overview, setup instructions, and documentation for the project.

```
