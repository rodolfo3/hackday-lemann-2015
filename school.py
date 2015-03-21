import bson
import datetime
import utils
import flask


def include_me(app):
    app.route("/schools/")(utils.to_json(school_list))
    app.route("/schools/<id>/weeklyReport")(utils.to_json(school_weekly_report))


def _add_weekly_report_link(school):
    school["_links"] = school.get("_links", {})
    school["_links"]["weeklyReport"] = flask.url_for(
        ".school_weekly_report",
        id=school["_id"],
        _external=True
    )
    return school


def school_list():
    return map(
        _add_weekly_report_link,
        utils.get_database().schools.find()
    )


def _get_school(id_):
    return utils.get_database().schools.find_one({"_id": bson.ObjectId(id_)})


def school_weekly_report(id):
    school = _get_school(id);
    db = utils.get_database()
    result = db.weekly.aggregate([
        {
            "$match": {
                "escola": school["name"],
            }
        },
        {
            "$group": {
                "_id": "$semana",

                "minTotalMinutes": {"$min": "$totalminutes"},
                "minVideoMinutes": {"$min": "$videominutes"},
                "minExerciseMinutes": {"$min": "$exerciseminutes"},
                "minNivel1": {"$min": "$nivel1"},
                "minNivel2": {"$min": "$nivel2"},
                "minPrecisaPraticar": {"$min": "$precisa_praticar"},
                "minPraticado": {"$min": "$praticado"},
                "minDominado": {"$min": "$dominado"},
                "minPontos": {"$min": "$pontos"},

                "maxTotalMinutes": {"$max": "$totalminutes"},
                "maxVideoMinutes": {"$max": "$videominutes"},
                "maxExerciseMinutes": {"$max": "$exerciseminutes"},
                "maxNivel1": {"$max": "$nivel1"},
                "maxNivel2": {"$max": "$nivel2"},
                "maxPrecisaPraticar": {"$max": "$precisa_praticar"},
                "maxPraticado": {"$max": "$praticado"},
                "maxDominado": {"$max": "$dominado"},
                "maxPontos": {"$max": "$pontos"},

                "avgTotalMinutes": {"$avg": "$totalminutes"},
                "avgVideoMinutes": {"$avg": "$videominutes"},
                "avgExerciseMinutes": {"$avg": "$exerciseminutes"},
                "avgNivel1": {"$avg": "$nivel1"},
                "avgNivel2": {"$avg": "$nivel2"},
                "avgPrecisaPraticar": {"$avg": "$precisa_praticar"},
                "avgPraticado": {"$avg": "$praticado"},
                "avgDominado": {"$avg": "$dominado"},
                "avgPontos": {"$avg": "$pontos"},
            }
        }
    ])["result"]
    def _split_result(r):
        return {
            "_id": r["_id"],
            "avg": {
                "totalMinutes": r["avgTotalMinutes"],
                "videoMinutes": r["avgVideoMinutes"],
                "exerciseMinutes": r["avgExerciseMinutes"],
                "nivel1": r["avgNivel1"],
                "nivel2": r["avgNivel2"],
                "precisaPraticar": r["avgPrecisaPraticar"],
                "praticado": r["avgPraticado"],
                "dominado": r["avgDominado"],
                "pontos": r["avgPontos"],
            },

            "min": {
                "totalMinutes": r["minTotalMinutes"],
                "videoMinutes": r["minVideoMinutes"],
                "exerciseMinutes": r["minExerciseMinutes"],
                "nivel1": r["minNivel1"],
                "nivel2": r["minNivel2"],
                "precisaPraticar": r["minPrecisaPraticar"],
                "praticado": r["minPraticado"],
                "dominado": r["minDominado"],
                "pontos": r["minPontos"],
            },

            "max": {
                "totalMinutes": r["maxTotalMinutes"],
                "videoMinutes": r["maxVideoMinutes"],
                "exerciseMinutes": r["maxExerciseMinutes"],
                "nivel1": r["maxNivel1"],
                "nivel2": r["maxNivel2"],
                "precisaPraticar": r["maxPrecisaPraticar"],
                "praticado": r["maxPraticado"],
                "dominado": r["maxDominado"],
                "pontos": r["maxPontos"],
            },
        }

    return map(_split_result, result)
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
