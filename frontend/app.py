import streamlit as st
import sys, os

# allow import from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Interface import analyze_repo

st.set_page_config(page_title="GitHub Health Analyzer", layout="centered")

st.title(" GitHub Project Health Analyzer")

owner = st.text_input("Repository Owner", placeholder="e.g. tensorflow")
repo = st.text_input("Repository Name", placeholder="e.g. tensorflow")

threshold = st.number_input(
    "Regular Contributor Threshold",
    min_value=2,
    max_value=100,
    value=5,
    step=1
)

if st.button("Analyze Project"):

    if owner and repo:
        with st.spinner("Running analysis..."):
            results = analyze_repo(owner, repo)

        st.success("Analysis Complete")

        for key, value in results.items():
            st.subheader(key)
            st.write(value)

    else:
        st.warning("Please enter both owner and repository name.")