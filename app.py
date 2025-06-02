import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from preprocess_viz_top_skills import preprocess_data, create_view_model_top_skills, show_top_skills


st.set_page_config(
    page_title="DataIT Job Whit What 2023",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    
    job_data = []
    job_titles = ['Data Scientist', 'Data Engineer', 'Data Analyst', 'ML Engineer', 
                  'Software Engineer', 'Product Manager', 'DevOps Engineer']
    
    for _ in range(1000):
        job_data.append({
            'job_posted_date': np.random.choice(dates),
            'job_title_short': np.random.choice(job_titles),
            'salary_year_avg': np.random.randint(50000, 200000)
        })
    
    return pd.DataFrame(job_data)


# load data asli
try:
    job_df = pd.read_csv('data/job_postings_fact.csv')
    df_skills = pd.read_csv('data/skills_dim.csv')
    df_skills_job = pd.read_csv('data/skills_job_dim.csv')
except:
    st.warning("Data file tidak ditemukan, menggunakan data simulasi")
    job_df = load_data()

#preprocessing data top skills
df_jobs_clean, df_skills_clean, df_skills_job_clean = preprocess_data(job_df, df_skills, df_skills_job)
df_top10_skills = create_view_model_top_skills(df_jobs_clean, df_skills_clean, df_skills_job_clean)


# Sidebar
with st.sidebar:
    st.title('🚀 DataIT Job Whit What 2023')
    st.markdown("---")
 
    # st.markdown("### 📊 Data View")
    # # Membuat radio button dengan default "All"
    # option = st.radio("Choose data view", ["All", "Only Top 10"], index=0)
    
    st.markdown("### 📅 Filter by Month")
    
    # Filter month
    month_num = {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
        6: "June", 7: "July", 8: "August", 9: "September", 
        10: "October", 11: "November", 12: "December"
    }
    month_name_to_num = {v: k for k, v in month_num.items()}
    
    # Menambahkan opsi "All Months" di awal
    available_months = [month_num[m] for m in sorted(
        pd.to_datetime(job_df["job_posted_date"]).dt.month.unique(), 
        key=lambda month: month
    )]
    month_options = ["All Months"] + available_months
    
    # Selectbox dengan default "All Months"
    month_list = st.selectbox('Select a month', month_options, index=0)
    
    # Set month_chosen berdasarkan pilihan
    if month_list == "All Months":
        month_chosen = None
    else:
        month_chosen = month_name_to_num[month_list]
    
    # st.markdown("---")
    # st.markdown("### 🎨 Theme Settings")
    # st.info("Dark theme aktif! 🌙")
    st.markdown("---")
    st.markdown("### 🛠️ Filter Top Skills")
    job_titles = sorted(job_df['job_title_short'].unique())

    selected_job_titles = st.sidebar.multiselect(
        "🎯 Pilih maksimal 3 Job Title",
        options=job_titles,
        max_selections=3
    )

# Filter berdasarkan bulan dan option
if month_chosen is not None:
    job_df_filtered = job_df[pd.to_datetime(job_df["job_posted_date"]).dt.month == month_chosen]
    display_month = month_list
else:
    job_df_filtered = job_df.copy()
    display_month = "All Months"

# Preprocess data gaji 
job_df_filtered = job_df_filtered.dropna(subset=["salary_year_avg"])

summary_df = job_df_filtered.groupby("job_title_short").agg(
    avg_salary=("salary_year_avg", "mean"),
    max_salary=("salary_year_avg", "max"),
    min_salary=("salary_year_avg", "min"),
    count=("salary_year_avg", "count")
).reset_index()

# Gunakan radio button untuk menentukan data yang ditampilkan

display_df = summary_df.sort_values(by="avg_salary", ascending=False).head(10)
chart_title = f"Top 10 Highest Paying Jobs - {display_month} 2023"

# Page Title
st.title("💼 Data IT Job Market Analysis 2023")
st.markdown(f"### Analisis untuk: **{display_month}**")

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏢 Total Jobs", 
        value=f"{len(job_df_filtered):,}",
        delta=f"+{len(job_df_filtered) - 500}" if len(job_df_filtered) > 500 else None
    )

