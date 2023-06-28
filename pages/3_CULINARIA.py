#------------------------------------------------------------------------------
#                    PA nº 1 - Dashboard Projeto Fome Zero
#
# Curso . . .: Análise de dados com Python
# Instituição: COMUNIDADE DS
# Arquivo . .: 3_CULINARIA.PY
# Finalidade : Página da Visão Culinária
#                                                              Start: 25.6.2023
#                  manoelmendonca@hotmail.com                   Last: 27.6.2023
#------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px
import inflection

#from dbutil import dbutil

#--------- CLASSE: PÁGINA-3 'VISÃO CULINÁRIA' ---------------------------------

class app_culinarias():

    #..... CONSTRUCTOR
    def __init__(self) -> None:
        self.dfculinarias: pd.core.frame.DataFrame = None
        self.util: dbutil = None
        self.SliderQuantidade = 0
        return

    #..... BARRA LATERAL
    def BarraLateral(self) -> None:

        #..... ICONE+TÍTULO DO APP
        image_path = 'Restaurant_Icon.png'
        image = Image.open( image_path )
        st.sidebar.image( image, width=60 )

        #..... FILTROS: por países, por qtd.restaurantes, e por culinárias
        st.sidebar.markdown( '## Filtros' )
        st.sidebar.write('Escolha os **PAÍSES** cujas **CIDADES** deseja visualizar:')

        # Radio Button - todos ou só alguns países...
        qty_countries = st.sidebar.radio("", ('Os principais','Todos'), label_visibility="collapsed")
        if qty_countries == 'Todos':
            default_countries = self.util.get_all_countries()
        else:
            default_countries = self.util.countries_with_more_restaurants( 6 )

        #..... Filtro-1: por países
        the_countries = self.util.get_all_countries()
        country_options = st.sidebar.multiselect(
            label='Seleção de países:',
            options=the_countries,
            default=default_countries )
        # Obtém dataframe filtrado
        self.dfculinarias = self.util.get_items_with_these_countries(country_options)

        #..... Filtro-2: por quantidade de restaurantes

        #st.sidebar.markdown( '## Selecione a quantidade de Restaurantes para tabelar:' )
        val_slider = st.sidebar.slider(
            '## Selecione a quantidade de Restaurantes para tabelar:',
            value=10, min_value=1, max_value=20, format='%d' )
        st.sidebar.markdown("""---""")
        self.SliderQuantidade = val_slider

        #..... Filtro-3: por tipos de culinárias
        st.sidebar.write('Escolha as **CULINÁRIAS** que deseja visualizar:')

        # Radio Button - todos ou só alguns países...
        qty_cuisines = st.sidebar.radio("", ('As principais','Todas'), label_visibility="collapsed")
        if qty_cuisines == 'Todas':
            default_cuisines = self.util.get_all_cuisines()
        else:
            default_cuisines = self.util.cuisines_with_more_restaurants( 12, self.util.dtframe )

        the_cuisines = self.util.get_all_cuisines()
        cuisine_options = st.sidebar.multiselect(
            label='Seleção de Culinárias:',
            options=the_cuisines,
            default=default_cuisines )
        # Obtém dataframe filtrado
        self.dfculinarias = self.util.get_items_with_these_cuisines(self.dfculinarias, cuisine_options)

        #..... Assinatura do autor
        st.sidebar.write('')
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
                st.write('# Visão Culinária')

        #..... Container-1: 5 boxes - melhores restaurantes dos principais tipos culinários
        st.divider()
        with st.container():
            st.write('### Melhores Restaurantes por Tipo Culinário')
            cuisines = self.util.cuisines_with_more_restaurants( 5, self.dfculinarias  )
            col1, col2, col3, col4, col5 = st.columns( 5 )
            with col1:
                st.write('Tipo: **' + cuisines[0] + '**')
                df2 = self.util.best_restaurants_from_cuisine(cuisines[0],self.dfculinarias)
                st.write('#### '+df2.loc[0,'restaurant_name'])
                st.write('#### '+str(df2.loc[0,'aggregate_rating']))

            with col2:
                st.write('Tipo: **' + cuisines[1] + '**')
                df2 = self.util.best_restaurants_from_cuisine(cuisines[1],self.dfculinarias)
                st.write('#### '+df2.loc[0,'restaurant_name'])
                st.write('#### '+str(df2.loc[0,'aggregate_rating']))

            with col3:
                st.write('Tipo: **' + cuisines[2] + '**')
                df2 = self.util.best_restaurants_from_cuisine(cuisines[2],self.dfculinarias)
                st.write('#### '+df2.loc[0,'restaurant_name'])
                st.write('#### '+str(df2.loc[0,'aggregate_rating']))

            with col4:
                st.write('Tipo: **' + cuisines[3] + '**')
                df2 = self.util.best_restaurants_from_cuisine(cuisines[3],self.dfculinarias)
                st.write('#### '+df2.loc[0,'restaurant_name'])
                st.write('#### '+str(df2.loc[0,'aggregate_rating']))

            with col5:
                st.write('Tipo: **' + cuisines[4] + '**')
                df2 = self.util.best_restaurants_from_cuisine(cuisines[4],self.dfculinarias)
                st.write('#### '+df2.loc[0,'restaurant_name'])
                st.write('#### '+str(df2.loc[0,'aggregate_rating']))

        #..... Container-2: tabela - Top-10 restaurantes
        st.divider()
        with st.container():
            st.write('### Restaurantes Melhor Avaliados')
            df2 = self.util.best_restaurants(self.dfculinarias)
            st.write( df2.head(self.SliderQuantidade) )

        #..... Gráfico-3 e 4: 2 histogramas postos lateralmente, a saber:
        #                     h.1 - Top-10 melhores tipos de culinárias
        #                     h.2 - Bottom-10 piores tipos de culinárias
        st.divider()
        with st.container():
            col1, col2 = st.columns( 2 )
            with col1:
                st.write('### Melhores Culinárias')
                df2 = self.util.best_cuisines( False, self.dfculinarias )
                df2.columns = ['Tipo de Culinária','Avaliação Média']
                fig = px.bar( df2.head(self.SliderQuantidade), x='Tipo de Culinária', y='Avaliação Média', text_auto=True )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.write('### Piores Culinárias')
                df2 = self.util.best_cuisines( True, self.dfculinarias )
                df2.columns = ['Tipo de Culinária','Avaliação Média']
                fig = px.bar( df2.head(self.SliderQuantidade), x='Tipo de Culinária', y='Avaliação Média', text_auto=True )
                st.plotly_chart(fig, use_container_width=True)

        return


