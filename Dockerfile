FROM python:alpine3.20

RUN apk update && apk upgrade

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x ./entrypoint.sh 

# # # Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]