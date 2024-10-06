"""
Chart generation module for the AI Budgeting Assistant.

This module contains functions for creating various financial charts
using Plotly, including expense breakdown pie charts and income vs
expenses bar charts.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Chart generation functions
def generate_expense_chart(categorized_expenses):
    """
    Generates and display a pie chart showing expense breakdown by category.

    Args:
        categorized_expenses (dict): A dictionary where keys are expense categories
        and values are the total expenses for each category.
    """
    fig = px.pie(
        values=list(categorized_expenses.values()),
        names=list(categorized_expenses.keys()),
        title="Expense Breakdown by Category"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

def generate_income_vs_expenses_chart(total_income, total_expenses):
    """
    Generates and display a bar chart comparing total income to total expenses.

    Args:
        total_income (float): The user's total income.
        total_expenses (float): The user's total expenses.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Income"], y=[total_income], name="Income"))
    fig.add_trace(go.Bar(x=["Expenses"], y=[total_expenses], name="Expenses"))
    fig.update_layout(title="Income vs Expenses", barmode='group')
    st.plotly_chart(fig)

def generate_savings_projection(current_savings, monthly_savings, timeline_months):
    """
    Generates and display a line chart projecting savings growth over time.

    Args:
        current_savings (float): The user's current savings amount.
        monthly_savings (float): The estimated monthly savings amount.
        timeline_months (int): The number of months to project into the future.
    """
    months = list(range(timeline_months + 1))
    savings = [current_savings + (monthly_savings * i) for i in months]
    
    fig = px.line(
        x=months,
        y=savings,
        title="Savings Projection",
        labels={"x": "Months", "y": "Savings ($)"}
    )
    st.plotly_chart(fig)