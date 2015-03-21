a = db.weekly.aggregate([
    {
        $group: {
            _id: "$escola"
        },
    },
    {
        $project: {
            _id: 0,
            name: "$_id"
        }
    }
])["result"];
db.schools.insert(a);
