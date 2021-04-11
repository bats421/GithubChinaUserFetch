import yaml
import configparser

config = configparser.ConfigParser()
with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
