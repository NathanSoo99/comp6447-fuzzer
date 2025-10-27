# Start from a default ubuntu image.
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /

# Copy/Compile my fuzzer
COPY fuzzer.py /

# Install dependencies
# RUN apt-get update && apt-get install -y gdb

# Install python libraries
COPY requirements.txt /
RUN pip install -r requirements.txt

# Run it.
CMD ["python", "fuzzer.py"]

