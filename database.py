import sys
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import pyodbc 

def main(word):
    # Aquí puedes agregar la lógica para manejar la palabra, por ejemplo, guardarla en una base de datos
    print(f"Received word: {word}")
    print(search_news(word))
    #df_news=search_news(word)
    #load_df(df_news)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        word = sys.argv[1]
        main(word)
    else:
        print("No word provided")


def search_news(searched_word):
    #searched_word='debate'
    url = 'https://content.guardianapis.com/search?q='+searched_word+'&api-key=466c799b-326e-42d0-8131-7d5d474fb9fd'
    response = requests.get(url)
    data=response.json()
    results = data.get('response', {}).get('results', [])

    titles = []
    urls = []
    sections = []
    publication_dates = []


    contador =0
    for article in results:
        if contador <100:
            titles.append(article.get('webTitle'))
            urls.append(article.get('webUrl'))
            sections.append(article.get('sectionName'))
            publication_dates.append(article.get('webPublicationDate'))
            contador +=1

    df = pd.DataFrame({
        'Title': titles,
        'URL': urls,
        'Section': sections,
        'Publication Date': publication_dates
    })
    df['Publication Date'] = pd.to_datetime(df['Publication Date']).dt.date
    return(df)

def load_df(df):
    server = 'database-1.c7gw8mggu831.us-east-2.rds.amazonaws.com'
    database = 'worley'
    username = 'admin'
    password = 'admin123'


    # Cadena de conexión
    connection_string = (
        f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
        #f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server'
    )

    # Crear el engine
    engine = create_engine(connection_string)
    df.to_sql('guardian_news', engine, if_exists='replace', index=False)