with col2:
    avg_salary = job_df_filtered["salary_year_avg"].mean()
    st.metric(
        label="💰 Avg Salary", 
        value=f"${avg_salary:,.0f}",
        delta=f"+${avg_salary - 80000:,.0f}" if avg_salary > 80000 else None
    )

with col3:
    max_salary = job_df_filtered["salary_year_avg"].max()
    st.metric(
        label="🚀 Highest Salary", 
        value=f"${max_salary:,.0f}"
    )

with col4:
    unique_titles = job_df_filtered["job_title_short"].nunique()
    st.metric(
        label="🎯 Job Types", 
        value=unique_titles
    )

st.markdown("---")

# Warna tema dark yang konsisten
DARK_THEME = {
    'background_color': '#0E1117',
    'paper_color': '#262730',
    'text_color': '#FAFAFA',
    'grid_color': '#464853',
    'primary_color': '#FF6B6B',
    'secondary_color': '#4ECDC4',
    'success_color': '#45B7D1',
    'accent_colors': ['#FF6B6B', '#4ECDC4', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF'],
    'gradient_colors' : ['#B3E5FC', '#81D4FA', '#4FC3F7', '#29B6F6', '#03A9F4', '#039BE5', '#0288D1', '#0277BD', '#01579B', '#014A7A']
}

# Chart utama
fig = go.Figure()

# Add bars dengan gradient effect
fig.add_trace(go.Bar(
    x=display_df.sort_values(by="avg_salary")["avg_salary"],
    y=display_df.sort_values(by="avg_salary")["job_title_short"],
    orientation='h',
    marker=dict(
        color=display_df.sort_values(by="avg_salary")["avg_salary"],
        # colorscale='Plasma',
        line=dict(color=DARK_THEME["gradient_colors"])
    ),
    text=[f'${x:,.0f}' for x in display_df.sort_values(by="avg_salary")["avg_salary"]],
    textposition='outside',
    textfont=dict(color=DARK_THEME['text_color'], size=11),
    customdata=display_df.sort_values(by="avg_salary")[["max_salary", "min_salary", "count"]].values,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "💰 Avg Salary: $%{x:,.0f}<br>"
        "📈 Max Salary: $%{customdata[0]:,.0f}<br>"
        "📉 Min Salary: $%{customdata[1]:,.0f}<br>"
        "👥 Total Workers: %{customdata[2]}<br>"
        "<extra></extra>"
    )
))

# Layout dengan tema dark
fig.update_layout(
    title={
        'text': chart_title,
        'font': {'size': 20, 'color': DARK_THEME['text_color']},
        'x': 0.5
    },
    plot_bgcolor=DARK_THEME['background_color'],
    paper_bgcolor=DARK_THEME['paper_color'],
    font=dict(color=DARK_THEME['text_color']),
    xaxis=dict(
        title="Average Yearly Salary (USD)",
        gridcolor=DARK_THEME['grid_color'],
        zeroline=False,
        tickformat='$,.0f'
    ),
    yaxis=dict(
        title="Job Title",
        gridcolor=DARK_THEME['grid_color'],
        zeroline=False
    ),
    margin=dict(l=20, r=20, t=60, b=20),
    height=500,
    hoverlabel=dict(
        bgcolor=DARK_THEME['paper_color'],
        bordercolor=DARK_THEME['primary_color'],
        font_color=DARK_THEME['text_color']
    )
)

st.plotly_chart(fig, use_container_width=True)

