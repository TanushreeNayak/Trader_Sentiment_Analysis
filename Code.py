import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Trader Sentiment Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("Trader Performance vs Market Sentiment Dashboard")
st.markdown("Analyze trader profitability, win rates, and trade behavior under different market sentiments.")


@st.cache_data
def load_data():
    df = pd.read_csv("merged_trader_sentiment.csv")
    return df

merged_df = load_data()


avg_profit = merged_df["Closed PnL"].mean()
win_rate = (merged_df["Closed PnL"] > 0).mean()
avg_size = merged_df["Size USD"].mean()
total_profit = merged_df["Closed PnL"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Profit", f"${avg_profit:,.2f}")
col2.metric("Win Rate", f"{win_rate*100:.2f}%")
col3.metric("Avg Trade Size", f"${avg_size:,.2f}")
col4.metric("Total Profit", f"${total_profit:,.2f}")

st.markdown("---")


avg_pnl = merged_df.groupby("classification")["Closed PnL"].mean().reset_index()

fig1 = px.bar(
    avg_pnl,
    x="classification",
    y="Closed PnL",
    title="Average Profit by Market Sentiment",
    color="classification",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)


merged_df["win"] = merged_df["Closed PnL"] > 0
win_rate_sentiment = merged_df.groupby("classification")["win"].mean().reset_index()

fig2 = px.bar(
    win_rate_sentiment,
    x="classification",
    y="win",
    title="Win Rate by Market Sentiment",
    color="classification",
    text_auto=".2%"
)

st.plotly_chart(fig2, use_container_width=True)


avg_size_sentiment = merged_df.groupby("classification")["Size USD"].mean().reset_index()

fig3 = px.bar(
    avg_size_sentiment,
    x="classification",
    y="Size USD",
    title="Average Trade Size by Market Sentiment",
    color="classification",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)


total_pnl_sentiment = merged_df.groupby("classification")["Closed PnL"].sum().reset_index()

fig4 = px.bar(
    total_pnl_sentiment,
    x="classification",
    y="Closed PnL",
    title="Total Profit by Market Sentiment",
    color="classification",
    text_auto=True
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Sentiment Summary Table")

summary = merged_df.groupby("classification").agg({
    "Closed PnL": "mean",
    "Size USD": "mean",
    "win": "mean"
}).reset_index()

summary.columns = ["Sentiment", "Avg Profit", "Avg Trade Size", "Win Rate"]

st.dataframe(summary, use_container_width=True)


st.subheader("Key Insights")

st.markdown("""
- **Extreme Greed** yields the highest **average profit** and **win rate**
- **Fear** has the highest **trade size** and **total profit**
- Traders are **most successful in bullish conditions**
- Traders take **largest risks during Fear**
- Sentiment can be used as a **risk management signal**
""")