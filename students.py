import bson
import utils


def include_me(app):
    app.route("/schools/<school_id>/turma/<turma_id>/students")(utils.to_json(student_list))


def student_list(school_id, turma_id):
    db = utils.get_database()
    school = utils.get_database().schools.find_one({"_id": bson.ObjectId(school_id)})
    data_filter = {
        "escola": school["name"],
        "turma": turma_id,
    }
    print repr(data_filter)
    result = db.weekly.aggregate([
        {
            "$match": data_filter,
        },
        {
            "$group": {
                "_id": "$aluno"
            }
        },
        {
            "$project": {
                "_id": 1,
                "name": {"$concat": ["Aluno ", "$_id"]}
            }
        },
        {
            "$sort": {
                "name": 1
            }
        }
    ])["result"]

    return result
