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
    df_merged = df_skills_job.merge(df_jobs[['job_id','job_title', 'job_title_short']], on='job_id', how='left')
    df_summary = df_merged.groupby(['job_title_short', 'skills', 'job_title', 'type']).size().reset_index(name='count')

    return df_summary


@st.cache_data(show_spinner=False)
def get_time_series_skill_trend(df_jobs, df_skills, df_skills_job):
    df_skills_job = df_skills_job.merge(df_skills, on='skill_id', how='left')
    df_merged = df_skills_job.merge(df_jobs[['job_id', 'job_title', 'job_title_short', 'job_posted_date','job_schedule_type']],on='job_id', how='left')

    # Pastikan tanggal dalam format datetime
    df_merged['job_posted_date'] = pd.to_datetime(df_merged['job_posted_date'])

    # Grouping berdasarkan skill + tanggal posting
    df_summary = df_merged.groupby(['job_title_short','job_title', 'skills', 'job_posted_date','job_schedule_type']).size().reset_index(name='count')

    return df_summary
