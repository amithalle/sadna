FROM python:3.8 as compiler
COPY requirements.txt .
RUN pip install --user -r requirements.txt


FROM python:3.8-slim AS build-image
COPY --from=compiler /root/.local/ /root/.local
WORKDIR /root/
COPY src/ ./
ENV PATH=/root/.local:/root/.local/bin:$PATH
ENV FLASK_APP="src/flaskr"

CMD ["flask", "run"]

