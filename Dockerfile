#1 Base Image: Grab a lightweight version of Python
FROM python:3.11-slim

#2 Set the working directory inside the container
WORKDIR /app

#3 Copy our requirements list into the container
COPY requirements.txt .

#4 Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

#5 Copy all our python scripts into the container
COPY . .

#6 Run and extract, and if successful (&&) run transform
CMD ["sh", "-c", "python extract.py && python transform.py"] 