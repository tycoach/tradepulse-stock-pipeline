FROM apache/airflow:2.10.5-python3.11

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/jars \
    && curl -fsSL -o /opt/jars/postgresql.jar \
       https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar

RUN ln -s "$(dirname "$(dirname "$(readlink -f "$(which java)")")")" /opt/java
ENV JAVA_HOME=/opt/java

USER airflow
COPY requirements.txt /requirements.txt
RUN python -m pip install --no-cache-dir -r /requirements.txt \
    && python -c "import pyspark; print('PySpark', pyspark.__version__, 'installed OK')"