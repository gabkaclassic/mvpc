import configparser

config = configparser.ConfigParser()
config.read("config.cfg")

# Application configuration
app_host = config.get("app", "host")
app_port = config.getint("app", "port")
app_reload = config.getboolean("app", "reload")
workers = config.getint("app", "workers")
node_type = config.get("app", "node_type")

# Docker builds configuration
docker_work_directory = config.get("docker", "work_directory")

# Database configuration
db_username = config.get("db", "username")
db_password = config.get("db", "password")
db_host = config.get("db", "host")
db_port = config.get("db", "port")
db_name = config.get("db", "name")
