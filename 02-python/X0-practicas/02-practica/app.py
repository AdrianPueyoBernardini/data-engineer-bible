import pandas as pd
import pathlib


data = pathlib.Path(__file__).with_name("data.csv")
df = pd.read_csv(data, encoding="utf-8")


def lectura_csv():

    #Devolvemos el csv
    return df.head(30)

def media_csv():

    #Sacamos la media del csv
    return df.describe()

print(lectura_csv())
print(media_csv())