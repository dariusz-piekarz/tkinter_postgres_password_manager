from db_core import PostgreAdminConnector
from Config import Config


class Shared:
    pg = PostgreAdminConnector()
    config = Config("config.json")
