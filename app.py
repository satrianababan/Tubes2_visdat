import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_option_menu import option_menu
from preprocess_viz_top_skills import preprocess_data, create_view_model_top_skills, get_time_series_skill_trend
import pydeck as pdk

st.set_page_config(
    page_title="DataIT Job Whit What 2023",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #152a4f 0%, #161B22 50%, #0c172d 100%);
        color: #E6EDF3;
        font-family: sans-serif !important
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Custom CSS
st.markdown("""
<style>
div[data-testid="stSelectbox"] > div {
    width: 300px;
}
</style>
""", unsafe_allow_html=True)

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
df_top5_skills_trend = get_time_series_skill_trend(df_jobs_clean, df_skills_clean, df_skills_job_clean)


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
    'gradient_colors' : ['#014A7A', '#01579B', '#0277BD', '#0288D1', '#039BE5', '#03A9F4', '#29B6F6', '#4FC3F7', '#81D4FA', '#B3E5FC']
}



# =========================================== SIDEBAR =======================================================
with st.sidebar:
    st.markdown("<h2 style='color:white; font-weight:bold;'> 💼  Data IT</h2>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title = "",
        options=["🏠 Overview", "💰 Salary", "🛠️ Top Skills", "📍 Location"],
        default_index=0,
        styles={
            "container": {
                "background-color": "transparent",
            },
            "icon": {
                "color": "transparent",
                "font-size": "20px"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0.3rem 0",
                "color": "white",
                "border-radius": "8px",
            },
            "nav-link-hover": {
                "background-color": "rgba(255, 255, 255, 0.2)",
                "color": "white",
                "font-weight": "bold",
            },
            "nav-link-selected": {
                "background-color": "rgba(255, 255, 255, 0.2)",
                "color": "white",
                "font-weight": "bold",
            }
        }
    )
# =========================================== SIDEBAR =======================================================




