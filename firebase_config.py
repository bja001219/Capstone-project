# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

# 이미 초기화했는지 확인
if not firebase_admin._apps:
    cred = credentials.Certificate("ent-pibo-firebase-adminsdk-fbsvc-666a413106.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
