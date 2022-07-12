FROM ubuntu:18.04

# Install Python
RUN apt update && \
    apt install -y \
        python3 \
        python3-pip && \
    apt clean

# Set up a working folder and install the pre-reqs
WORKDIR /app
ADD . /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV FLASK_APP=main.py

ENV PORT 5000
EXPOSE $PORT

# Run training and predictions
CMD ["python3", "main.py"]