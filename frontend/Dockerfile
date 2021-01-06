FROM python:3.7
EXPOSE 8050
COPY requirements.txt /opt
RUN pip install -r opt/requirements.txt
COPY . /opt
WORKDIR opt
CMD ["python", "app.py"]