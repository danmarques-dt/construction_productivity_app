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

# ---- Data handling---- 

@st.cache_data
def get_data_from_excel():

    prod = pd.read_excel(io='construction_productivity.xlsx',
                        engine='openpyxl',
                        sheet_name='database',
                        usecols='A:O')

    prod['production'] = round(prod['production'],2)
    prod['prod_index'] = round(prod['prod_index'],2)

    return prod

prod = get_data_from_excel()

# ---- Header Section ----

st.title('Productivity Follow-Up Between Construction Activities')
    
'----'
# ---- Sidebar ----

# Sidebar Logo
image = Image.open("images/dan-marques-logo.png")
st.sidebar.image(image, use_column_width=True)

# Sidebar title
st.sidebar.title("Filters")

#### SIDEBAR FILTERS ####

# Dynamic month filter 
year = st.sidebar.multiselect(
    "year:",
    options=prod["year"].unique(),
    default=prod["year"].unique()
)
# Filter the DataFrame with selected years
year_selec = prod[prod["year"].isin(year)]

# unique years
month_selec = year_selec["month"].unique()

# Verify selected year
if year:
    month= st.sidebar.multiselect(
        "Month:",
        options=month_selec,
        default=month_selec
    )
else:
    month= []

if month:
    city = st.sidebar.multiselect(
        "city:",
        options=prod[prod["month"].isin(month)]["city"].unique(),
        default=prod[prod["month"].isin(month)]["city"].unique()
)
else:
    city = []

if  city: 
    type = st.sidebar.multiselect(
    "type:",
    options=prod[prod["city"].isin(city)]["type"].unique(),
    default=prod[prod["city"].isin(city)]["type"].unique()
)
else:
    type = []

# Contact
st.sidebar.title("Contact")
st.sidebar.info(
    """
    Daniel Marques: [E-mail](mailto:danmarques.ai@gmail.com), 
    [Linkedin](https://www.linkedin.com/in/danmarques-ai/) or
    [Instagram](https://www.instagram.com/danmarques.dt/) 
    """
)

# ---- Selections ----

st.markdown('##### Select one construction site, category and activity to see the metrics')
c1, c2, c3 = st.columns(3)

if type:
    construction_site = c1.multiselect(
    "Construction Site:",
    options=prod[(prod["type"].isin(type)) & (prod["city"].isin(city))]["construction_site"].unique(),
    default=[]
)
else:
    construction_site = []

if construction_site:
    etapa = c2.multiselect(
        "Category: ",
        options=prod[prod["construction_site"].isin(construction_site)]["category"].unique(),
        default=[]
)
else:
    etapa = []

if etapa:
    activity = c3.multiselect(
    "activity:",
    options=prod[(prod["category"].isin(etapa)) & (prod["construction_site"].isin(construction_site))]["activity"].unique(),
    default=[],
)
else:
    activity = []


## ---- NOVO DATAFRAME UTILIZANDO OS FILTROS ----

df_filtered_sidebar = prod[
    prod["year"].isin(year) &
    prod["month"].isin(month) &
    prod["category"].isin(etapa) &
    prod["activity"].isin(activity) &
    prod["city"].isin(city) &
    prod["type"].isin(type) &
    prod["construction_site"].isin(construction_site)
]

df_filtered_sidebar = df_filtered_sidebar.sort_values(by=["date","construction_site"], ascending=False)


## ---- VERIFICATION OF PREVIOUS MONTHS ----

records_of_fitered_data = df_filtered_sidebar['month'].count()

############################################################ LAST RECORDS ######################################################################
'----'
st.markdown("##### Last Added Records")

# Filter the data
df_filtered_last_records = prod[prod["construction_site"].isin(construction_site)]

# Calculate the last records
last_records = df_filtered_last_records[df_filtered_last_records['date'] == df_filtered_last_records['date'].max()]

# Number of records
number_of_last_records = last_records['month'].count()
st.write(f'Númber of records: {number_of_last_records}')

# Show the data
st.dataframe(last_records[['month_year','construction_site','category','activity','unt','professionals','production','work_days','prod_index']], use_container_width=True)

############################################################ ANALYSIS ######################################################################

## ---- CALCULATE MAXIMUM, MINIMUM, AVERAGES FOR THE METRICS CARDS ----

# Last record for the filter of "prod_index"

last_index = df_filtered_sidebar.sort_values('date', ascending=False)

if not last_index['prod_index'].head(1).empty:
    # Select the value of the column 'prod_index' on the first line
    last_index = round(last_index['prod_index'].iloc[0],2)

else:
    last_index = 0

# Average "prod_index"

avg_index = round(df_filtered_sidebar["prod_index"].mean(),2)

# Maximum "prod_index"

if not df_filtered_sidebar.empty:
    max_row = df_filtered_sidebar.loc[df_filtered_sidebar['prod_index'].idxmax()]
    max_index = max_row['prod_index']
    max_construction_site = max_row['construction_site']

else:
    st.warning('Select at least one activity to generate the chart', icon="⚠️")
    max_index = None
    max_construction_site = None

# Minimum "prod_index"

if not df_filtered_sidebar.empty:
    min_row = df_filtered_sidebar.loc[df_filtered_sidebar['prod_index'].idxmin()]
    min_index = min_row['prod_index']
    min_construction_site = min_row['construction_site']

else:
    st.write("")
    min_index = None
    min_construction_site = None

# Calculate deltas

delta_last_index = round(last_index - avg_index,2)

############################################################ METRICS ######################################################################
'----'
st.markdown("##### Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(label="Last Productivity Index", value=last_index, delta=delta_last_index)
c2.metric(label="Avg Index", value=avg_index)
c3.metric(label="Min Index", value=min_index)
c4.metric(label="Max Index", value=max_index)
c5.write('')
c5.write('')
c5.write(f'Number of records:  {records_of_fitered_data}')

############################################################ LINE CHART ######################################################################
'----'
st.markdown("##### Follow-up of productivity index")

df_filtered_sidebar_chart = df_filtered_sidebar.sort_values('date')

title_line_chart = df_filtered_sidebar_chart['activity'].unique()  

fig = px.line(
    df_filtered_sidebar_chart,
    x="month_year",
    y="prod_index",
    color="activity",
    )
fig.update_xaxes(title_text="Month ")
fig.update_traces(
mode="lines+markers+text", 
text=df_filtered_sidebar_chart["prod_index"],
textposition="top center"
)
# Loop through each trace (line) in the figure and update the text value
for i, trace in enumerate(fig.data):
    # Get the data for the current trace
    x_data = trace.x
    y_data = trace.y
            
    # Create a list of text values for the current trace
    text_values = [f"{y:.2f}" for y in y_data]
    
    # Update the text value for the current trace
    fig.data[i].text = text_values

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

'----'   

## ---- FILTERED DATA AND DOWNLOAD ----

st.markdown(
    "##### Table of selected records"
)

st.dataframe(df_filtered_sidebar[['month_year','construction_site','category','activity','unt','professionals','production','work_days','prod_index']], use_container_width=True)

# Convert the filtered DataFrame into a XLSX file in memory
to_excel = io.BytesIO()
df_filtered_sidebar.to_excel(to_excel, index=False, header=True)
to_excel.seek(0)

# Encode XLSX file in base64
b64 = base64.b64encode(to_excel.read()).decode()   

# Generate download link
href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="follow_up_data.xlsx">Download file in XLSX</a>'
st.markdown(href, unsafe_allow_html=True)



