import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide")
st.title("Codigo Facilito - Data Science - 2022")

cf_data = pd.read_csv("respuestas_encuesta.csv")
cf_data["Fecha de inicio en data"] =  pd.to_datetime(cf_data["Fecha de inicio en data"], dayfirst=True)
mini_chart_1 = alt.Chart(cf_data).mark_bar().encode(
    x='País', 
    y=alt.Y('count()', axis=alt.Axis(format='c', title='Numero de estudiantes')),
    tooltip=[alt.Tooltip('País'), alt.Tooltip('count()', title='Numero de Estudiantes')]
    )

base = alt.Chart(cf_data).encode(
    theta=alt.Theta("count(Rango de edad)", stack=True),
    radius=alt.Radius("count(Rango de edad)", scale=alt.Scale(type="sqrt", zero=True, rangeMin=50)),
    color="Rango de edad",
    tooltip=[alt.Tooltip('Rango de edad'), alt.Tooltip('count()', title='Numero de Estudiantes')]
)
c1 = base.mark_arc(innerRadius=40, stroke='#0E1117')
c2 = base.mark_text(radiusOffset=30).encode(text="Rango de edad")

mini_chart_2 = c1 + c2

mini_chart_3 = alt.Chart(cf_data).mark_bar().encode(
    x=alt.X('sum(Sistema operativo que usas)', title='Numero de usuarios', axis=alt.Axis(labels=False)),
    y=alt.Y('count()', title=''),
    color=alt.Color('Sistema operativo que usas',title='Sistema operativo utilizado'),
    order=alt.Order(
      # Sort the segments of the bars by this field
      'Sistema operativo que usas',
      sort='ascending'
    ),
    tooltip=[alt.Tooltip('Sistema operativo que usas', title='Sistema Operativo'), alt.Tooltip('count()', title='Numero de Usuarios')]
)

mini_chart_4 = alt.Chart(cf_data).mark_boxplot(extent='min-max', color='green', size=100).encode(
    x=alt.X('Fecha de inicio en data:T', axis=alt.Axis(format="%Y %B"), title='Inicio en Data Science'),
    y=alt.Y('y:O', title=None, axis=alt.Axis(labels=False)),
    # tooltip=[alt.Tooltip('min(Fecha de inicio en data)', title='Inicio mas reciente'), alt.Tooltip('max(Fecha de inicio en data)', title='Inicio mas antiguo'), alt.Tooltip('mean(Fecha de inicio en data)', title='Inicio promedio')]
    ).properties(height=360)
#isotype chart
big_chart_1 = alt.Chart(cf_data).mark_image().encode(
    alt.X('x:O', title='Numero de estudiantes', axis=alt.Axis(labelAngle=0)),
    alt.Y('Objetivo en data:N'),
    url=alt.condition(
        alt.datum['Género'] == 'Masculino',
        alt.value('https://cdn-icons-png.flaticon.com/512/1488/1488581.png'),
        alt.value('https://cdn-icons-png.flaticon.com/512/1508/1508880.png')
    ),
    tooltip=[alt.Tooltip('Género')]
).transform_window(
    x='rank()',
    groupby=['Objetivo en data']
).properties(height=400)

big_chart_2 = alt.Chart(cf_data).mark_circle(size=400).encode(
    alt.X('x:O', axis=alt.Axis(labels=False), title=None),
    alt.Y('Género musical favorito'),
    color='Objetivo en data',
    tooltip=[alt.Tooltip('Género musical favorito'), alt.Tooltip('Objetivo en data')]
).transform_window(
    x='rank()',
    groupby=['Género musical favorito']
).properties(height=300)

main_container = st.container()
with main_container:
    mini_container = st.container()
    with mini_container:
        col1, col2, col3 = st.columns([3, 1, 1])
        #big plots section
        col1.altair_chart(big_chart_1, use_container_width=True, theme="streamlit")
        col1.altair_chart(big_chart_2, use_container_width=True, theme="streamlit")
        #mini plots section
        col2.altair_chart(mini_chart_1, use_container_width=True, theme="streamlit")
        col3.altair_chart(mini_chart_2, use_container_width=True, theme="streamlit")
        col2.altair_chart(mini_chart_3, use_container_width=True, theme="streamlit")
        col3.altair_chart(mini_chart_4, use_container_width=True, theme="streamlit")