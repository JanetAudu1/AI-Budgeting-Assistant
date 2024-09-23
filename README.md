# AI-Powered Budgeting Assistant

## Overview
This AI-Powered Budgeting Assistant is a web application that provides personalized financial budgeting advice using OpenAI's GPT model. It analyzes user-provided financial data to generate tailored budgeting and savings recommendations.

## Features
- **Expense Tracking**: Visualize spending habits with intuitive charts
- **Financial Insights**: Receive personalized advice based on financial data inputted and goals set,and receive proposed budgets

## Setup and Installation


### Option 1: Using Docker (Recommended)

1. Install Docker:
   - For Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - For macOS/Linux: [Get Docker](https://docs.docker.com/get-docker/)
   - Note: avoid signing up for docker hub using your email account, preferrably,sign up using your github account or sign up manually.

2. Clone the repository:
   ```
   git clone https://github.com/JanetAudu1/AI-Budgeting-Assistant.git
   cd AI-Budgeting-Assistant
   ```

3. Build the Docker image:
   ```
   docker build -t ai-budgeting-assistant .
   ```
4a. Note: For the purpose of the workshop, we have provided you an openai key, so you can skip step 4b and step 4c

4b. Get OpenAI API key from https://platform.openai.com/docs/quickstart

4c. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   
5. Run the Docker container:
   - For Windows (PowerShell):
     ```
     docker run -d -p 8000:8000 -p 8501:8501 --env-file .\.env ai-budgeting-assistant
     ```
   - For macOS/Linux:
     ```
     docker run -d -p 8000:8000 -p 8501:8501 --env-file .env ai-budgeting-assistant
     ```

6. Access the application:
   - Streamlit UI: http://localhost:8501
   - FastAPI backend: http://localhost:8000 - already started with the docker run command, not neccessary to run.

Important Docker Notes: 

- Note for Windows users: Ensure Docker Desktop is running before executing these commands.
- If you see an error relating to docker daemon not being connected, run:
  ```
   "docker login" to ensure you are logged in to the dockerhub
    ```
- If you see an error relating to "port already in use", run:
   ```
     lsof -i :<portnumber in use> - to see the processes running on that port
     copy the PID
     run kill -9 PID - to kill process running on the port
    ```
- To stop docker instance running on machine, run:
   ```
     docker ps - to see the docker processes running on your machine
     copy ContainerID
     docker stop <ContainerID>
    ```
  
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

main.py: FastAPI server setup and configuration.

routes.py: Defines API endpoints and request handling.

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
