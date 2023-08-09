import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import plotly.express as px




st.markdown("""# Hungry index App""")


# Mínimos e máximos dos nossos parâmetros

le_min, le_max = 0,120
eys_min, eys_max = 0,20
mys_min, mys_max =0.0,20.0
gnipc_min, gnipc_max =300, 90000
mmr_min, mmr_max =0,2500
abr_min, abr_max =0.0,205.0
co2_prod_min, co2_prod_max =0.0,40.0
mf_min, mf_max =0.0,100.0
rpg_min, rpg_max =-12.0,20.0
sub_region = ['Caribbean', 'Central America', 'Central Asia', 'Eastern Africa',
       'Eastern Asia', 'Eastern Europe', 'Melanesia', 'Middle Africa',
       'Northern Africa', 'Northern Europe', 'South America',
       'South-Eastern Asia', 'Southern Africa', 'Southern Asia',
       'Southern Europe', 'Western Africa', 'Western Asia']

col1, col2,col3, col4, col5 = st.columns(5)

with col1:
    mmr = st.slider("Maternal Mortality Ratio (deaths per 100,000 live births)", mmr_min, mmr_max, value = 1000)
    le = st.slider("Life Expectancy at Birth (years)", le_min, le_max, value = 68)


with col2:
    mys = st.slider("Mean Years of Schooling (years)", mys_min, mys_max, value = 7.6)
    gnipc = st.slider("Gross National Income Per Capita (2017 PPP$)", gnipc_min, gnipc_max, value = 10999)


with col3:
    abr = st.slider("Adolescent Birth Rate (births per 1,000 women ages 15-19)", abr_min, abr_max, value = 200.0)
    rpg =  st.slider("Rural population growth (annual %)", rpg_min, rpg_max, value = 0.33)


with col4:
    eys =  st.slider("Expected Years of Schooling (years)", eys_min, eys_max, value = 12)
    co2_prod = st.slider("Carbon dioxide emissions per capita (production) (tonnes)", co2_prod_min, co2_prod_max, value = 4.88)

with col5:
    mf =  st.slider("Material footprint per capita (tonnes)", mf_min, mf_max, value = 9.8)
    selected_region = st.multiselect('Select the subregion:', sub_region,default = 'South America')

url = 'https://hitw5-acslzvyr6a-rj.a.run.app/predict'

if url == 'https://hitw5-acslzvyr6a-rj.a.run.app/predict':

    #st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')
    data = dict(le=le,
                eys=eys,
                mys=mys,
                gnipc=gnipc,
                mmr=mmr,
                abr=abr,
                co2_prod=co2_prod,
                mf=mf,
                rpg=rpg,
                sub_region=selected_region
                )
    response = requests.get(url=url,params = data)
    if response.status_code == 200:
        data = response.json()

    else:
        st.error("Erro na requisição: " + str(response.status_code))

# Crie uma barra lateral
st.sidebar.title("Hunger Index")
valor_predito = data[0]
# Adicione o texto estilizado na barra lateral
st.sidebar.markdown(
    f'<p style="text-align: right; font-size: 24px; color: red;">{valor_predito}</p>',
    unsafe_allow_html=True
)
GHI_2022 = {
    'Belarus':5,'Bosnia & Herzegovina':5,'Chile':5,'China':5,'Croatia':5,'Estonia':5,'Hungary':5,'Kuwait':5,'Latvia':5,'Lithuania':5,'Montenegro':5,'North Macedonia':5,'Romania':5,'Serbia':5,'Slovak Republic':5,'Türkiye':5,'Uruguay':5,'Costa Rica':5.3,'United Arab Emirates':5.3,'Brazil':5.4,'Uzbekistan':5.6,'Georgia':5.7,'Mongolia':5.7,'Bulgaria':5.9,'Kazakhstan':5.9,'Tunisia':6.1,'Albania':6.2,'Russian Federation':6.4,'Iran (Islamic Republic of)':6.5,'Saudi Arabia':6.7,'Argentina':6.8,'Algeria':6.9,'Armenia':6.9,'Moldova':6.9,'Jamaica':7,'Azerbaijan':7.5,'Ukraine':7.5,'Colombia':7.6,'Peru':7.6,'Kyrgyz Republic':7.8,'Paraguay':8,'Mexico':8.1,'Panama':8.1,'El Salvador':8.4,'Dominican Republic':8.8,'Trinidad & Tobago':9,'Fiji':9.2,'Morocco':9.2,'Turkmenistan':9.5,'Suriname':10.2,'Guyana':10.4,'Lebanon':10.5,'Jordan':10.6,'Cabo Verde':11.8,'Viet Nam':11.9,'Thailand':12,'Egypt':12.3,'Malaysia':12.5,'South Africa':12.9,'Oman':13,'Bolivia (Plurinational State of)':13.2,'Honduras':13.4,'Mauritius':13.4,'Nicaragua':13.6,'Sri Lanka':13.6,'Iraq':13.7,'Ghana':13.9,'Tajikistan':13.9,'Philippines':14.8,'Ecuador':15.2,'Myanmar':15.6,'Senegal':15.6,'Eswatini':16.3,'Côte dIvoire':16.8,'Cambodia':17.1,'Gabon':17.2,'Indonesia':17.9,'Namibia':18.7,'Guatemala':18.8,'Cameroon':18.9,'Nepal':19.1,'Lao PDR':19.2,'Solomon Islands':19.4,'Bangladesh':19.6,'Venezuela (Bolivarian Republic of)':19.9,'Botswana':20,'Gambia':20.7,'Malawi':20.7,'Mauritania':20.7,'Djibouti':21.5,'Benin':21.7,'Togo':22.8,'Mali':23.2,'Kenya':23.5,'Tanzania (United Republic of)':23.6,'Burkina Faso':24.5,'Korea (DPR)':24.9,'Angola':25.9,'Pakistan':26.1,'Papua New Guinea':26.5,'Comoros':26.9,'Rwanda':27.2,'Nigeria':27.3,'Ethiopia':27.6,'Congo (Republic of)':28.1,'Sudan':28.8,'India':29.1,'Zambia':29.3,'Afghanistan':29.9,'Timor-Leste':30.6,'Guinea-Bissau':30.8,'Sierra Leone':31.5,'Lesotho':32.4,'Liberia':32.4,'Niger':32.6,'Haiti':32.7,'Guinea, Mozambique, Uganda, and Zimbabwe':34.9,'Chad':37.2,'Dem. Rep. of the Congo':37.8,'Madagascar':38.7,'Central African Rep.':44,'Yemen':45.1
}

GHI_2022['new']= float(valor_predito)

# Converter o dicionário em DataFrame
df = pd.DataFrame.from_dict(GHI_2022, orient='index', columns=['GHI'])
valores_classificados = sorted(list(GHI_2022.values()))
valores_classificados.append(GHI_2022['new'])

# Encontrar a posição do valor predito na lista classificada
posicao = valores_classificados.index(GHI_2022['new']) + 1

# Exibir a posição em ordem crescente do valor predito
st.write(f"Your position is {posicao}°")


fig = px.choropleth(df, locations=df.index, locationmode="country names", color='GHI',
                    color_continuous_scale='OrRd')

# Configurar o layout do mapa
fig.update_layout(
    title_text='Global Hunger Index',
    geo=dict(
        showcoastlines=True,
        showland=True,
        showcountries=True,
        landcolor='rgb(217, 217, 217)',
        coastlinecolor='rgb(255, 255, 255)',
        countrycolor='rgb(255, 255, 255)'
    )
)
st.plotly_chart(fig, use_container_width=True)
