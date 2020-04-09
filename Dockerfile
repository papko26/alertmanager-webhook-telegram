FROM python:3.8-alpine as builder

WORKDIR /install
COPY requirements.txt .
RUN apk add --no-cache gcc python3-dev libffi-dev openssl-dev build-base
RUN pip3 install --install-option="--prefix=/install" --ignore-installed -r requirements.txt && rm requirements.txt

FROM python:3.8-slim
COPY --from=builder /install /usr/local
COPY --from=builder /root/.cache /app/.cache
RUN pip3 install cryptography && rm -rf /root/.cache
WORKDIR /app 
COPY flaskAlert.py .
EXPOSE 9119
CMD ["gunicorn","-b","0.0.0.0:9119","--workers=2", "--threads=4", "--worker-class=gthread","--log-file=-","--worker-tmp-dir","/dev/shm", "flaskAlert:app"]