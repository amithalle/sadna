FROM python:3.8 as compiler
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./

FROM python:3.8-slim AS build-image
COPY --from=compiler /root/.local/bin /root/.local
ENV PATH=/root/.local:$PATH

CMD ["flask", "run", "srcflaskr"]

