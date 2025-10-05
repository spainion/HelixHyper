FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["uvicorn", "hyperhelix.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
