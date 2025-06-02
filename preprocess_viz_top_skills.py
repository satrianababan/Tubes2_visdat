import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def preprocess_data(df_jobs, df_skills, df_skills_job):
    df_jobs = df_jobs.drop_duplicates(subset=['job_id'])
    df_skills = df_skills.drop_duplicates(subset=['skill_id'])
    df_skills_job = df_skills_job.drop_duplicates(subset=['job_id', 'skill_id'])

    df_jobs = df_jobs.dropna(subset=['job_id', 'job_title_short'])
    df_skills = df_skills.dropna(subset=['skill_id', 'skills'])
    df_skills_job = df_skills_job.dropna(subset=['job_id', 'skill_id'])

    df_jobs['job_id'] = df_jobs['job_id'].astype(str)
    df_skills['skill_id'] = df_skills['skill_id'].astype(str)
    df_skills_job['job_id'] = df_skills_job['job_id'].astype(str)
    df_skills_job['skill_id'] = df_skills_job['skill_id'].astype(str)

    df_jobs['job_title_short'] = df_jobs['job_title_short'].str.strip()
    df_skills['skills'] = df_skills['skills'].str.strip()

    return df_jobs, df_skills, df_skills_job

@st.cache_data(show_spinner=False)
def create_view_model_top_skills(df_jobs, df_skills, df_skills_job):
    df_skills_job = df_skills_job.merge(df_skills, on='skill_id', how='left')
    df_merged = df_skills_job.merge(df_jobs[['job_id', 'job_title_short']], on='job_id', how='left')

    df_summary = df_merged.groupby(['job_title_short', 'skills']).size().reset_index(name='count')
    df_top10 = df_summary.sort_values(['job_title_short', 'count'], ascending=[True, False]) \
                        .groupby('job_title_short').head(10)

    df_top10.to_csv('job_title_skill_count.csv', index=False)
    return df_top10

def show_top_skills(df_jobs, df_skills, df_skills_job):
    job_title_options = df_jobs['job_title_short'].dropna().unique()
    selected_job_title = st.selectbox("Pilih Job Title Short:", options=sorted(job_title_options))

    job_ids = df_jobs.loc[df_jobs['job_title_short'] == selected_job_title, 'job_id'].unique()
    skills_for_jobs = df_skills_job[df_skills_job['job_id'].isin(job_ids)]
    skills_merged = pd.merge(skills_for_jobs, df_skills, on='skill_id', how='left')

    top_skills = skills_merged['skills'].value_counts().head(10)

    st.subheader(f"Top 10 Skills for '{selected_job_title}'")
    if not top_skills.empty:
        st.bar_chart(top_skills)
    else:
        st.write("No skills found for this selection.")
