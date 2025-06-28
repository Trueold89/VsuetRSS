FROM python:3.13-alpine as builder
RUN pip install -U pip build
COPY . /tmp/build
WORKDIR /tmp/build
RUN python -m build --sdist

FROM python:3.13-alpine as runtime
RUN apk update && apk add curl --no-cache
COPY --from=builder /tmp/build/dist/* ./
RUN pip install -U pip && pip install *.tar.gz
RUN rm *.tar.gz
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:80/service/health
EXPOSE 80
ENTRYPOINT ["gunicorn"]
CMD ["-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "vsuetrssfeed:root_api"]
