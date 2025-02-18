import requests
import pandas as pd
from prefect import task, Flow
from sqlalchemy import create_engine

@task
def extract_data():
    response = requests.get("https://dados.mobilidade.rio/gps/brt")
    data = response.json()
    return data

@task
def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('brt_data.csv', mode='a', header=False, index=False)

@task
def load_to_postgres():
    engine = create_engine('postgresql://docker:secreta@localhost:5432/brt_data')
    df = pd.read_csv('brt_data.csv')
    df.to_sql('gps_brt', engine, if_exists='append', index=False)

with Flow("BRT Data Flow") as flow:
    data = extract_data()
    save_to_csv(data)
    load_to_postgres()

if __name__ == "__main__":
    flow.run()


