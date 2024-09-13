# Personalized Budgeting Assistant

Welcome to the **Personalized Budgeting Assistant**! This tool is designed to help you take control of your finances by offering personalized financial advice based on your unique financial data. Whether you're looking to save more, invest wisely, or pay off debt, this assistant will guide you in the right direction with simple, friendly advice.

## Features

- **Expense Tracking**: Visualize where your money is going with intuitive charts that break down your expenses by category.
- **Personalized Advice**: Receive friendly, easy-to-understand financial advice tailored to your current situation and goals.
- **Goal Setting**: Set and track your financial goals, such as saving for a big purchase, paying off debt, or building an emergency fund.
- **Investment Recommendations**: Get advice on how to start or optimize your investments based on your savings and financial goals.
- **Debt Management**: Learn how to prioritize and pay down high-interest debt to free up more of your income for savings and investments.

## How It Works

### 1. Input Your Financial Data
Enter details about your income, savings, expenses, goals, and priorities. You can also paste your bank statement directly into the app for automatic parsing.

### 2. Analyze Your Spending
The app categorizes your expenses and provides a visual breakdown of where your money is going each month.

### 3. Get Personalized Advice
Receive friendly, actionable financial advice based on your current financial situation. The advice includes specific calculations to help you understand the impact of your financial decisions.

### 4. Track Your Progress
Use the app to continuously monitor your spending, savings, and progress toward your financial goals. Adjust your strategy as needed with the help of ongoing advice.

## 🖥️ Installation

### Prerequisites

- **Python 3.7+**
- **Streamlit**: For running the web application.
- **FastAPI**: For running the backend API.
- **Matplotlib**: For generating visualizations.
- **Pandas**: For data handling and manipulation.
- **OpenAI API Key**: Required for generating AI-based financial advice. Register for an Open AI account and get a key and save in your env variable as described below
- **Quandl API Key**: Required for pulling financial and economic data. Register for a Quandl account and get an api key and save in your env variable as described below

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/personalized-budgeting-assistant.git
   cd personalized-budgeting-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**:
   Export your API keys as environment variables:
   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   export QUANDL_API_KEY='your-quandl-api-key'
   ```

### Running the Application

#### Start the Backend Server

1. **Navigate to the Backend Directory**:
   ```bash
   cd backEnd
   ```

2. **Run the FastAPI server**:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Start the Frontend

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontEnd
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

### Important Notes

- **Port Conflicts**: Note that both the FastAPI backend and Streamlit frontend default to using port 8000. To avoid conflicts:
  - Run FastAPI on a different port (e.g., 8001) by changing the `uvicorn` command:
    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8001 --reload
    ```
  - Update the frontend `app.py` to use the correct backend URL if you change the port.

- **Multiple Runs**: If you want to run multiple instances, ensure that the ports are not conflicting. Use the following commands to manage ports:
  - Find the process using a port:
    ```bash
    lsof -i :8000
    ```
  - Kill the process using the port:
    ```bash
    kill -9 <processID>
    ```

## Example Bank Statement

Bank Statement - August 2024

```plaintext
Date        | Description          | Amount (USD)  | Balance (USD)
08/01/2024  | Opening Balance       |               | 1200.00
08/03/2024  | Coffee Shop           | -8.50         | 1191.50
08/05/2024  | Textbook Purchase     | -75.00        | 1116.50
08/12/2024  | Grocery Store         | -45.75        | 1370.75
08/15/2024  | Rent Payment          | -2600.00       | 770.75
08/18/2024  | Phone Bill            | -30.00        | 740.75
08/20/2024  | Online Subscription   | -60.99        | 727.76
08/22/2024  | Public Transportation | -300.00        | 702.76
08/25/2024  | Income      | +8000.00       | 852.76
08/27/2024  | Fast Food             | -15.00        | 837.76
08/30/2024  | Movie Night           | -10.00        | 827.76
08/31/2024  | Closing Balance       |               | 827.76
```
