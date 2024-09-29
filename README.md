# AI-Powered Budgeting Assistant

## Overview
This AI-Powered Budgeting Assistant is a web application that provides personalized financial advice using OpenAI's GPT model. It analyzes user-provided financial data to generate tailored budgeting and savings recommendations.

## Features
- **Expense Tracking**: Visualize spending habits with intuitive charts
- **Financial Insights**: Receive personalized advice based on financial data and proposed budgets
- **Goal Setting**: Set and track financial objectives over time


## Setup and Installation


### Option 1: Using Docker (Recommended)

1. Install Docker:
   - For Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - For macOS/Linux: [Get Docker](https://docs.docker.com/get-docker/)
   - Note: sign up to docker hub with your github account or directly.
   
2. Clone the repository:
   ```
   git clone https://github.com/JanetAudu1/AI-Budgeting-Assistant.git
   cd AI-Budgeting-Assistant
   ```

3. Build the Docker image:
   ```
   docker build -t ai-budgeting-assistant .
   ```

4. Get OpenAI API key from https://platform.openai.com/docs/quickstart

5. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

6. Run the Docker container:
   - For Windows (PowerShell):
     ```
     docker run -d -p 8000:8000 -p 8501:8501 --env-file .\.env ai-budgeting-assistant
     ```
   - For macOS/Linux:
     ```
     docker run -d -p 8000:8000 -p 8501:8501 --env-file .env ai-budgeting-assistant
     ```

7. Access the application:
   - FastAPI backend: http://localhost:8000
   - Streamlit UI: http://localhost:8501

Note for Windows users: Ensure Docker Desktop is running before executing these commands.

Note: 
if you get an error with the 


### Option 2: Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/JanetAudu1/AI-Budgeting-Assistant.git
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

3b. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   Replace 'your-api-key-here' with your actual OpenAI API key.

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
│ ├── init.py
│ ├── ui/
│ │ ├── init.py
│ │ ├── app.py
│ │ ├── layout.py
│ │ ├── input_handlers.py
│ │ ├── charts.py
│ │ └── advice.py
│ ├── api/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── routes.py
│ │ └── models.py
│ ├── core/
│ │ ├── init.py
│ │ └── config.py
│ └── services/
│ ├── init.py
│ ├── recommender.py
│ └── model_handlers.py
├── tests/
│ ├── init.py
│ ├── test_ui.py
│ ├── test_api.py
│ └── test_recommender.py
├── requirements.txt
└── README.md
```

```
File Descriptions: 

Frontend (app/ui/):

app.py: Main Streamlit application orchestrating UI components and user interactions.

layout.py: Renders different sections/pages like Home and Financial Analysis.

input_handlers.py: Manages user data input, including bank statement uploads and financial details.

advice.py: Handles the generation and display of AI-powered financial advice.

charts.py: Creates and displays visual charts for financial data visualization.


Backend (app/api/ and app/core/):

Backend (app/api/ and app/core/):

main.py: FastAPI server setup and configuration.

routes.py: Defines API endpoints and request handling.

models.py: Defines the UserDataInput model for data validation and structure.

config.py: Stores application-wide configurations.

data_validation.py: Defines data models to ensure incoming data is valid and well-structured.


Services (app/services/):

recommender.py: Core logic for interfacing with OpenAI's GPT-4 to produce personalized advice.


Tests (tests/):

test_ui.py: Contains tests for the UI components.

test_api.py: Includes tests for the API endpoints.

test_recommender.py: Tests for the recommender service.


Root Directory:

requirements.txt: Lists all Python dependencies required for the project.

README.md: Provides an overview, setup instructions, and documentation for the project.

```
