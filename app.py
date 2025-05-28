import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#file
# comp_df = pd.read_csv('data/company_dim.csv')
job_df = pd.read_csv('data/job_postings_fact.csv')
# skill_df = pd.read_csv('data/company_dim.csv')

# Page configuration
st.set_page_config(
    page_title="DataIT Job Whit What 2023",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


with st.sidebar:
    st.title('DataIT Job Whit What 2023')


    option = st.radio("Choose data view (masih mock)", ["All", "Only Top 10"])


    month_num = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
            6: "June", 7: "July", 8: "August", 9: "September", 
            10: "October", 11: "November", 12: "December"
    }
    month_name_to_num = {v: k for k, v in month_num.items()} #take month num again

    month_names = [month_num[m] for m in sorted
    (
        pd.to_datetime(job_df["job_posted_date"]).dt.month.unique(), key=lambda month: month   #sort month name (jan to dec)
    )]


    #filter based on month
    month_list = st.selectbox('Select a month', month_names)

    month_chosen = month_name_to_num[month_list]

    df_month_chosen = job_df[pd.to_datetime(job_df["job_posted_date"]).dt.month == month_chosen]


    #avg salary year for filter month

    #preprocess data gaji 
    job_df= df_month_chosen.dropna(subset=["salary_year_avg"])

    summary_df = df_month_chosen.groupby("job_title_short").agg(
        avg_salary=("salary_year_avg", "mean"),
        max_salary=("salary_year_avg", "max"),
        min_salary=("salary_year_avg", "min"),
        count=("salary_year_avg", "count")
    ).reset_index()

    top10_df = summary_df.sort_values(by="avg_salary", ascending=False).head(10)
    # df_month_chosen_sort_salary_year_month = df_month_chosen.sort_values(by="", ascending=False)


#-------------------------------------------------------------------------------


#preprocess data gaji 
job_df= job_df.dropna(subset=["salary_year_avg"])

summary_df = job_df.groupby("job_title_short").agg(
    avg_salary=("salary_year_avg", "mean"),
    max_salary=("salary_year_avg", "max"),
    min_salary=("salary_year_avg", "min"),
    count=("salary_year_avg", "count")
).reset_index()

top10_df = summary_df.sort_values(by="avg_salary", ascending=False).head(10)




fig = px.bar(
    # job_df.sort_values(job_df["salary_year_average"], ascending=True),
    top10_df.sort_values(by="avg_salary"),  # biar urut dari kecil ke besar
    x="avg_salary",
    y="job_title_short",
    orientation='h',
    text="avg_salary",
    labels={"avg_salary": "Avg Yearly Salary", "job_title_short": "Job Title"},
    title="Top 10 Highest Paying Job Titles (Yearly Average)"
)

#tooltip
fig.update_traces(
    texttemplate='$%{text:,.0f}',
    customdata=top10_df[["max_salary", "min_salary", "count"]],
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Avg Salary: $%{x:,.0f}<br>"
        "Max Salary: $%{customdata[0]:,.0f}<br>"
        "Min Salary: $%{customdata[1]:,.0f}<br>"
        "Total Worker: %{customdata[2]}"
    )
)

# Layout styling (opsional)
fig.update_layout(
    plot_bgcolor="rgba(120,21,89,0.78)",
    paper_bgcolor="rgba(25,150,35,0.7)",
    font=dict(color="white"),
    title_font=dict(size=20)
)

# Tampilkan di Streamlit
st.plotly_chart(fig, use_container_width=True)