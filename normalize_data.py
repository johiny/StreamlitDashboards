import pandas as pd

cf_data = pd.read_csv("respuestas_encuesta.csv").drop(['Unnamed: 0', 'Marca temporal'], axis=1)
cf_data[['País', 'Color favorito', 'Género musical favorito']] = cf_data[['País', 'Color favorito', 'Género musical favorito']].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.capitalize().str.strip())
print(cf_data)
cf_data.to_csv('respuestas_encuesta.csv')