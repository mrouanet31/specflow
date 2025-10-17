
FROM mcr.microsoft.com/devcontainers/java:bookworm

COPY ./zscaler.crt /usr/local/share/ca-certificates/

RUN apt-get update && apt-get install -y ca-certificates curl && \
    update-ca-certificates