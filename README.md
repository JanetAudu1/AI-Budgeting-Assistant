# 💰 Personalized Budgeting Assistant

Welcome to the **Personalized Budgeting Assistant**! This tool is designed to help you take control of your finances by offering personalized financial advice based on your unique financial data. Whether you're looking to save more, invest wisely, or pay off debt, this assistant will guide you in the right direction with simple, friendly advice.

## 🚀 Features

- **Expense Tracking**: Visualize where your money is going with intuitive charts that break down your expenses by category.
- **Personalized Advice**: Receive friendly, easy-to-understand financial advice tailored to your current situation and goals.
- **Goal Setting**: Set and track your financial goals, such as saving for a big purchase, paying off debt, or building an emergency fund.
- **Investment Recommendations**: Get advice on how to start or optimize your investments based on your savings and financial goals.
- **Debt Management**: Learn how to prioritize and pay down high-interest debt to free up more of your income for savings and investments.

## 🛠️ How It Works

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
- **Matplotlib**: For generating visualizations.
- **Pandas**: For data handling and manipulation.
- **OpenAI API Key**: Required for generating AI-based financial advice.

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

3. **Set Up OpenAI API Key**:
   Export your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-openai-api-key'
   ```

4. **Run the Application**:
   Start the Streamlit app by executing:
   ```bash
   streamlit run frontEnd/app.py
   ```
 

Note that for fastapi, we have hardcoded port 8000, which is also the port form which streamlit is being ran. So if you want to try multiple runs of the app, ensure to check for the process id and kill the process being ran on port 8000 before retrying.
To find the process id:  run lsof -i :8000
To kill the process: run kill -9 <processID>



Bank Statement - August 2024
Date	Description	Amount (USD)	Balance (USD)
08/01/2024	Opening Balance		1200.00
08/03/2024	Coffee Shop	-8.50	1191.50
08/05/2024	Textbook Purchase	-75.00	1116.50
08/08/2024	Part-Time Job Income	+300.00	1416.50
08/12/2024	Grocery Store	-45.75	1370.75
08/15/2024	Rent Payment	-600.00	770.75
08/18/2024	Phone Bill	-30.00	740.75
08/20/2024	Online Subscription	-12.99	727.76
08/22/2024	Public Transportation	-25.00	702.76
08/25/2024	Freelance Income	+150.00	852.76
08/27/2024	Fast Food	-15.00	837.76
08/30/2024	Movie Night	-10.00	827.76
08/31/2024	Closing Balance		827.76



