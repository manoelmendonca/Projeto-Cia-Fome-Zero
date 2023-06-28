#------------------------------------------------------------------------------
#                    PA nº 1 - Dashboard Projeto Fome Zero
#
# Curso . . .: Análise de dados com Python
# Instituição: COMUNIDADE DS
# Arquivo . .: HOME.PY
# Finalidade : Página de apresentação do APP
#                                                              Start: 18.6.2023
#                  manoelmendonca@hotmail.com                   Last: 27.6.2023
#------------------------------------------------------------------------------

# SOME STREAMLIT REF:
#   IMAGE . . . : https://docs.streamlit.io/library/api-reference/media/st.image
#   MARKDOWN. . : https://docs.streamlit.io/library/api-reference/text/st.markdown
#   WRITE . . . : https://docs.streamlit.io/library/api-reference/write-magic/st.write
#   MULTISELECT : https://docs.streamlit.io/library/api-reference/widgets/st.multiselect
#   DOWNLOAD. . : https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-file-streamlit
#                 https://docs.streamlit.io/library/api-reference/widgets/st.download_button
#   PLOTLY CHART: https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart


import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

from dbutil import dbutil

#--------- CLASSE: PÁGINA 'HOME' ----------------------------------------------
class app_home():

    #..... CONSTRUCTOR
    def __init__(self) -> None:
        self.dfhome: pd.core.frame.DataFrame = None
        #self.util: dbutil = None
        return

    #..... BARRA LATERAL
    def BarraLateral(self) -> None:

        #..... ICONE+TÍTULO DO APP
        image_path = 'Restaurant_Icon.png'
        image = Image.open( image_path )
        # OBS: elemento 'image' não prevê incluir texto lateral
        st.sidebar.image( image, width=80 )

        st.sidebar.markdown( '# Fome Zero' )

        #..... FILTROS
        st.sidebar.markdown( '## Filtros' )
        st.sidebar.write('Escolha os **PAÍSES** cujas **INFORMAÇÕES** deseja visualizar:')

        # Radio Button - todos ou só alguns países...
        qty_countries = st.sidebar.radio("", ('Os principais','Todos'), label_visibility="collapsed")
        if qty_countries == 'Todos':
            default_countries = self.util.get_all_countries()
        else:
            default_countries = self.util.countries_with_more_restaurants( 6 )

        # Critérios de filtragem
        the_countries = self.util.get_all_countries()
        country_options = st.sidebar.multiselect(
            label='Seleção:',
            options=the_countries,
            default=default_countries )

        # Obtém dataframe filtrado
        self.dfhome = self.util.get_items_with_these_countries(country_options)

        #..... Download Button
        st.sidebar.markdown("""---""")
        csv_file = self.dfhome.to_csv()
        txt = 'Dados tratados e com filtragem do usuário'
        if st.sidebar.download_button('Baixar dados', csv_file, None, 'text/csv', help=txt):
            st.sidebar.write( 'Download OK :thumbsup:' )

        #..... Assinatura do autor
        st.sidebar.caption('Autor.....: Manoel Mendonça - 2023')
        st.sidebar.caption(':blue[manoelmendonca@hotmail.com]')
        st.sidebar.caption('[menezes.mendonca.nom.br](http://menezes.mendonca.nom.br)')

        # fim
        return

    #..... PÁGINA PRINCIPAL
    def MainPage(self):

        #..... Título
        with st.container():
            col1, col2, col3, col4, col5 = st.columns( 5 )
            with col1:
                image_path = 'Restaurant_Icon.png'
                image = Image.open( image_path )
                st.image( image, width=160 )
            with col2:
                st.write('# Fome Zero!')

        #..... SubTítulo
        st.write( "### O melhor lugar para encontrar o seu mais novo restaurante favorito" )

        #..... Indicadores gerais de desempenho
        st.markdown("""---""")
        st.write( "#### Nossa plataforma vem alcançando as seguintes marcas:" )

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.write('**Países selecionados**')
            with col2:
                st.write('**Cidades cadastradas**')
            with col3:
                st.write('**Restaurantes cadastrados**')
            with col4:
                st.write('**Avaliações feitas na plataforma** (x 1k)')
            with col5:
                st.write('**Tipos de culinárias ofertadas**')

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                tot = len( self.dfhome['country_name'].unique() )
                st.markdown('## **'+str(tot)+'**')
            with col2:
                tot = len( self.dfhome['city'].unique() )
                st.markdown('## **'+str(tot)+'**')
            with col3:
                tot = len( self.dfhome['restaurant_name'].unique() )
                st.markdown('## **'+str(tot)+'**')
            with col4:
                df1 = self.dfhome['votes']
                tot = round( df1.sum() / 1000, 1 )
                st.markdown('## **'+str(tot)+'**')
            with col5:
                tot = len( self.dfhome['unique_cuisine'].unique() )
                st.markdown('## **'+str(tot)+'**')

        #..... MAPA MUNDI
        st.markdown("""---""")
        self.country_map()

        # FIM
        return

    #..... MAPA MUNDI
    def country_map( self ) -> None:
        colunas = ['city','aggregate_rating','rating_color','latitude','longitude']
        df2 = self.dfhome.loc[: ,colunas]
        # df3 = pontos a colocar no mapa 
        #  -->  [ city, aggregate_rating, latitude, longitude ]
        df3 = ( df2.loc[:,:].groupby(['city','aggregate_rating','rating_color'])
                            .median()
                            .reset_index() )
        # Desenhar MAPA
        CityMap = folium.Map( zoom_start=11 )

        for index, location_info in df3.iterrows():
            # Insere, um por um, os pinos no mapa.
            folium.Marker( [location_info['latitude'],
                            location_info['longitude']],
                            popup=location_info[['city','aggregate_rating']], 
                            icon=folium.Icon( color=self.util.color_name(location_info['rating_color']) ) ).add_to(CityMap)
        folium_static( CityMap, width=1024, height=600 )
        # FIM
        return

#--------- MAIN HOME PROCEDURE ------------------------------------------------
def main():
    st.set_page_config(
        page_title="Home",
        page_icon="🍴",
        layout='wide'
    )

    MyCSV = 'http://menezes.mendonca.nom.br/datasets/zomato.csv'
    util = dbutil()
    util.LoadDataframe( MyCSV )
    util.GeneralCleansing()         # clean & adjust data

    #..... Cria a Home e inclui BarraLateral e PáginaPrincipal
    HomePage = app_home()
    HomePage.util = util
    HomePage.BarraLateral()
    HomePage.MainPage()

    return

#--------- START ME UP --------------------------------------------------------
main()
