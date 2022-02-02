# fastapi_twitter_api_2
fastapi_twitter_api upgrade using a MySQL database with docker.

## MySQL Configuration

1. You should install Docker in your environment
2. Open your terminal and execute this line for create MySQL docker
   `docker run -d -p 33060:3306 --name mysql-db -e MYSQL_ROOT_PASSWORD=secret`
3. Enter to MySQL docker and create the database
   `docker exec -it mysql-db mysql -p`
4. Create the database
   `create database twitterdb;`

***Note: Your always should run the mySQL docker for using this Twitter API example***

## Run Uvicorn

1. Run virtual environment
   
   Windows
   `.\venv\Scripts\activate`

   Mac/Linux
   `source venv/bin/activate`

2. Run Uvicorn server
   `uvicorn main:app --reload`