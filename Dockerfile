FROM sukesh1312/pytezos:latest
RUN adduser --system --group --no-create-home app
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
RUN chown -R app:app /app
USER app