#--------- CLASSE: FUNÇÕES DE APOIO PARA ACESSO AOS DADOS (arq: "dbutil.py") --
class dbutil():

    #----- INITIAL METHODS: CONSTRUCTOR, DISTRUCTOR, LOADING DATA -------------
    #..... CONSTRUCTOR
    def __init__(self) -> None:
        self.dtframe = None
        # CODE kindly supplied in the assignment statement
        self.COUNTRIES = {
            1: "India",
            14: "Australia",
            30: "Brazil",
            37: "Canada",
            94: "Indonesia",
            148: "New Zealand",
            162: "Philippines",
            166: "Qatar",
            184: "Singapure",
            189: "South Africa",
            191: "Sri Lanka",
            208: "Turkey",
            214: "United Arab Emirates",
            215: "England",
            216: "United States of America",
        }
        self.COLORS = {
            "3F7E00": "darkgreen",    #  4161024
            "5BA829": "green",        #  6006825
            "9ACD32": "lightgreen",   # 10145074
            "CBCBC8": "darkred",      # 13355976
            "CDD614": "orange",       # 13489684
            "FFBA00": "red",          # 16759296
            "FF7800": "darkred",      # 16742400
        }
        return

    #..... LOAD DATAFRAME
    def LoadDataframe(self, inCSVfile) -> None:
        self.dtframe = pd.read_csv( inCSVfile )
        return

    #----- CLEANSING METHODS, TO ADJUST DATA ----------------------------------

    #..... Perform the main general cleansing operations (JUST CALL THIS ONE)
    def GeneralCleansing(self) -> pd.core.frame.DataFrame:

        # First op: rename columns
        self.rename_columns()

        # Remove duplicated restaurant regs
        self.dtframe.drop_duplicates(subset=['restaurant_id'], inplace=True)

        # Remove 'switch_to_order_menu' column: not needed
        self.dtframe.drop( columns=['switch_to_order_menu'] )

        # Eliminate white spaces at beginning & ending
        self.StripColumns()

        # Create 'UniqueCuisine' column
        self.CreateUniqueCuisine()

        return self.dtframe

    #..... Apply strip() command to some columns.
    def StripColumns(self) -> None:
        self.dtframe['restaurant_name'] = self.dtframe['restaurant_name'].str.strip()
        self.dtframe['city'] = self.dtframe['city'].str.strip()
        self.dtframe['locality'] = self.dtframe['locality'].str.strip()
        self.dtframe['locality_verbose'] = self.dtframe['locality_verbose'].str.strip()
        return

    #..... Create column to receive the first type of Cuisine shown in 'Cuisines' column
    def CreateUniqueCuisine(self) -> None:
        #
        # When running command [ dtframe.isna().sum() ] to discover number of NAN's...
        # ...we noticed that 'Cuisines' column has 13. Other columns do not have it.
        # Solution: when 'Cuisines' = nan, make 'UniqueCuisine' = ""
        #
        self.dtframe['unique_cuisine'] = ( self.dtframe.loc[:, 'cuisines']
                                  .apply(lambda x: x.split(",")[0] if isinstance(x, str) else "") )
        return

    #..... Adjust column names, extract white spaces, etc
    def rename_columns( self ) -> pd.core.frame.DataFrame:
    
        # Kindly offered by the teacher :)
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(self.dtframe.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        self.dtframe.columns = cols_new

        # create 'country_name' column
        self.dtframe['country_name'] = ( self.dtframe.loc[:, 'country_code']
                                             .apply(lambda x: self.country_name(x)) )

        return self.dtframe

    #..... CODE kindly supplied in the assignment statement
    def color_name(self, color_code):
        return self.COLORS[color_code]

    #..... CODE kindly supplied in the assignment statement
    def country_name(self, country_id):
        return self.COUNTRIES[country_id]

    #..... CODE kindly supplied in the assignment statement
    def create_price_tye(self, price_range):
        # Price range . . . . : int, values = [ 1, 2, 3, 4 ]
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"

    #..... Create column to receive the price range as text
    def create_price_range_txt(self) -> None:
        #
        # Force a column with the string info.
        # Price range . . . . : int, values = [ 1, 2, 3, 4 ]
        #
        self.dtframe['price_range_txt'] = ( self.dtframe.loc[:, 'price_range']
                                  .apply(lambda x: self.create_price_tye(x) ) )
        return

    #----- COUNTRIES DATA HANDLING METHODS ------------------------------------

    def get_all_countries(self) -> list:
        all_countries = self.dtframe['country_name'].unique().tolist()
        return sorted(all_countries)

    def countries_with_more_restaurants(self, NumCountries: int) -> list:
        if NumCountries < 1:
            return []

        colunas = ['country_name','restaurant_id']
        df1 = ( self.dtframe.loc[:, colunas]
                            .groupby('country_name').count()
                            .sort_values(by=['restaurant_id'], ascending=False)
                            .reset_index() )
        aux = df1.loc[0:(NumCountries-1), 'country_name']
        the_countries = aux.tolist()
        return the_countries

    def get_items_with_these_countries(
            self, 
            list_of_countries: list) -> pd.core.frame.DataFrame:
        #
        # From the whole base ('self.dtframe'), extract lines that match 'list_of_countries'
        #
        lines = ( self.dtframe.loc[:, 'country_name']
                              .apply( lambda x: any(country in x for country in list_of_countries) ) )
        df = self.dtframe.loc[lines, :].copy().reset_index()
        return df

    def qty_restaurants_per_country(self, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        # Quantidade de restaurantes em cada país
        colunas = ['country_name','restaurant_id']
        df = ( inDF.loc[:, colunas]
                   .groupby('country_name').count()
                   .sort_values(by=['restaurant_id'], ascending=False)
                   .reset_index() )
        return df

    def qty_cities_per_country(self, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        colunas = ['country_name','city']
        df = ( inDF.loc[:, colunas]
                    .groupby('country_name').nunique()
                    .sort_values(by=['city'], ascending=False)
                    .reset_index() )
        return df
    
    def mean_rating_per_country(self, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        colunas = ['country_name','votes']
        df = ( inDF.loc[:, colunas]
                    .groupby('country_name').mean()
                    .sort_values(by=['votes'] , ascending=False )
                    .reset_index() )
        df['votes'] = df.loc[:,'votes'].apply( lambda x: round(x, 0) )
        return df

    def mean_costfor2_per_country(self, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        colunas = ['country_code','country_name','average_cost_for_two']
        df = ( inDF.loc[:, colunas]
                   .groupby(['country_code','country_name']).mean()
                   .sort_values('average_cost_for_two', ascending=False)
                   .reset_index() )
        df['average_cost_for_two'] = df.loc[:,'average_cost_for_two'].apply( lambda x: round(x, 1) )
        return df

    #----- CUISINES DATA HANDLING METHODS -------------------------------------

    def get_all_cuisines(self) -> list:
        linhas = self.dtframe['unique_cuisine'] != ''
        df2 = self.dtframe.loc[linhas, :].copy()
        all_items = df2['unique_cuisine'].unique().tolist()
        return sorted(all_items)

    def cuisines_with_more_restaurants(self, NumCuisines: int, inDF: pd.core.frame.DataFrame) -> list:
        if NumCuisines < 1:
            return []

        colunas = ['unique_cuisine','restaurant_id']
        df1 = ( inDF.loc[:, colunas]
                    .groupby('unique_cuisine').count()
                    .sort_values(by=['restaurant_id'], ascending=False)
                    .reset_index() )
        aux = df1.loc[0:(NumCuisines-1), 'unique_cuisine']
        the_countries = aux.tolist()
        return the_countries

    def get_items_with_these_cuisines(self, 
                                      inDF: pd.core.frame.DataFrame, 
                                      list_of_cuisines: list) -> pd.core.frame.DataFrame:
        #
        # From the input base ('inDF'), extract lines that match 'list_of_cuisines'
        #
        lines = ( inDF.loc[:, 'unique_cuisine']
                              .apply( lambda x: any(cuizn in x for cuizn in list_of_cuisines) ) )
        df = inDF.loc[lines, :].copy().reset_index()
        return df

    def best_restaurants_from_cuisine(self, cuisine:str, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        # Select all regs of the 'cuisine'
        colunas = ['restaurant_id','restaurant_name','unique_cuisine','aggregate_rating']
        linhas = (inDF['unique_cuisine']==cuisine)
        df2 = inDF.loc[linhas, colunas].copy()
        # Find the best rating
        df3 = df2.sort_values(by='aggregate_rating', ascending=False).reset_index()
        max_rating = df3.loc[0, 'aggregate_rating']
        # Get the best ranked restaurants
        linhas = df3['aggregate_rating']==max_rating
        df4 = df3.loc[linhas,:].sort_values(by='restaurant_id').reset_index()
        return df4

    def best_restaurants(self, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        colunas = ['restaurant_id','restaurant_name','country_name','city','unique_cuisine','aggregate_rating']
        df3 = inDF.loc[:,colunas].copy()
        df3['restaurant_id'] = -df3['restaurant_id']
        df4 = ( df3.loc[:, :]
                   .sort_values(by=['aggregate_rating','restaurant_id'], ascending=False)
                   .reset_index() )
        df4['restaurant_id'] = -df4['restaurant_id']
        return df4

    def best_cuisines(self, ascending_order: bool, inDF: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        colunas = ['unique_cuisine','aggregate_rating']
        df = ( inDF.loc[:, colunas]
                    .groupby('unique_cuisine').mean()
                    .sort_values(by='aggregate_rating', ascending=ascending_order)
                    .reset_index() )
        df['aggregate_rating'] = df.loc[:,'aggregate_rating'].apply( lambda x: round(x, 1) )
        return df


#--------- MAIN HOME PROCEDURE ------------------------------------------------
def main():
    st.set_page_config(
        page_title="Culinárias",
        page_icon="🫖",
        layout='wide'
    )

    MyCSV = 'http://menezes.mendonca.nom.br/datasets/zomato.csv'
    util = dbutil()
    util.LoadDataframe( MyCSV )
    util.GeneralCleansing()         # clean & adjust data

    #..... Cria a Home e inclui BarraLateral e PáginaPrincipal
    HomePage = app_culinarias()
    HomePage.util = util
    HomePage.BarraLateral()
    HomePage.MainPage()

    return

#--------- START ME UP --------------------------------------------------------
main()
