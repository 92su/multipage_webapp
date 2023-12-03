import streamlit as st
from multiapp import MultiApp
from apps import home,data,map

st.set_page_config(layout='wide',initial_sidebar_state='expanded')

with open ('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

#st.sidebar.header('Dashboard `version 1`' )


app = MultiApp()

st.markdown("""
# Online Business Registration System Data Analysis

""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Data", data.app)
app.add_app("Map", map.app)

app.run()
