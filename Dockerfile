# base image
FROM python:3.12-slim

# setting working directory
WORKDIR /brw_tracker

# installing dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# adding user
RUN useradd -m user
RUN chown -R user:user /brw_tracker
USER user


# startup command
CMD ["python", "main.py"]