# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

ENV PATH /home/root/.local/bin:${PATH}

# Install the dependencies
RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir cryptography
RUN pip install --no-cache-dir pydantic
RUN pip install --no-cache-dir uvicorn

RUN echo $(python3 -m site --user-base)

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8002

# Run the application
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]
