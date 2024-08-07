from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import re
import json

class Spider():
    def __init__(self):
        pass
    def html_to_txt(self,url,adress,headers = None,cookies = None,proxys=None,params = None):
        
        """
        This function help us to save the request in a .txt file to save the number of request
        we do in order to not being blocked.
        
        
        """
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.proxys = proxys
        self.params = params
        self.adress = adress
        
        session = HTMLSession()
    
        request = session.get(self.url)
        with open(adress,"w",encoding="UTF-8") as f:
            data = f.write(request.text)
            f.close()
            
        print(f"HTML succesfully saved in {adress}")
        return data
        
    def html_to_json(self,url,adress,headers = None,cookies = None,proxys=None,params = None):
        """
        This function help us to save the request in a .json file to save the number of request
        we do in order to not being blocked. Usually this kind of requests are done to an API.
        
        
        """
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.proxys = proxys
        self.params = params
        self.adress = adress
        
        session = HTMLSession()
    
        request = session.get(self.url)
        data = request.json()
        
        with open(self.adress,"w") as j:
            json.dump(data,j)
            
        return data
    def extract_single_api_data(self,url = None,headers = None,cookies = None,proxys=None,params = None,use_json=None,adress_json=None):
        """
        We can extract the data whether from the outcome of the html_to_json() function using the
        parameters use_json == True, adress_json and url == None or straightly do the http request
        to the API
        """
        if use_json == True and adress_json and url == None:
#             print("Let's use json!")
            with open(adress_json,"r",encoding="UTF-8") as j:
                data = json.load(j)
            
        
            
        else:
            self.url = url
            self.headers = headers
            self.cookies = cookies
            self.proxys = proxys
            self.params = params
            session = HTMLSession()

            request = session.get(self.url,self.headers,self.cookies,self.proxys,self.params)
            
            data = request.json()
            
            
        product_name = []
        price_value = []
        price_kg_value = []
        aditional_data_value = []
        sku_id = []
        data2 = data["plp_items"]
#         print(data2)
        for i in data2:

            try:
                product_name.append(i["display_name"])
                price_value.append(i["prices"]["price"])
                price_kg_value.append(i["prices"]["price_per_unit"])
                sku_id.append(i["sku_id"])
                aditional_data_value.append(i["product_info"])

            except:
                aditional_data_value.append("No data")


        data_pd = {

            "Product name" : product_name,
            "Price value" : price_value,
            "Price per kg" : price_kg_value,
            "Aditional data" : aditional_data_value,
            "SKU ID" : sku_id


        
        }
#         print(data_pd)

        df = pd.DataFrame(data_pd)
        return df
    def extract_multiple_api_data(self,url = None,headers = None,cookies = None,proxys=None,params = None,use_json=None,adress_json=None,url_list = None):
        """
        This function is diferent to extract_single_api_data() because here we don't have the option
        of getting the data from a local json file. We need to provide an url list in the parameter
        'url_list' so we can scrape all the data from every file
        
        """
        
        self.url_list = url_list
        product_name = []
        price_value = []
        price_kg_value = []
        aditional_data_value = []
        sku_id = []
        category = []
        
        for url_data in self.url_list:
            
            self.url = f"https://www.dia.es/api/v1/plp-back/reduced{url_data}"
            # print(self.url)
            self.headers = headers
            self.cookies = cookies
            self.proxys = proxys
            self.params = params
            session = HTMLSession()
            

            request = session.get(self.url)

            data = request.json()
            
        

            
            
            data2 = data["plp_items"]
    #         print(data2)
            for i in data2:

                try:
                    product_name.append(i["display_name"])
                    price_value.append(i["prices"]["price"])
                    price_kg_value.append(i["prices"]["price_per_unit"])
                    sku_id.append(i["sku_id"])
                    category.append(url_data)
                    aditional_data_value.append(i["product_info"])

                except:
                    aditional_data_value.append("No data")


        data_pd = {

            "Product name" : product_name,
            "Price value" : price_value,
            "Price per kg" : price_kg_value,
            "Aditional data" : aditional_data_value,
            "SKU ID" : sku_id,
            "Category" : category



        }
