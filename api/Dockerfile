FROM python:3.7
EXPOSE 80
COPY requirements.txt /opt
RUN pip install -r opt/requirements.txt
COPY . /opt
WORKDIR opt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--workers","4"]