FROM python:3.10

WORKDIR /app

COPY . /app/

RUN pip install -U pip  \
    &&pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]