#         print(data_pd)

        df = pd.DataFrame(data_pd)
        def split_value(x):
            value = x.split("/")[2].replace("-"," ").capitalize()
            return value

        df["Category"] = df["Category"].apply(split_value)
        return df
            
        
    def extract_single_data(self,url = None,headers = None,cookies = None,proxys=None,params = None,use_txt=None,adress_txt=None):
        #Extracting compiled urls-----------------------------------------------------
        
        """
        We can extract the data whether from the outcome of the html_to_txt() function using the
        parameters use_txt == True, adress_txt and url == None or straightly do the http request
        to the web page
        """
        if use_txt == True and adress_txt and url == None:
            print("Let's use txt!")
            with open(adress_txt,"r",encoding="UTF-8") as f:
                request = f.read()
                f.close()
            bs = BeautifulSoup(request,"lxml")
            
        else:
            
            self.url = url
            self.headers = headers
            self.cookies = cookies
            self.proxys = proxys
            self.params = params
            session = HTMLSession()

            request = session.get(self.url)
            bs = BeautifulSoup(request.text,"lxml")

        
        self.bs = bs
#         Change class and label-------------------------------------------------------------
        soup = bs.find_all("li",class_="product-card-list__item-container")

#         Defining variables to create the dictionary and afterwards the dataframe-----------
#         print(request.text)  
        product_name = []
        price_value = []
        price_kg_value = []
        aditional_data_value = []
#         aditional_data_value = []
        x = bs.find_all("a",class_="pagination-list__item")
        return [i.attrs["href"] for i in x]
#     Extract simple and single data-------------------------------------------------------
#             print()
#         for text in soup:
#             try:
# #                 print(text)
            
#                 product_name = text.find("p",class_="search-product-card__product-name").text
#                 print(product_name)
#             except:
#                 product_name1 = text.text
#                 print(product_name1)
                
            
#             price_value = search_second_number(text.find("div",class_="flex flex-wrap justify-start items-center lh-title mb1").text)
#             price_kg_value = search_review(text.find("div",class_="flex items-center mt2").text)
#             aditional_data_value = ""
            
#             try:
                
#                 aditional_data_value = text.find("div",class_="flex items-center mt2 mb1").text
#                 if aditional_data_value:
#                     aditional_data_value = aditional_data_value
#                 else:
#                     aditional_data_value = "No value"
                    
                    
#             except:
#                 if len(aditional_data_value) == 0:
#                     w_save = "No value"
                    
            
#             Stablishing dictionary's values for Dataframe-------------------------------

#             item_description_value.append(item_description)
#             price_value.append(price)
#             rating_value.append(rating)
#             w_save_value.append(w_save)
#             aditional_data_value.append(aditional_data)
#             print(title_value)
#         Creating Pandas Dataframe
    
#         data = {
    
#             "Producto name" : product_name
# #             "Price" : price_value,
# #             "Rating" : rating_value,
# # #             "W+": w_save_value,
# # #             "Aditional info" : aditional_data_value
       
#         }

#         df = pd.DataFrame(data)
        
#         self.df = df
     
#         return df
        
            
#         Function finished
        
            
    def extract_multiple_pages(self):
        """
        We use this function in combination with the extract_single_data() if we are sure we have more than
        one page to scrape
        
        """
        bs_page = self.bs
        soup = bs_page.find("li",class_="next")
        if soup.a.text == "next":
            url1 = f"https://books.toscrape.com/{soup.a.attrs['href']}"
        else:
            return "Ningún enlace ha sido encontrado"

        session = HTMLSession()
        request = session.get(url1)
        bs = BeautifulSoup(request.text,"lxml")
        soup = bs.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
#         Loop straight to labels(a,h1,h2,div) or go to the class
        title_value = []
        price_value = []
        stars_value = []
        available_value = []
        
        for text in soup:
            title = text.h3.a.text
            price = text.find("p",class_="price_color").text.replace("Â£","")
            stars = text.p["class"][1]
            available = text.find("p",class_="instock availability").text.strip()
            
            title_value.append(title)
            price_value.append(price)
            stars_value.append(stars)
            available_value.append(available)
