# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Define the build argument and set it as an environment variable
ARG DISCORD_BOT_TOKEN
ENV DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run bot.py when the container launches
CMD ["python", "bot.py"]