#========================================== OVERVIEW PAGE ==================================================
if selected == "🏠 Overview":
    st.title("💼 IT Job Market Explorer 2023")
    
    # Hero Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem 2rem; 
                border-radius: 15px; 
                color: white; 
                margin-bottom: 2.5rem;
                text-align: center;
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.1);">
        <h1 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 300;">🚀 Welcome to Your Career Compass</h1>
        <p style="font-size: 1.3rem; margin-bottom: 1.5rem; opacity: 0.95;">
            Navigate the dynamic landscape of IT opportunities with confidence
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8; opacity: 0.9; max-width: 800px; margin: 0 auto;">
            Dive into a comprehensive analysis of the global IT job market. Whether you're a seasoned 
            professional looking for your next challenge or a newcomer exploring career paths, this dashboard 
            provides the insights you need to make informed decisions about your future in technology.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # What You'll Discover Section
    st.markdown("## ✨ Discover Market Insights")
    
    # First row - 2 columns for better spacing
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin-bottom: 1.5rem;
                    color: white;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🌍</div>
            <h3 style="margin-bottom: 1rem; font-weight: 500;">Global Opportunities</h3>
            <p style="line-height: 1.6; opacity: 0.95; margin: 0;">
                Explore job markets across different countries and discover where your expertise is most valued worldwide.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin-bottom: 1.5rem;
                    color: white;
                    box-shadow: 0 8px 25px rgba(79, 172, 254, 0.15);">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">💡</div>
            <h3 style="margin-bottom: 1rem; font-weight: 500;">Role Diversity</h3>
            <p style="line-height: 1.6; opacity: 0.95; margin: 0;">
                From AI engineers to UX designers, discover the full spectrum of IT careers and find your perfect match.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row - single column for market trends
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fa709a, #fee140); 
                padding: 2rem; 
                border-radius: 15px; 
                margin-bottom: 2rem;
                color: white;
                text-align: center;
                box-shadow: 0 8px 25px rgba(250, 112, 154, 0.15);">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
        <h3 style="margin-bottom: 1rem; font-weight: 500;">Market Intelligence</h3>
        <p style="line-height: 1.6; opacity: 0.95; margin: 0; max-width: 600px; margin: 0 auto;">
            Stay ahead with comprehensive insights into salary trends, skill demands, and emerging technologies shaping the future of work.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Journey Steps
    st.markdown("## 🗺️ Your Exploration Journey")
    
    # Create better spacing for journey steps
    step1, step2, step3 = st.columns(3)
    
    with step1:
        st.markdown("""
        <div style="background: #f8fafc; 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    text-align: center;
                    border: 2px solid #e2e8f0;
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📍</div>
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Explore</h4>
            <p style="color: #4a5568; margin: 0; font-size: 0.9rem;">
                Navigate through different sections using the sidebar
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step2:
        st.markdown("""
        <div style="background: #f8fafc; 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    text-align: center;
                    border: 2px solid #e2e8f0;
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🔍</div>
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Analyze</h4>
            <p style="color: #4a5568; margin: 0; font-size: 0.9rem;">
                Dive deep into salary trends and market insights
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with step3:
        st.markdown("""
        <div style="background: #f8fafc; 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    text-align: center;
                    border: 2px solid #e2e8f0;
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Decide</h4>
            <p style="color: #4a5568; margin: 0; font-size: 0.9rem;">
                Make informed career decisions with data
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2.5rem; 
                border-radius: 12px; 
                text-align: center; 
                color: white; 
                margin: 2rem 0;">
        <h3 style="margin-bottom: 1rem; font-weight: 300;">Ready to Shape Your Future? 🚀</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem; opacity: 0.95;">
            Use the sidebar to navigate through detailed analytics and uncover the opportunities that await you in the IT industry
        </p>
        <div style="background: rgba(255,255,255,0.2); 
                    padding: 0.8rem 2rem; 
                    border-radius: 25px; 
                    display: inline-block; 
                    backdrop-filter: blur(10px);">
            ✨ Start exploring now and discover your next career move!
        </div>
    </div>
    """, unsafe_allow_html=True)
#========================================== OVERVIEW PAGE ==================================================



#=========================================== VARAZ =======================================================
elif selected == "💰 Salary":
    st.header("💰 Salary Analysis")
    # Tambahkan plot salary di sini

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


    # Chart utama
    fig = go.Figure()

    # Add bars dengan gradient effect
    fig.add_trace(go.Bar(
        x=display_df.sort_values(by="avg_salary")["avg_salary"],
        y=display_df.sort_values(by="avg_salary")["job_title_short"],
        orientation='h',
        marker=dict(
            color=display_df.sort_values(by="avg_salary", ascending=False)["avg_salary"],
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
            xaxis=dict(gridcolor=DARK_THEME['grid_color'], title_text="Salary Year Average"),
            yaxis=dict(
                gridcolor=DARK_THEME['grid_color'],
                title_text="Number of People"  # <--- TAMBAHKAN BARIS INI atau title="Jumlah Orang"
            ),
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
#=========================================== VARAZ =======================================================





#=========================================== ROY =======================================================
elif selected == "🛠️ Top Skills":
    st.header("🛠️ Top Skills")
    # Tambahkan visualisasi skills di sini
    def format_k(n):
        return f"{n / 1_000:.3f}K" if n >= 1_000 else str(n)
    
    st.markdown("""
        <style>
        div[data-baseweb="select"] > div {
            font-size: 20px;  /* ukuran teks dropdown */
        }
        label {
            font-size: 22px;  /* ukuran label 'Job Title :' */
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    #job title short
    job_titles = ["Select All"] + sorted(job_df['job_title_short'].unique())

    selected_job_title = st.selectbox(
        "Job Title :",
        options=job_titles,
        key='job_title1',
        index=0
    )

    # type skills
    skill_type = ["All", "programming","databases", "webframeworks", "analyst_tools", "cloud", "os","sync","async", "other"]
    def format_label(option):
        if option == "databases":
            return "Databases"
        elif option == "analyst_tools":
            return "Tools"
        elif option == "programming":
            return "Languages"
        elif option == "webframeworks":
            return "Frameworks"
        elif option == "cloud":
            return "Cloud"
        elif option == "os":
            return "OS"
        elif option == "other":
            return "Other"
        else:
            return option
        

    selected_type_skill = st.radio(
        "Skills :",
        options=skill_type,
        index=0,
        format_func=format_label,
        horizontal=True
    )


    # Filter data
    filtered = df_top10_skills.copy()
    if selected_job_title != "Select All":
        filtered = filtered[filtered['job_title_short'] == selected_job_title]

    if selected_type_skill != "All":
        filtered = filtered[filtered['type'] == selected_type_skill]


    # Total job postings (unik job_id)
    total_jobs = filtered['job_title'].nunique()

    # Hitung berapa job unik per skill
    skill_job_counts = filtered.groupby('skills')['job_title'].nunique()

    # Ambil top 20 skills berdasarkan jumlah job_id (bukan count rows)
    top10_skills = skill_job_counts.nlargest(20).index.tolist()

    # Hitung persentase per skill per total job_id
    percent_per_skill = (skill_job_counts[top10_skills] / total_jobs * 100).round(2)

    # Urutkan skill berdasarkan persentase (atau tetap pakai original order, sesuai preferensi)
    skill_order = percent_per_skill.sort_values().index.tolist()
        
    colorscale = px.colors.sequential.Tealgrn[::-1]
    max_val = max(percent_per_skill[skill_order])
    xaxis_max = max_val + 5 if max_val + 5 <= 100 else 100

    bar_count = len(skill_order)
    fig_height = 700
    bar_slot = fig_height / bar_count
    font_size = int(bar_slot * 0.7)  # ambil 70% dari slot, biar proporsional

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=skill_order,
        x=percent_per_skill[skill_order],
        orientation='h',
        marker=dict(
            color=percent_per_skill[skill_order],
            colorscale=colorscale,
            line=dict(color='rgba(0,0,0,0)', width=2),
        ),
        hovertemplate=f"<b>%{{y}}</b><br>📊jobfair requires %{{x:.1f}}% <extra></extra>"
    ))

    annotations = []
    for i, skill in enumerate(skill_order):
        val = percent_per_skill[skill]
        # Text skill di kiri
        annotations.append(dict(
            x=0,
            y=skill,
            xanchor='right',
            yanchor='middle',
            text=skill,
            font=dict(color='white', size=font_size),
            showarrow=False,
            xshift=-10
        ))
        # Persentase di kanan
        annotations.append(dict(
            x=val,
            y=skill,
            xanchor='left',
            yanchor='middle',
            text=f"{val:.1f}%",
            font=dict(color='white', size=font_size),
            showarrow=False,
            xshift=10
        ))

    fig.update_layout(
        annotations=annotations,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            visible=False,
            range=[0, xaxis_max]
        ),
        yaxis=dict(
            visible=False,
            categoryorder='total ascending'
        ),
        margin=dict(l=150, r=40, t=60, b=40),
        newselection_line=dict(
            color='white',
            dash='solid'
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='#16213e',
            bordercolor='white',
            font=dict(color='white', size=0.75*font_size),
        ),
        hoverdistance=40,
        bargap=0.3,
        height=700
    )


    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'modeBarButtonsToRemove': [
            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
            'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
            'toggleSpikelines', 'toImage'
        ],
        'displaylogo': False
    })

    st.markdown("---")
    st.header("📈 Demand Skills")

    job_titles2 = ["Select All"] + sorted(job_df['job_title_short'].unique())

    selected_job_title2 = st.selectbox(
        "Job Title :",
        options=job_titles2,
        key='job_title2',
        index=0
    )

    job_type = ["Select All"] + sorted(job_df['job_schedule_type'].dropna().unique())

    # Filter data
    filtered2 = df_top5_skills_trend.copy()
    if selected_job_title2 != "Select All":
        filtered2 = filtered2[filtered2['job_title_short'] == selected_job_title2]
    
    # Total job postings (unik job_id)
    total_jobs2 = filtered2['job_title'].nunique()

    # Hitung berapa job unik per skill
    skill_job_counts2 = filtered2.groupby('skills')['job_title'].nunique()

    # Ambil top 5 skills berdasarkan jumlah job_id (bukan count rows)
    top5_skills = skill_job_counts2.nlargest(5).index.tolist()

    # Ambil hanya baris dengan skill teratas
    filtered_top5 = filtered2[filtered2['skills'].isin(top5_skills)]

    # Hitung jumlah posting per tanggal per skill
    # Buat semua kombinasi tanggal x skill (supaya bisa isi 0)
    all_dates = pd.date_range(filtered_top5['job_posted_date'].dt.date.min(), filtered_top5['job_posted_date'].dt.date.max())
    all_dates= all_dates.date
    all_combinations = pd.MultiIndex.from_product([all_dates, top5_skills], names=["job_posted_date", "skills"]).to_frame(index=False)

    # Hitung jumlah posting per tanggal per skill
    filtered_top5['job_posted_date'] = pd.to_datetime(filtered_top5['job_posted_date']).dt.date
    df_trend = (
        filtered_top5
        .groupby(['job_posted_date', 'skills'])['job_title']
        .nunique()
        .reset_index(name='count')
    )


    # Gabungkan dengan semua kombinasi dan isi NaN dengan 0
    df_trend_full = (
        all_combinations
        .merge(df_trend, on=['job_posted_date', 'skills'], how='left')
        .fillna({'count': 0})
        .sort_values('job_posted_date')
    )

    # Ubah count ke integer
    df_trend_full['count'] = df_trend_full['count'].astype(int)

    # Buat line chart per skill
    fig = go.Figure()
    for skill in top5_skills:
        df_skill = df_trend_full[df_trend_full['skills'] == skill]
        fig.add_trace(go.Scatter(
            x=df_skill['job_posted_date'],
            y=df_skill['count'],
            mode='lines',
            name=skill
            
    ))


    min_date = filtered_top5['job_posted_date'].min()
    max_date = filtered_top5['job_posted_date'].max()

    fig.update_layout(
        title=dict(
            text="Top 5 Trend Skills in Demand by Time Series",
            x=0.5,
            xanchor='center',
            font=dict(size=15, color='white')
        ),
        xaxis_title='',
        yaxis_title='',
        hoverdistance=100,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='black',
            bordercolor='white',
            font_size=14,
            font_color='white'
        ),
        dragmode='pan',
        xaxis=dict(
            range=[min_date, max_date],
            minallowed=min_date,
            maxallowed=max_date,
            type='date',
            fixedrange=False,
            constrain='range',
            rangeslider=dict(visible=True, thickness=0.0),
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikecolor='rgba(255, 255, 255, 0.4)',
            spikethickness=0.05,
            showline=True,
            showgrid=True,
            linecolor='white',
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        ),


        yaxis=dict(
            showspikes=False,
            spikemode='across',
            spikesnap='cursor',
            showline=True,
            showgrid=True,
            linecolor='white',
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True, config={
        'scrollZoom': True,  # zoom dengan scroll mouse aktif
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtons': [
            ['pan2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
        ],
    })





#=========================================== ROY =======================================================

#=========================================== SATRIA =======================================================
elif selected == "📍 Location":
    st.header("🌍 Job Openings by Country")
    st.markdown("This map shows the distribution of job vacancies across countries from the dataset.")

    # =======================
    # PREPARE COUNTRY COUNT
    # =======================
    # Hitung jumlah lowongan per negara
    job_postings_fact = pd.read_csv('data/job_postings_fact.csv')
    # Bersihkan negara yang tidak relevan
    invalid_countries = ["Remote", "Worldwide", "Europe", "Asia", "Africa", "", None]
    job_postings_fact = job_postings_fact[~job_postings_fact['job_country'].isin(invalid_countries)]

    # Hitung jumlah job per negara
    country_counts = job_postings_fact['job_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Job Count']

    # Tambahkan koordinat negara (bisa diperluas lagi)
    country_coords = pd.DataFrame({
        'Country': ['United States', 'India', 'Germany', 'United Kingdom', 'Indonesia', 
                    'Canada', 'Australia', 'France', 'Brazil', 'Japan'],
        'lat': [37.0902, 20.5937, 51.1657, 55.3781, -0.7893, 
                56.1304, -25.2744, 46.2276, -14.2350, 36.2048],
        'lon': [-95.7129, 78.9629, 10.4515, -3.4360, 113.9213, 
                -106.3468, 133.7751, 2.2137, -51.9253, 138.2529]
    })

    # Gabungkan
    map_data = pd.merge(country_counts, country_coords, on='Country', how='left')
    map_data.dropna(subset=['lat', 'lon'], inplace=True)

    # Normalisasi radius
    map_data['radius'] = map_data['Job Count'] / map_data['Job Count'].max() * 500000

    # Tampilkan map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v10',
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[lon, lat]',
                get_fill_color='[255, 100, 100, 160]',
                get_radius='radius',
                pickable=True,
            ),
        ],
        tooltip={"text": "{Country}\nJobs: {Job Count}"}
    ))

#=========================================== SATRIA =======================================================

#========================================== FOOTER =======================================================
# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🚀 DataIT Job Market Analysis Dashboard</p>
    <p>Built with Streamlit • Data from 2023 Job Market</p>
</div>
""", unsafe_allow_html=True)
#========================================== FOOTER ======================================================

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