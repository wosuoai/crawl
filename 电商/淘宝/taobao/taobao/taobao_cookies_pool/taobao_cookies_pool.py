import requests
import hashlib
import time
from flask import Flask,jsonify
import json

class CookiesPool:
    def __init__(self) -> None:
        self.app = Flask(__name__)
    
    # 获取cookiesList
    def get(self):
        pass