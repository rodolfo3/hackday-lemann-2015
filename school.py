import bson
import datetime
import flask

import queries
import utils


def include_me(app):
    app.route("/schools/")(utils.to_json(school_list))
    app.route("/schools/_decreasing")(utils.to_json(school_problem_list))
    app.route("/schools/<id>/weeklyReport")(utils.to_json(school_weekly_report))


def school_list():
    return map(
        _add_weekly_report_link,
        utils.get_database().schools.find()
    )

def _add_school_by_name(data):
    data["school"] = utils.get_database().schools.find_one({"name": data["schoolName"]})
    data["_id"] = data["school"]["_id"]
    return _add_weekly_report_link(data)


def school_problem_list():
    return map(
        _add_school_by_name,
        queries.get_decreasing_schools("totalminutes")
    )


def school_weekly_report(id):
    school = _get_school(id);
    db = utils.get_database()
    data_filter = {
        "escola": school["name"],
    }
    turma = flask.request.values.get("turma")
    if turma:
        data_filter["turma"] = turma

    aluno = flask.request.values.get("aluno") or flask.request.values.get("student")
    if aluno:
        data_filter["aluno"] = aluno

    result = db.weekly.aggregate([
        {
            "$match": data_filter,
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
                "minComDificuldade": {"$min": "$com dificuldade"},

                "maxTotalMinutes": {"$max": "$totalminutes"},
                "maxVideoMinutes": {"$max": "$videominutes"},
                "maxExerciseMinutes": {"$max": "$exerciseminutes"},
                "maxNivel1": {"$max": "$nivel1"},
                "maxNivel2": {"$max": "$nivel2"},
                "maxPrecisaPraticar": {"$max": "$precisa_praticar"},
                "maxPraticado": {"$max": "$praticado"},
                "maxDominado": {"$max": "$dominado"},
                "maxPontos": {"$max": "$pontos"},
                "maxComDificuldade": {"$max": "$com dificuldade"},

                "avgTotalMinutes": {"$avg": "$totalminutes"},
                "avgVideoMinutes": {"$avg": "$videominutes"},
                "avgExerciseMinutes": {"$avg": "$exerciseminutes"},
                "avgNivel1": {"$avg": "$nivel1"},
                "avgNivel2": {"$avg": "$nivel2"},
                "avgPrecisaPraticar": {"$avg": "$precisa_praticar"},
                "avgPraticado": {"$avg": "$praticado"},
                "avgDominado": {"$avg": "$dominado"},
                "avgPontos": {"$avg": "$pontos"},
                "avgComDificuldade": {"$avg": "$com dificuldade"},
            }
        },
        {
            "$sort": {
                "_id": -1
            }
        },
    ])["result"]
    def _split_result(r):
        return {
            "_id": r["_id"],
            "week": r["_id"],
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
                "comDificuldade": r["avgComDificuldade"],
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
                "comDificuldade": r["minComDificuldade"],
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
                "comDificuldade": r["maxComDificuldade"],
            },
        }

    return map(_split_result, result)


def _add_weekly_report_link(school):
    school["_links"] = school.get("_links", {})
    school["_links"]["weeklyReport"] = flask.url_for(
        ".school_weekly_report",
        id=school["_id"],
        _external=True
    )
    return school


def _get_school(id_):
    return utils.get_database().schools.find_one({"_id": bson.ObjectId(id_)})
