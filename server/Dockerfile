FROM python:3.11.6-alpine

# Install python and necessary libraries
RUN apk --no-cache add python3 py3-pip

# Create and set the working directory
#WORKDIR .

# When using compose
WORKDIR /server

# Copy the requirements.txt file 
COPY requirements.txt .

# Install python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
#COPY . .
# When using compose
COPY /server .

# # Expose the port your app will run on
#EXPOSE 8000

# Command to run the application
CMD ["python3", "server.py"]



