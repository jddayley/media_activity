from flask import Flask, render_template
import mariadb
import sys

application = Flask(__name__)

@application.route("/")
@application.route("/movie/")
def movie_table():
    conn = getDBcon()
    cur = conn.cursor()
    cur.execute(
        "SELECT CONCAT( '[', GROUP_CONCAT(JSON_OBJECT('event', tv.state, 'id', tv.name, 'date', tv.tvdate)), ']') as json "
        "FROM ("
        "SELECT states.state, "
        "CASE states.metadata_id "
        "WHEN '138' THEN 'Basement' "
        "WHEN '139' THEN 'Bedroom' "
        "WHEN '140' THEN 'Office' "
        "WHEN '141' THEN 'LG TV' "
        "END as name, "
        "DATE(CONVERT_TZ(FROM_UNIXTIME(states.last_updated_ts), '+00:00', '-04:00')) as tvdate "
        "FROM homeassistant.states "
        "WHERE (states.metadata_id IN ('138', '139', '140', '141')) "
        "AND states.state != 'unknown' "
        "AND states.state != ' ' "
        "AND states.last_updated_ts >= UNIX_TIMESTAMP(CURDATE()) - (2 * 86400) "
        "GROUP BY states.metadata_id, states.state, DATE(CONVERT_TZ(FROM_UNIXTIME(states.last_updated_ts), '+00:00', '-04:00')) "
        "ORDER BY states.last_updated_ts DESC "
        "LIMIT 40) as tv"
    )
    queryresult = cur.fetchone()[0]
    return render_template("movie_table.html", movies=queryresult)

@application.route("/pivot/")
def pivot_table():
    conn = getDBcon()
    cur = conn.cursor()
    cur.execute(
        "SELECT CONCAT( '[', GROUP_CONCAT(JSON_OBJECT('event', tv.state, 'id', tv.name, 'date', tv.tvdate)), ']') as json "
        "FROM ("
        "SELECT states.state, "
        "CASE states.metadata_id "
        "WHEN '138' THEN 'Basement' "
        "WHEN '139' THEN 'Bedroom' "
        "WHEN '140' THEN 'Office' "
        "WHEN '141' THEN 'LG TV' "
        "END as name, "
        "DATE(CONVERT_TZ(FROM_UNIXTIME(states.last_updated_ts), '+00:00', '-04:00')) as tvdate "
        "FROM homeassistant.states "
        "WHERE (states.metadata_id IN ('138', '139', '140', '141')) "
        "AND states.state != 'unknown' "
        "AND states.state != ' ' "
        "AND states.last_updated_ts >= UNIX_TIMESTAMP(CURDATE()) - (2 * 86400) "
        "GROUP BY states.metadata_id, states.state, DATE(CONVERT_TZ(FROM_UNIXTIME(states.last_updated_ts), '+00:00', '-04:00')) "
        "ORDER BY states.last_updated_ts DESC "
        "LIMIT 40) as tv"
    )
    queryresult = cur.fetchone()[0]
    return render_template("pivot.html", movies=queryresult)

def getDBcon():
    try:
        conn = mariadb.connect(
            user="admin",
            password="",
            host="",
            port=3306,
            database="homeassistant"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

if __name__ == "__main__":
    application.run(debug=True)
