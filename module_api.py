import datetime
from typing import List
from sqlalchemy import Column, Integer, Float, DateTime
import pandas as pd
import pytz
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_USER, DB_HOST, DB_PORT, DB_PASS, DB_NAME

from models import data_respondent, Audience

app = FastAPI(title='OKKAM',
              description=f'подключена БД - {DB_HOST}:{DB_PORT}')

# Создаем подключение к базе данных

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Создаем базовый класс модели
Base = declarative_base()
Base.metadata.create_all(engine)
# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()


# Определяем модель таблицы
class Respondent(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    respondent = Column(Integer)
    sex = Column(Integer)
    age = Column(Integer)
    weight = Column(Float)


def str_date_to_date(date_string):
    # Преобразование строки в объект datetime

    date_string = str(date_string).replace('.0', '')
    date = datetime.datetime.strptime(date_string, "%Y%m%d")

    # Добавление текущего времени UTC
    date_with_utc = date.replace(tzinfo=pytz.UTC)
    print(date_with_utc)
    return date_with_utc


# Создаем сессию для работы с базой данных

# Считываем данные из CSV файла
data = pd.read_csv('data.csv', header=0, sep=';')
data = data.set_axis(["id", 'date', 'respondent', 'sex', 'age', 'weight'], axis=1, )
# Сохраняем изменения в базе данных
data.to_sql('data', engine, if_exists='append', index=False)
session.commit()


def process_sql_condition(condition):
    """
    :param condition:  - запрос после слов WHERE, например: data.age BETWEEN 18 AND 35
    :return: таблица
    """

    # Формируем выражение SQLAlchemy из текстового условия SQL
    query = session.query(data_respondent).filter(text(condition))

    # Выполняем запрос
    results = query.all()

    # Возвращаем результаты
    if len(results) > 0:

        print("Результат выполнения запроса успешный")
        return results
    else:
        # raise HTTPException(status_code=300, detail=f"Результат выполнения << {condition} >> - пустой")
        return False


@app.post("/getPercent", tags=['Мои API'])
async def get_percent(audiences: List[Audience]):
    """ Пример: data.age BETWEEN 18 AND 35
                data.sex = 1 AND data.age >= 18 """


    try:
        # b.	Для каждой из аудиторий отобрать из таблицы всех респондентов, подходящих под параметры
        result = {}

        unswer1 = process_sql_condition(audiences[0].audience1)

        result['audience1'] = unswer1
        df1 = pd.DataFrame(unswer1)
        print(df1.head().to_string())

        unswer2 = process_sql_condition(audiences[0].audience2)

        result['audience2'] = unswer2
        df2 = pd.DataFrame(unswer2)

        # с. Для каждой из аудиторий взять средний Weight респондента этой аудиторий, сгруппировав по их уникальному номеру
        if df1.empty or df2.empty:
            return {"error": 'датафрейм пустой'}
        else:
            df_group_1 = df1.groupby('respondent')['weight'].mean()
            df_group_2 = df2.groupby('respondent')['weight'].mean()
            if df_group_1.equals(df_group_2):
                return {"percent": "100%"}
            else:

                merged_df = pd.merge(df_group_1, df_group_2, on='weight')

                percent = (len(merged_df) / len(df1)) * 100

                return {"percent": "{:.2f}%".format(percent)}
    except Exception as err:

        return {"error": err.__str__()}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)
