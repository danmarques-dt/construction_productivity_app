import streamlit as st
import pandas as pd
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
import base64
import io
import matplotlib.pyplot as plt

# ---- Page Configuration ----

st.set_page_config(page_title='Productivity In Construction',page_icon=':bar_chart:',layout='wide', initial_sidebar_state='expanded')

#---- Hide streamlit style ----

hide_st_style = """
                <style>
                #MainMenu {visibility: visible;}
                footer {visibility: visible;}
                footer:after {content: 'Copyright @ 2023: Daniel Marques';
                    display:block;
                    position:relative
                    
                } 
                header {visibility: hidden;} 
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)

# ---- Header Section ----


st.title('Construction Productivity Tracker')

st.write('This app provides a comprehensive tracker of productivity among the construction sites of the company.')
st.write('It envolves all of the company current construction sites and delivers information to exchange information between them. \
          Overall, this app serves as a valuable resource for the company \
          seeking to improve productivity and stay up-to-date on the latest trends and best practices.')

st.markdown('#### Follow-Up')

st.markdown(' A page where you can check a construction activity across the months.')
st.write('*For example: What is the average productivity for installing countertops in my construction site? And how am I performing over the months?*')

st.markdown('#### Comparison')

st.markdown('A page where you can compare a productivity index to other construction sites.')
st.write('*For example: What is the average productivity across residential construction sites? What is the construction site that is performing the better?*')

st.markdown('#### Understand')
st.write('To better comprehend and start using this tool check this short post that I wrote: [Check the post](https://medium.com/@danmarques.ai/construction-productivity-app-in-streamlit-ea93514cb343)')
st.write('You can check the Github Repo to view and get the code to this app: [Check the github repo](https://github.com/danmarques-dt/construction_productivity_app)')

# Contact
st.sidebar.title("Contact")
st.sidebar.info(
    """
    Daniel Marques: [E-mail](mailto:danmarques.ai@gmail.com), 
    [Linkedin](https://www.linkedin.com/in/danmarques-ai/) or
    [Instagram](https://www.instagram.com/danmarques.dt/) 
    """
    )



