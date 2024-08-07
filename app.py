import streamlit as st
from spider import Spider
from downloader import FileDownloader
import streamlit.components as select_slider
import pandas
import base64
import time
from io import BytesIO

dia_links = [
r"https://www.dia.es/charcuteria-y-quesos/jamon-cocido-lacon-fiambres-y-mortadela/c/L2001",
r"https://www.dia.es/charcuteria-y-quesos/jamon-curado-y-paleta/c/L2004",
r"https://www.dia.es/charcuteria-y-quesos/lomo-chorizo-fuet-salchichon/c/L2005",
r"https://www.dia.es/charcuteria-y-quesos/queso-curado-semicurado-y-tierno/c/L2007",
r"https://www.dia.es/charcuteria-y-quesos/queso-fresco/c/L2008",
r"https://www.dia.es/charcuteria-y-quesos/queso-azul-y-roquefort/c/L2009",
r"https://www.dia.es/charcuteria-y-quesos/quesos-fundidos-y-cremas/c/L2010",
r"https://www.dia.es/charcuteria-y-quesos/quesos-internacionales/c/L2011",
r"https://www.dia.es/charcuteria-y-quesos/salchichas/c/L2206",
r"https://www.dia.es/charcuteria-y-quesos/foie-pate-y-sobrasada/c/L2012"
]

timestr = time.strftime("%Y%m%d-%H%M%S")

@st.cache_data
def scrapping_data(urls):
    spider = Spider()
    links = []
    for link in dia_links:
        links.extend(spider.extract_single_data(url=link))

    df = spider.extract_multiple_api_data(url_list=links)

    return df


st.set_page_config(layout="wide")
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #78ADE2;
    }
</style>
""", unsafe_allow_html=True)

def main():
    values = ["Scrapping","About"]
    st.sidebar.selectbox("Valores",values)
    st.title("Web scrapping DIA marketplace")
    with st.form(key="scrapping"):
        st.markdown("**Click the button to scrape :)**")
       
        value = st.form_submit_button("Submit request")
    if value:
        
        df = scrapping_data(urls=dia_links)
        st.success("Successfully scrapped!")
        st.dataframe(df)
        tab1,tab2,tab3 = st.tabs(["CSV","Excel","JSON"])

        with tab1:
            download = FileDownloader(df.to_csv(), file_ext=".csv").download()

        with tab2:
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            download = FileDownloader(towrite.read(), file_ext="xlsx").download_xlsx()

        with tab3:
            json_data = df.to_json(orient='records')
            download = FileDownloader(json_data, file_ext="json").download_json()


    
    
                



if __name__=="__main__":
    main()
