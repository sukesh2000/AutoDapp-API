import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'base'
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]
    KEY = {
      "mnemonic": [
        "arrow",
        "equip",
        "robust",
        "unable",
        "defy",
        "letter",
        "fragile",
        "arch",
        "until",
        "unfair",
        "vivid",
        "mushroom",
        "sniff",
        "police",
        "multiply"
      ],
      "secret": "928338cd083c1cb3b791cad7f89ccc283c11365e",
      "amount": "11635800074",
      "pkh": "tz1crdfpwanvWJ7n7hEq2Wvj3BuGfVfva8fE",
      "password": "kfPvDiji8P",
      "email": "qlavxonl.zwylvzfh@tezos.example.org"
    }
    SHELL = 'https://florence-tezos.giganode.io'
    MAINCONTRACT = 'KT19NQzt1D7DnKcGqqkRsgB9eya11qxahJXX'

class ProductionConfig(Config):
    SECRET_KEY = 'prod'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'