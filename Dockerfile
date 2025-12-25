# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . .

# Hugging Face Spaces run on port 7860 by default
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]