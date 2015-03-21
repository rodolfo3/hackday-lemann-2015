import datetime
import utils


def include_me(app):
    app.route("/schools/")(utils.to_json(school_list))
    app.route("/schools/<id>/weeklyReport")(utils.to_json(school_weekly_report))


def school_list():
    return [
        {
            "id": "abc",
            "name": "Escola ABC",
        },
        {
            "id": "31415",
            "name": "Escola Pi",
        },
    ]


def school_weekly_report(id):
    return [
        {
            "week": datetime.datetime(2014, 11, 23),
            "schoolId": id,
            "totalMinutes": 20.5,
            "videoMinutes": 10.25,
            "exerciseMinutes": 10.25,
        },
        {
            "week": datetime.datetime(2014, 11, 30),
            "schoolId": id,
            "totalMinutes": 18.5,
            "videoMinutes": 10.25,
            "exerciseMinutes": 8.25,
        },
    ]
