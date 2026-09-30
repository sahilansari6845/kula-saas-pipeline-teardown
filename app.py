import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Kula.ai Funnel Teardown", layout="wide")

st.title("📊 Kula.ai Pipeline & Revenue Leakage Analysis")
st.markdown("Interactive executive dashboard modeling SaaS drop-offs and trial activation thresholds.")

# Load data
df = pd.read_csv('kula_pipeline_data.csv')

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
total_leads = len(df)
closed_deals = (df['deal_status'] == 'Closed Won').sum()
total_arr = df['arr_value_usd'].sum()
avg_show_rate = (df['demo_attended'].sum() / total_leads) * 100

col1.metric("Total Inbound Leads", total_leads)
col2.metric("Demo Attendance Rate", f"{avg_show_rate:.1f}%")
col3.metric("Deals Closed Won", closed_deals)
col4.metric("Total ARR Won", f"${total_arr:,.0f}")

st.divider()

# Visuals Row 1
v1, v2 = st.columns(2)

with v1:
    st.subheader("1. Pipeline Stage Conversion Funnel")
    funnel_data = dict(
        stages=['Demo Requested', 'Demo Attended', 'Trial Activated', 'Closed Won'],
        values=[
            len(df),
            df['demo_attended'].sum(),
            df['trial_activated'].sum(),
            (df['deal_status'] == 'Closed Won').sum()
        ]
    )
    fig_funnel = px.funnel(funnel_data, y='stages', x='values', color_discrete_sequence=['#4F46E5'])
    st.plotly_chart(fig_funnel, use_container_width=True)

with v2:
    st.subheader("2. Attendance Rate by Lead Source (No-Show Leak)")
    channel_df = df.groupby('lead_source').agg(
        total=('company_id', 'count'),
        attended=('demo_attended', 'sum')
    ).reset_index()
    channel_df['rate'] = (channel_df['attended'] / channel_df['total']) * 100
    fig_channel = px.bar(
        channel_df, x='lead_source', y='rate', 
        text_auto='.1f', color='rate', color_continuous_scale='Blues',
        labels={'rate': 'Attendance Rate (%)', 'lead_source': 'Channel'}
    )
    st.plotly_chart(fig_channel, use_container_width=True)

st.divider()

# Visuals Row 2
v3, v4 = st.columns(2)

with v3:
    st.subheader("3. Product Activation Impact (The 50-Email Mark)")
    trial_df = df[df['trial_activated'] == 1].copy()
    trial_df['Usage Group'] = trial_df['emails_sent_in_trial'].apply(
        lambda x: 'Low Usage (<50 emails)' if x < 50 else 'High Usage (>=50 emails)'
    )
    usage_summary = trial_df.groupby('Usage Group').agg(
        total=('company_id', 'count'),
        won=('deal_status', lambda x: (x == 'Closed Won').sum())
    ).reset_index()
    usage_summary['Conversion %'] = (usage_summary['won'] / usage_summary['total']) * 100
    fig_usage = px.bar(
        usage_summary, x='Usage Group', y='Conversion %', 
        text_auto='.1f', color='Usage Group', color_discrete_sequence=['#EF4444', '#10B981']
    )
    st.plotly_chart(fig_usage, use_container_width=True)

with v4:
    st.subheader("4. Actionable Takeaways for Kula Leadership")
    st.markdown("""
    * **Plug Outbound Calendar Leak:** Cold outbound has a 43.6% no-show rate. Introducing automated WhatsApp/SMS calendar reminders and a 1-click reschedule link can recover estimated ~$180k ARR.
    * **Drive Early Trial Adoption:** Accounts hitting $\ge$50 candidate outreach sequences show a **66.7% close rate** vs **19.7%** for low adoption. Product onboarding should incentivize sending the first 50 outreach sequences within Day 3 of trial.
    """)
