import requests
import pandas as pd
from prefect import task, Flow
from sqlalchemy import create_engine
from prefect.schedules.schedules import IntervalSchedule
from datetime import timedelta

@task
def extract_data():
    response = requests.get("https://dados.mobilidade.rio/gps/brt")
    content = response.json()
    data = content["veiculos"]
    return data

# schedule data extraction to run every minute
schedule = IntervalSchedule(interval=timedelta(minutes=1))

@task
def save_to_csv(data):
    df = pd.json_normalize(data)
    df.to_csv('brt_data.csv', mode='a', header=False, index=False)

@task
def load_to_postgres():
    engine = create_engine('postgresql://docker:secreta@localhost:5432/brt_data')
    new_columns = ['codigo', 'placa', 'linha', 'latitude', 'longitude', 'dataHora',
       'velocidade', 'id_migracao_trajeto', 'sentido', 'trajeto', 'hodometro',
       'direcao', 'ignicao']
    df = pd.read_csv('brt_data.csv', names=new_columns, header=None)
    df.to_sql('gps_brt', engine, if_exists='append', index=False)

with Flow("BRT Data Flow", schedule=schedule) as flow:
    data = extract_data()
    csv_task = save_to_csv(data)
    load_task = load_to_postgres()

    # define task dependency
    load_task.set_upstream(csv_task)

if __name__ == "__main__":
    flow.run()