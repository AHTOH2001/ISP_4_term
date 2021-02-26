FROM python:3.8

RUN pip install requests

ARG UID=1000

RUN useradd -u $UID -G 4,24,30,46 -m ForecastStealer

WORKDIR /home/ForecastStealer

USER ForecastStealer

COPY ForecastStealer.py /home/ForecastStealer/ForecastStealer.py

ENTRYPOINT ["python3", "ForecastStealer.py"]
