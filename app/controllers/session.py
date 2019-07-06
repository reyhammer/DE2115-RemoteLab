from app import app, db
from flask import render_template, flash, request, redirect, session, url_for
from app.models.tables import User, Session
from app.models.forms import CommandForm

from app.controllers.login import login_required, fresh_login_required, current_user

import serial
import time
import datetime
import os
import threading

arduino_sessions = {}
queue = []
next_user = None
next_session = None

def bind_func(FPGA):
    time.sleep(1)
    myCmd = os.popen("sudo usbip bind -b %s" % FPGA).read()
    print(myCmd)

def end_session(session):
    global next_user
    global next_session

    #myCmd = os.popen("sudo usbip unbind -b %s" % session.FPGA).read()

    if (len(queue) > 0):
        session.user_id = None
        db.session.commit()

        next_session = Session.query.filter(Session.id == session.id).first()
        next_user = queue[0]
        #print("Next user: %r" % next_user)
    else:
        session.available = True
        session.user_id = None
        db.session.commit()

def init_session(user, session):
    user.session = session
    db.session.commit()

    if not session.Arduino in arduino_sessions:
        port = serial.Serial(session.Arduino, baudrate = 9600, timeout = 1)
        arduino_sessions[session.Arduino] = port
        port.write("b'\n")
        port.readline()

    arduino_sessions[session.Arduino].write(("chuser@%d&%s\n" % (session.user.id, session.user.name)).encode("ASCII", errors='ignore'));
    arduino_sessions[session.Arduino].readline()

    bind_func_thread = threading.Thread(target = bind_func, args=(session.FPGA, ))
    bind_func_thread.start()

@app.route("/threads/")
def threads():
    return str(threading.activeCount())

@app.route("/session/<username>", methods=["GET"])
def session(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return "NO_USERNAME"

    session = Session.query.filter_by(user_id=user.id).first()

    if not session:
        return "NO_SESSION"

    return ("%s" % session.FPGA)

@app.route("/session_cmd/<int:session>", methods=["GET", "POST"])
@login_required
def session_cmd(session):
    form = CommandForm()
    session = Session.query.filter_by(id=session).first()

    if request.method == "POST" and form.validate_on_submit() and session:
        if not session.Arduino in arduino_sessions:
            port = serial.Serial(session.Arduino, baudrate = 9600, timeout = 1)
            arduino_sessions[session.Arduino] = port
            port.write("b'\n")
            port.readline()

        arduino_sessions[session.Arduino].write((form.command.data+"\n").encode("ASCII", errors='ignore'));
        b = arduino_sessions[session.Arduino].readline()
        flash(b.strip()+"&success")

        if form.command.data == "endsession":
            end_session(session)
            return redirect("/home")

        return render_template("session_cmd.html", session = session, form = form)

    return render_template("session_cmd.html", session = session, form = form)

@login_required
@app.route("/add_session", methods=["GET"])
def add_session():
	i = Session("", "/dev/ttyUSB0", "http://192.168.1.15:8090/stream.mjpg")
	db.session.add(i)
	db.session.commit()
	return "Sucesso !!!"

@app.route("/session_cron_job", methods=["GET"])
def session_cron_job():
    global next_user
    global next_session

    u = Session.query.filter(Session.available == False).all()

    for session in u:
        #print("Session: %d !!!" % ( int(time.mktime(datetime.datetime.now().timetuple())) - int(time.mktime(session.timestamp.timetuple())) ) )
        #if (( int(time.mktime(datetime.datetime.now().timetuple())) - int(time.mktime(session.timestamp.timetuple())) ) > (1*60)):
        print("Let's make this session "+str(session.id)+" free !!!")
        end_session(session)

    return "OK"

@app.route("/new_session", methods=["GET"])
def new_session():
    global next_user
    global next_session

    if current_user.session:
        return redirect("session_cmd/"+str(current_user.session.id))

    available_session = Session.query.filter(Session.available == True).first()

    if available_session and queue == []:
        available_session.available = False
        available_session.timestamp = db.func.now()
        db.session.commit()

        init_session(current_user, available_session)
        #return session_cmd(available_session.id)
        return redirect("/session_cmd/"+str(available_session.id))

    if next_user == current_user and next_session != None:
        i = next_session.id

        queue.remove(User.query.filter(User.id == current_user.id).first())

        init_session(current_user, next_session)

        next_user = None
        next_session = None

        return redirect("session_cmd/"+str(i))

    #print("Current_user = ", current_user)

    for index in range(len(queue)):
        if queue[index].id == current_user.id:
            #print("RETURN Current_user = ", current_user, index, queue[index].id, current_user.id)
            return render_template("session_queue.html", position = index+1)

    queue.insert(len(queue), User.query.filter(User.id == current_user.id).first())

    #print("Queue = ", queue)

    return render_template("session_queue.html", position = len(queue))

@app.route("/sessions", methods=["GET"])
def sessions():
	u = Session.query.filter(Session.available == True).all()

	return render_template("sessions.html", sessions=u)
