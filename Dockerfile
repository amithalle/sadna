FROM python:3.8 as compiler
COPY requirements.txt .
RUN pip install --user -r requirements.txt


FROM python:3.8-slim AS build-image
COPY --from=compiler /root/.local/ /root/.local
COPY src/ ./
ENV PATH=/root/.local:$PATH

CMD ["flask", "run", "srcflaskr"]

