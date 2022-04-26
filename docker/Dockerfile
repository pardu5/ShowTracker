FROM python
WORKDIR /src
RUN pip install requests
run pip install mysql-connector-python
COPY . /src
CMD ["python", "docker_test.py"]