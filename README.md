# Link-Shrink with IP Grabber

This is a simple API built using FastAPI that allows users to login with JWT tokens and create short links. It also logs each request made to the short link endpoint, storing the visitor's IP address, user agent, and timestamp in a PostgreSQL database.

## Requirements

To run this project, you'll need the following software installed on your machine:

    Python 3.7 or higher
    PostgreSQL 12 or higher

You'll also need to install the required Python packages using pip:

    pip install -r requirements.txt

## Configuration

Before you can run the application, you'll need to create a .env file in the project root directory with the following environment variables for example:
    
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_NAME=IP-Grabber
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=123
    SECRET_KEY=jHj8O4oSAfi5jkaSDFG41Rg33NOawBHHIoWp4cgqWN
    ALGORITHM=HS256
    ACCESS_TOKEN_MINUTES=60
    
## Usage

To start the web server, run the ```main.py``` file or run the following command:

    uvicorn main:app --reload
    
To view the API documentation visit ```localhost:8000/redoc``` or ```localhost:8000/docs```.

## License

This project is licensed under the MIT License. See the LICENSE file for details.



