FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "eastridge:create_app()", "-w", "4", "-b", "0.0.0.0:5000"]