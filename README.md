# AI-Budgeting-Assistant

A budget analyzer using AI to make budgeting reocmmendations

How to start the app: 
Open two terminal tabs 
cd to frontEnd in one tab 
cd to backEnd in one tab 

in the backEnd tab run "uvicorn api:app --reload" 
in the frontEnd tab run "streamlit run app.py" 

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


