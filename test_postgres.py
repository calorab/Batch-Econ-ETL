import psycopg2

# Establish a connection
try:
    connection = psycopg2.connect(
        dbname="batch-econ-etl",
        user="AllHeart",
        host="localhost",
        port="5432"
    )
except psycopg2.Error as err:
    print("An error occured: ", err)

# Get the username and host from the connection parameters
username = connection.get_dsn_parameters()["user"]
host = connection.get_dsn_parameters()["host"]
password = connection.get_dsn_parameters()

print("Username:", username)
print("Host:", host)
print('password:', password)

# Close the connection
connection.close()