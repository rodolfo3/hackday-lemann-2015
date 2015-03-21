db.schools.find({turmas: null}).map(function(s) {
  
    var turmas = db.weekly.aggregate([
        {
            "$match": {
                "escola": s.name
            }
        },
        {
            "$group": {
                "_id": "$turma"
            },
        },
        {
            "$unwind": "$_id"
        },
        {
            "$project": {
                "name": "$_id"
            }
        }
    ])["result"];
    s.turmas = turmas;
    db.schools.save(s);
    return s;
});