# Chart tambahan
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Salary Distribution")
    
    fig_hist = px.histogram(
        job_df_filtered, 
        x="salary_year_avg", 
        nbins=20,
        title="Salary Distribution"
    )
    
    fig_hist.update_layout(
        plot_bgcolor=DARK_THEME['background_color'],
        paper_bgcolor=DARK_THEME['paper_color'],
        font=dict(color=DARK_THEME['text_color']),
        xaxis=dict(gridcolor=DARK_THEME['grid_color']),
        yaxis=dict(gridcolor=DARK_THEME['grid_color']),
        bargap=0.1
    )
    
    fig_hist.update_traces(marker_color=DARK_THEME['primary_color'])
    
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.markdown("### 🥧 Job Title Distribution")
    
    job_counts = job_df_filtered["job_title_short"].value_counts().head(8)
    
    fig_pie = px.pie(
        values=job_counts.values,
        names=job_counts.index,
        title="Job Title Distribution"
    )
    
    fig_pie.update_layout(
        plot_bgcolor=DARK_THEME['background_color'],
        paper_bgcolor=DARK_THEME['paper_color'],
        font=dict(color=DARK_THEME['text_color'])
    )
    
    fig_pie.update_traces(
        marker=dict(colors=DARK_THEME['accent_colors']),
        textfont=dict(color=DARK_THEME['text_color'])
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

def format_k(n):
    return f"{n / 1_000:.3f}K" if n >= 1_000 else str(n)

if selected_job_titles:
    st.markdown("---")
    st.markdown("### 🔍 Top Skills for Selected Job Titles")

    filtered = df_top10_skills[df_top10_skills['job_title_short'].isin(selected_job_titles)]

    # Total semua skill count gabungan (all data)
    total_all_count = filtered['count'].sum()

    # Top 10 skills secara total
    top10_skills = (
        filtered.groupby('skills')['count']
        .sum()
        .nlargest(10)
        .index.tolist()
    )

    filtered = filtered[filtered['skills'].isin(top10_skills)]
    skill_order = (
        filtered.groupby('skills')['count']
        .sum()
        .sort_values()
        .index.tolist()
    )

    # Urutkan job titles dari total terbesar (biar stack kiri dominan)
    job_title_order = (
        filtered.groupby('job_title_short')['count']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    colors = ['#4ECDC4', '#FF6B6B', '#556270', '#C7F464', '#FFAA5C', '#6B5B95']

    fig = go.Figure()

    for i, jt in enumerate(job_title_order):
        df_jt = (
            filtered[filtered['job_title_short'] == jt]
            .set_index('skills')
            .reindex(skill_order, fill_value=0)
            .reset_index()
        )

        fig.add_trace(go.Bar(
            y=df_jt['skills'],
            x=df_jt['count'],
            name=jt,
            orientation='h',
            marker_color=colors[i % len(colors)],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "📊 Percentage: %{customdata[0]:.1f}%<br>"
                "🔢 Count: %{customdata[1]} from %{customdata[2]} data<extra></extra>"
            ),
            customdata=[
                (
                    (row['count'] / total_all_count * 100) if total_all_count > 0 else 0,
                    f"{row['count']/1_000:.1f}K" if row['count'] >= 1_000 else str(row['count']),
                    f"{total_all_count/1_000:.1f}K" if total_all_count >= 1_000 else str(total_all_count)
                )
                for _, row in df_jt.iterrows()
            ]
        ))

    fig.update_layout(
        barmode='stack',
        title="Top 10 Skills Distribution for Selected Job Titles",
        plot_bgcolor=DARK_THEME['background_color'],
        paper_bgcolor=DARK_THEME['paper_color'],
        font=dict(color=DARK_THEME['text_color']),
        xaxis=dict(title='Count', gridcolor=DARK_THEME['grid_color']),
        yaxis=dict(title='Skill', categoryorder='array', categoryarray=skill_order, gridcolor=DARK_THEME['grid_color']),
        margin=dict(l=20, r=20, t=60, b=20),
        height=600,
        legend_title_text='Job Title',
        hoverlabel=dict(
            bgcolor=DARK_THEME['paper_color'],
            bordercolor=DARK_THEME['primary_color'],
            font_color=DARK_THEME['text_color']
        )
    )

    st.plotly_chart(fig, use_container_width=True)




# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🚀 DataIT Job Market Analysis Dashboard</p>
    <p>Built with Streamlit • Data from 2023 Job Market</p>
</div>
""", unsafe_allow_html=True)

# # Sidebar instructions
# st.sidebar.markdown("---")
# st.sidebar.markdown("### 🛠️ Setup Instructions")
# st.sidebar.markdown("""
# **Untuk tema dark permanent:**

# 1. Buat file `.streamlit/config.toml`:
# ```toml
# [theme]
# primaryColor = "#FF6B6B"
# backgroundColor = "#0E1117"
# secondaryBackgroundColor = "#262730"
# textColor = "#FAFAFA"
# font = "sans serif"
# ```

# 2. Atau run dengan command:
# ```bash
# streamlit run app.py --theme.base="dark"
# ```
# """)