#         Creating Pandas Dataframe
        
        data = {
            
                "Title" : title_value,
                "Price" : price_value,
                "Stars" : stars_value,
                "Available" : available_value

                    }

                    
                    
        df1 = pd.DataFrame(data)
        
        dfx1 = pd.concat([self.df,df1])
        
        
            
        try:
#             Stableshing the next link value
            value_link = bs.find("li",class_="next")     
            new_link = f"https://books.toscrape.com/{value.a.attrs['href']}"
        except:
            pass
#       Loop throught all the webpages
        title1_value = []
        price1_value = []
        stars1_value = []
        available1_value = []
            
        while 1:
            try:


                if value_link.a.text == "next":
                    url1 = f"https://books.toscrape.com/catalogue/{value_link.a.attrs['href']}"
                    print(url1)
                    session = HTMLSession()
                    request = session.get(url1)
                    
        


                bs = BeautifulSoup(request.text,"lxml")
                soup = bs.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        #         Loop straight to labels(a,h1,h2,div) or go to the class
             
                for text in soup:
                    title = text.h3.a.text
                    price = text.find("p",class_="price_color").text.replace("Â£","")
                    stars = text.p["class"][1]
                    available = text.find("p",class_="instock availability").text.strip()

                    title1_value.append(title)
                    price1_value.append(price)
                    stars1_value.append(stars)
                    available1_value.append(available)
#                 Getting the link to the next webpage    
                value_link = bs.find("li",class_="next")
              
            except:
                print(value_link)
                if len(title1_value) > 0:
                    data2 = {

                        "Title" : title1_value,
                        "Price" : price1_value,
                        "Stars" : stars1_value,
                        "Available" : available1_value

                            }
                    df2 = pd.DataFrame(data2)
                    dfx2 = pd.concat([dfx1,df2])
                    print("elif")
                    return dfx2
                else:
                    print("else")
                    return dfx1
                break
    def from_dataframe_to_data(self,df,extension,adress):
        
        """
        This function let us to save the data in the format we see fit.
        We can save in csv,xlsx,sql,json or parquet
        
        """
        self.extension = extension
        self.df = df
        self.adress = adress
        if self.extension == "csv":
            return self.df.to_csv(self.adress,index = False)
        elif self.extension == "xlsx":
            return self.df.to_excel(self.adress,index = False)
        elif self.extension == "sql":
            return self.df.to_sql(self.adress,index = False)
        elif self.extension == "json":
            return self.df.to_json(self.adress,index = False)
        elif self.extension == "parquet":
            return self.df.to_parquet(self.adress,index = False)
        
    
        
    

# if __name__=="__main__":
#     spider = Spider()
    
#     df = spider.run_javascript_multidata_extract()
#     print(df)

# spider = Spider()


# dia_links = [
# r"https://www.dia.es/charcuteria-y-quesos/jamon-cocido-lacon-fiambres-y-mortadela/c/L2001",
# r"https://www.dia.es/charcuteria-y-quesos/jamon-curado-y-paleta/c/L2004",
# r"https://www.dia.es/charcuteria-y-quesos/lomo-chorizo-fuet-salchichon/c/L2005",
# r"https://www.dia.es/charcuteria-y-quesos/queso-curado-semicurado-y-tierno/c/L2007",
# r"https://www.dia.es/charcuteria-y-quesos/queso-fresco/c/L2008",
# r"https://www.dia.es/charcuteria-y-quesos/queso-azul-y-roquefort/c/L2009",
# r"https://www.dia.es/charcuteria-y-quesos/quesos-fundidos-y-cremas/c/L2010",
# r"https://www.dia.es/charcuteria-y-quesos/quesos-internacionales/c/L2011",
# r"https://www.dia.es/charcuteria-y-quesos/salchichas/c/L2206",
# r"https://www.dia.es/charcuteria-y-quesos/foie-pate-y-sobrasada/c/L2012"
# ]

# links = []
# for link in dia_links:
#     links.extend(spider.extract_single_data(url=link))

# df = spider.extract_multiple_api_data(url_list=links)

# df