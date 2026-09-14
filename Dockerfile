# One image, built from this repository, on the declared Python floor of the
# project. The data location is mounted; nothing lives inside the image.
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir . \
    && rm -rf /app/src /app/pyproject.toml /app/README.md /app/LICENSE \
    && useradd --create-home --shell /usr/sbin/nologin paraphe

# Cards live at the mounted location. The default bind is loopback: the answer
# path refuses a non-loopback bind, so a deployment that must be reachable from
# outside the container configures the phone destination instead.
ENV PARAPHE_STORE_PATH=/data/inbox.sqlite
VOLUME /data
USER paraphe

ENTRYPOINT ["paraphe"]
