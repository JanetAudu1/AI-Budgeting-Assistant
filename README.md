# AI-Powered Budgeting Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://budgetwise.streamlit.app/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/JanetAudu1/AI-Budgeting-Assistant/issues)
![GitHub stars](https://github.com/JanetAudu1/AI-Budgeting-Assistant/stargazers)
![GitHub forks](https://github.com/JanetAudu1/AI-Budgeting-Assistant/forks) 
[![Discord](https://img.shields.io/badge/Discord-Join%20Chat-7289DA?logo=discord&logoColor=white)](https://discord.gg/DUv6Nwns)

## Overview
This AI-Powered Budgeting Assistant is a web application that provides personalized financial advice using OpenAI's GPT model. It analyzes user-provided financial data to generate tailored budgeting and savings recommendations.

## Features
- **Expense Tracking**: Visualize spending habits with intuitive charts
- **Financial Insights**: Receive personalized advice based on financial data and proposed budgets
- **Goal Setting**: Set and track financial objectives over time

## How to Use

1. Navigate to the "Budget Analysis" section.
2. Upload your bank statement (CSV format).
  Sample Statement:
   | #  | Date       | Description    | Debit | Credit | Category  | Balance |
   |----|------------|----------------|-------|--------|-----------|---------|
   | 0  | 9/1/2024   | Paycheck       |       | 3500   | Income    | 3500    |
   | 1  | 9/5/2024   | Rent Payment   | 1000  |        | Rent      | 2500    |
   | 2  | 9/10/2024  | Groceries      | 300   |        | Groceries | 2200    |
   | 3  | 9/15/2024  | Utilities      | 200   |        | Utilities | 2000    |
   | 4  | 9/16/2024  | Coffee         | 100   |        | Personal  | 1900    |
3. Fill in your financial information and goals.
4. Click "Generate Analysis" to receive AI-powered budgetting advice.
   

## Setup and Installation


### Option 1: Using Docker (Recommended - Quick Run of the App)

1. Install Docker:
   - For Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - For macOS/Linux: [Get Docker](https://docs.docker.com/get-docker/)
   - Note: sign up to docker hub with your github account or directly.
   
2. Get OpenAI API key from https://platform.openai.com/docs/quickstart
   Note that if you are running this in the workshop, I will provide you a key, so you can skip this part.

3. Check that you are in AI-Budgeting-Assistant folder/dir. Then create a `.env` file in the project root and add your OpenAI API key. 
   ```
   echo OPENAI_API_KEY=your-api-key-here > .env
   ```
   
4. Pull the Docker image:
   ```
   docker pull janetaudu1/ai-budgeting-assistant:vGHC

   ```

5. Run the Docker container:
   - For Windows (PowerShell):
     ```
     docker run -d -p 8000:8000 -p 8501:8501 --env-file .\.env janetaudu1/ai-budgeting-assistant:vGHC

     ```
   - For macOS/Linux:
     ```
     docker run -d -p 8000:8000 -p 8501:8501 --env-file .env janetaudu1/ai-budgeting-assistant:vGHC
     ```

6. Access the application:
   - Streamlit UI: http://localhost:8501

Note for Windows users: Ensure Docker Desktop is running before executing these commands.


### Option 2: Local Installation (Recommended for Building the App)

1. Clone the repository:
   ```
   git clone https://github.com/JanetAudu1/AI-Budgeting-Assistant.git
   cd AI-Budgeting-Assistant
   ```
   
    If you dont have git, you need to fix install git on your system:
    - For Windows: download and install Git from git-scm, then verify using git --version in PowerShell.
    - For Linux:  install using your package manager (e.g., sudo apt-get install git for Ubuntu), then verify with git --version.
    - For macOS:  use Homebrew (brew install git) or download from git-scm, then verify with git --version.

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
│ ├── styles/
| ├── css/
| |  └── themes.css
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
model_handlers.py: Contains functions to process user prompts using different language models, including Hugging Face models and GPT-4.


Tests (tests/):

test_ui.py: Contains tests for the UI components.

test_api.py: Includes tests for the API endpoints.

test_recommender.py: Tests for the recommender service.

Root Directory:

requirements.txt: Lists all Python dependencies required for the project.

```
## Contribution

We welcome contributions! To get started:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix:
   ```
      git checkout -b feature-name
   ```
3. Commit your changes and push them to your fork.
4. Create a Pull Request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit) file for details.

## About

This project was developed for the Grace Hopper Conference 2024 to showcase the integration of AI-powered financial insights in budgeting tools. It is open source and available for use and contributions.
