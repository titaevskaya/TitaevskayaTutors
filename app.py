import os
import json
import random
from flask import Flask, render_template, request
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = 'my-super-secret-phrase-I-dont-tell-this-to-nobody'

with open("profiles.json", encoding="utf-8") as f:
    profiles = json.load(f)
print(profiles[0])

with open("goals.json", encoding="utf-8") as f:
    goals = json.load(f)
print(goals)

days_of_week = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда",
                "thu": "Четверг", "fri": "Пятница", "sat": "Суббота",
                "sun": "Воскресенье"}


@app.route('/')
def render_main():
    return render_template('index.html', teachers=random.sample(profiles, 6), goals=goals)


@app.route('/goals/<goal>/')
def render_goal(goal):
    return render_template('goal.html', goal=goal, goals=goals, teachers=profiles)


@app.route('/profiles/<id>/')
def render_profile(id):
    return render_template('profile.html', teacher=profiles[int(id)], goals=goals,
                           days_of_week=days_of_week, id=id)


@app.route('/request/')
def render_request():
    return render_template('request.html')


@app.route('/request_done/', methods=["POST"])
def render_request_done():
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    goal = request.form.get("goal")
    time = request.form.get("time")
    if os.path.isfile("request.json"):
        with open("request.json", "r", encoding="utf-8") as f:
            requests = json.load(f)
        requests.append({"goal": goal, "time": time, "name": name, "phone": phone})
        with open("request.json", "w", encoding="utf-8") as f:
            json.dump(requests, f, ensure_ascii=False)
    else:
        with open("request.json", "w", encoding="utf-8") as f:
            json.dump([{"goal": goal, "time": time, "name": name, "phone": phone}], f, ensure_ascii=False)
    return render_template('request_done.html', name=name,
                           phone=phone, goal=goal, time=time)


@app.route('/booking/<id>/<day_week>/<time>/')
def render_booking(id, day_week, time):
    return render_template('booking.html', id=id, teacher=profiles[int(id)],
                           day_week=day_week, time=time, days_of_week=days_of_week)


@app.route('/booking_done/', methods=["POST"])
def render_booking_done():
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    weekday = request.form.get("clientWeekday")
    time = request.form.get("clientTime")
    teacher = request.form.get("clientTeacher")

    profiles[int(teacher)]['free'][weekday][time] = False
    if os.path.isfile("booking.json"):
        with open("booking.json", "r", encoding="utf-8") as f:
            booking = json.load(f)
        booking.append({"teacher": profiles[int(teacher)]["name"],
                        "weekday": weekday,
                        "time": time,
                        "name": name,
                        "phone": phone})
        with open("booking.json", "w", encoding="utf-8") as f:
            json.dump(booking, f, ensure_ascii=False)
    else:
        with open("booking.json", "w", encoding="utf-8") as f:
            json.dump([{"teacher": profiles[int(teacher)]["name"],
                        "weekday": weekday,
                        "time": time,
                        "name": name,
                        "phone": phone}], f, ensure_ascii=False)
    return render_template('booking_done.html', name=name, phone=phone,
                           weekday=days_of_week[weekday], time=time, teacher=profiles[int(teacher)])


if __name__ == '__main__':
    app.run()
