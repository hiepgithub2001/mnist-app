FROM python:3.12.2

# Set the working directory in the container
WORKDIR /app

VOLUME ["C:\\Users\\minht\\AppData\\Local\\pip\cache", "/root/.cache/pip"]
# Copy the current directory contents into the container at /app
COPY ./training_service /app
COPY requirements.txt /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt


# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "main.py"]