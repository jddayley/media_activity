from flask import Flask
import mariadb
import sys
from flask import render_template
from flask import Flask, redirect, url_for, request
from datetime import datetime
import json
application = Flask(__name__)
#JSONEncoder_olddefault = json.JSONEncoder.default

tableName = "members"

@application.route("/")
@application.route("/movie/")
def movie_table():
    conn = getDBcon()
    cur = conn.cursor()
    cur.execute(
            "SELECT CONCAT( '[', GROUP_CONCAT(JSON_OBJECT('event',tv.state, 'id', tv.entity_id, 'date', tv.tvdate) ),']') as json FROM (SELECT states.state, states.entity_id, DATE(CONVERT_TZ(states.last_updated ,'+00:00','-04:00')) as tvdate  FROM homeassistant.states WHERE (states.entity_id='sensor.frontroom_activity' OR states.entity_id='sensor.kidsroom_activity' OR states.entity_id='sensor.bedroom_activity' OR states.entity_id='sensor.lg_activity') AND states.state != 'unknown' AND states.state != ' '  GROUP BY states.entity_id, states.state, DATE(last_updated) ORDER BY last_updated DESC ) as tv"
            )
    queryresult = cur.fetchone()[0]
    #print(queryresult)
    #queryresult = {'firstname': "Mr.", 'lastname': "My Father's Son"}
    return render_template("movie_table.html", movies=queryresult)
@application.route("/pivot/")
def pivot_table():
    conn = getDBcon()
    cur = conn.cursor()
    cur.execute(
            "SELECT CONCAT( '[', GROUP_CONCAT(JSON_OBJECT('event',tv.state, 'id', tv.entity_id, 'date', tv.tvdate) ),']') as json FROM (SELECT states.state, states.entity_id, DATE(CONVERT_TZ(states.last_updated ,'+00:00','-04:00')) as tvdate  FROM homeassistant.states WHERE (states.entity_id='sensor.frontroom_activity' OR states.entity_id='sensor.kidsroom_activity' OR states.entity_id='sensor.bedroom_activity' OR states.entity_id='sensor.lg_activity') AND states.state != 'unknown' AND states.state != ' '  GROUP BY states.entity_id, states.state, DATE(last_updated) ORDER BY last_updated DESC ) as tv"
            )
    queryresult = cur.fetchone()[0]
    #print(queryresult)
    #queryresult = {'firstname': "Mr.", 'lastname': "My Father's Son"}
    return render_template("pivot.html", movies=queryresult)
def getDBcon():
    try:
        conn = mariadb.connect(
            user="admin",
            password="2beornot2be",
            host="192.168.0.22",
            port=3306,
            database="homeassistant"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn