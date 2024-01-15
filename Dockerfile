#FROM python:3.11
#LABEL authors="Sereja"
#
#
#ENTRYPOINT ["top", "-b"]
#
#WORKDIR /okkan_project
#
#COPY requirements.txt .
#
#RUN pip install -r requirements.txt
#
#COPY . .
#
#CMD gunicorn module_api.app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:80
#CMD ["uvicorn", "module_api:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.11
LABEL authors="AnosovSS"

WORKDIR okkan_project

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "module_api:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
#CMD ["uvicorn", "module_api.py:app", "--host", "0.0.0.0", "--port", "80"]