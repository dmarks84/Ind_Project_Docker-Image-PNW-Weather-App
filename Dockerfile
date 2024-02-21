FROM python:3.11

COPY . /

WORKDIR /

RUN pip3 install -r reqs.txt

EXPOSE 8050

ENTRYPOINT ["python3"]

CMD ["alerts.py"]