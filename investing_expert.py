import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import datetime

# Investment data
investment_data = {
    'VOO': [
        {'date': '2024-08-22', 'shares': 0.2922, 'cost': 513.95},
        {'date': '2024-09-04', 'shares': 0.4625, 'cost': 505.73},
        {'date': '2024-10-02', 'shares': 0.2182, 'cost': 523.58},
        {'date': '2024-11-01', 'shares': 0.3414, 'cost': 524.97},
        {'date': '2024-12-05', 'shares': 0.521, 'cost': 558.00},
        {'date': '2025-01-02', 'shares': 0.2332, 'cost': 540.73},
    ],
    'META': [
        {'date': '2024-12-06', 'shares': 0.2347, 'cost': 627.97},
        {'date': '2025-02-10', 'shares': 0.8124, 'cost': 713.97},
        {'date': '2025-02-26', 'shares': 0.2405, 'cost': 668.56},
    ],
    'SPGI': [
        {'date': '2025-03-05', 'shares': 0.5514, 'cost': 518.19},
    ]
}

# Function to fetch current stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    current_price = stock.history(period='1d')['Close'][0]
    return current_price

# Function to calculate portfolio value and performance
def calculate_portfolio(investment_data):
    portfolio = {}
    total_cost = 0
    total_value = 0
    for ticker, data in investment_data.items():
        total_shares = sum([item['shares'] for item in data])
        total_invested = sum([item['shares'] * item['cost'] for item in data])
        current_price = get_stock_data(ticker)
        current_value = total_shares * current_price
        portfolio[ticker] = {
            'total_shares': total_shares,
            'total_invested': total_invested,
            'current_price': current_price,
            'current_value': current_value,
            'gain_loss': (current_value - total_invested) / total_invested * 100
        }
        total_cost += total_invested
        total_value += current_value
    portfolio['total_cost'] = total_cost
    portfolio['total_value'] = total_value
    portfolio['total_gain_loss'] = (total_value - total_cost) / total_cost * 100
    return portfolio

# Function to display the dashboard
def display_dashboard(portfolio):
    st.title("Investment Dashboard")

    # Line Chart for Historical Performance
    st.subheader("Historical Performance")
    historical_data = {}
    for ticker in investment_data.keys():
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        historical_data[ticker] = hist['Close']
    historical_df = pd.DataFrame(historical_data)
    st.line_chart(historical_df)

    # Pie Chart for Asset Allocation
    st.subheader("Asset Allocation")
    allocations = {ticker: data['current_value'] for ticker, data in portfolio.items() if ticker not in ['total_cost', 'total_value', 'total_gain_loss']}
    allocation_df = pd.DataFrame(list(allocations.items()), columns=['Ticker', 'Value'])
    fig = px.pie(allocation_df, names='Ticker', values='Value', title='Asset Allocation')
    st.plotly_chart(fig)

    # Bar Chart for Individual Asset Performance
    st.subheader("Individual Asset Performance")
    performance_data = {ticker: data['gain_loss'] for ticker, data in portfolio.items() if ticker not in ['total_cost', 'total_value', 'total_gain_loss']}
    performance_df = pd.DataFrame(list(performance_data.items()), columns=['Ticker', 'Gain/Loss (%)'])
    st.bar_chart(performance_df)

    # Table for Detailed Breakdown
    st.subheader("Detailed Breakdown")
    detailed_data = []
    for ticker, data in portfolio.items():
        if ticker in ['total_cost', 'total_value', 'total_gain_loss']:
            continue
        detailed_data.append({
            'Ticker': ticker,
            'Total Shares': data['total_shares'],
            'Total Invested (USD)': data['total_invested'],
            'Current Price (USD)': data['current_price'],
            'Current Value (USD)': data['current_value'],
            'Gain/Loss (%)': data['gain_loss']
        })
    detailed_df = pd.DataFrame(detailed_data)
    st.table(detailed_df)

    # Total Portfolio Value and Performance
    st.subheader("Total Portfolio Value and Performance")
    st.write(f"Total Invested: ${portfolio['total_cost']:.2f}")
    st.write(f"Total Current Value: ${portfolio['total_value']:.2f}")
    st.write(f"Total Gain/Loss: {portfolio['total_gain_loss']:.2f}%")

# Main function
def main():
    portfolio = calculate_portfolio(investment_data)
    display_dashboard(portfolio)

# Run the app
if __name__ == "__main__":
    main()