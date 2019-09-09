FROM python:3.7-slim 

WORKDIR /app

COPY ./src /app 

RUN pip install --trusted-host pypi.python.org -r requirements.txt 

CMD ["python3", "main.py"]
