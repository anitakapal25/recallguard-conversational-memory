FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/implementation
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --create-home --uid 10001 recallguard && mkdir -p /data && chown recallguard /data
COPY implementation /app/implementation
USER recallguard
ENV RECALLGUARD_DB_PATH=/data/chroma
EXPOSE 5000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--call", "app:create_app"]
