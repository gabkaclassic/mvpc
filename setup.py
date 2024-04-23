import configparser

config = configparser.ConfigParser()
config.read("config.cfg")

# Application configuration
app_host = config.get("app", "host")
app_port = config.getint("app", "port")
app_reload = config.getboolean("app", "reload")
workers = config.getint("app", "workers")
node_type = config.get("app", "node_type")
