import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import keyboard  # pip install keyboard

# Firebase 초기화
cred = credentials.Certificate("ent-pibo-firebase-adminsdk-fbsvc-c45280ac53.json")  # 경로는 파일 위치에 맞게 수정
firebase_admin.initialize_app(cred)
db = firestore.client()

# 사용자 UID 설정 (테스트용으로 하드코딩하거나, 다른 방식으로 가져오세요)
user_uid = "GgGFBmYPq1fw6ss0mGVP6dJzAcz2"  # 실제 사용자 UID로 바꿔주세요

# reps, time, exp 설정값 (원하는 방식으로 수정 가능)
REPS_PER_SET = {
    'easy': 8,
    'normal': 12,
    'hard': 15
}
TIME_PER_SET = 10  # 예시로 1세트 10초
EXP_PER_REP = 10   # 예시로 1회당 경험치 10

def update_exercise_data(exercise):
    today_str = datetime.now().strftime("%Y-%m-%d")
    user_ref = db.collection("users").document(user_uid)
    
    # 유저 difficulty 가져오기
    user_doc = user_ref.get()
    if not user_doc.exists:
        print("User not found.")
        return
    
    difficulty = user_doc.to_dict().get("difficulty", "normal")
    reps = REPS_PER_SET.get(difficulty, 12)
    time_spent = TIME_PER_SET
    exp = reps * EXP_PER_REP

    exercise_ref = user_ref.collection(exercise).document(today_str)
    exercise_doc = exercise_ref.get()

    if exercise_doc.exists:
        existing_data = exercise_doc.to_dict()
        new_set_count = existing_data.get(f"{difficulty}_set", 0) + 1
        new_reps = existing_data.get("reps", 0) + reps
        new_time = existing_data.get("time", 0) + time_spent
        new_exp = existing_data.get("exp", 0) + exp
    else:
        new_set_count = 1
        new_reps = reps
        new_time = time_spent
        new_exp = exp

    update_data = {
        "date": today_str,
        f"{difficulty}_set": new_set_count,
        "reps": new_reps,
        "time": new_time,
        "exp": new_exp,
    }

    exercise_ref.set(update_data, merge=True)
    print(f"✅ {exercise.capitalize()} updated for difficulty: {difficulty}")


print("Press 's' for squat, 'b' for bench, 'd' for deadlift. Press ESC to exit.")
while True:
    if keyboard.is_pressed('s'):
        update_exercise_data('squat')
        keyboard.wait('s', suppress=True)  # 중복 방지
    elif keyboard.is_pressed('b'):
        update_exercise_data('bench')
        keyboard.wait('b', suppress=True)
    elif keyboard.is_pressed('d'):
        update_exercise_data('deadlift')
        keyboard.wait('d', suppress=True)
    elif keyboard.is_pressed('esc'):
        print("Exiting...")
        break
