import utils


def get_decreasing_schools(field_name="totalminutes", op="avg", extraFilter=None):
    db = utils.get_database()
    
    aggregateFilter = []
    if extraFilter:
        aggregateFilter.append({
            "$match": extraFilter
        })

    results = db.weekly.aggregate(list(aggregateFilter) + [
        {
            '$group': {
                '_id': {
                    "e": "$escola",
                    "w": "$semana",
                },
                'avg': {
                    '${}'.format(op): "${}".format(field_name)
                },
            }
        }
    ])["result"]
    all_schools = {}
    for r in results:
        school = r["_id"]["e"]
        week = r["_id"]["w"]
        avg = r["avg"]
        all_schools[school] = all_schools.get(school, {})
        all_schools[school][week] = avg

    process_output = []
    for school, data in all_schools.iteritems():
        avg = sum(data.values())/len(data.values())
        current = sorted(data.keys())[-1]
        last = sorted(data.keys())[-2]
        diff = data[current] - data[last]
        out = {
            'schoolName': school,
            'avg': avg,
            'week': last,
            'current': data[current],
            'last': data[last],
            'diff': diff,
            'percentDiff': float(diff)/data[last] * 100 if data[last] else None,
        }
        process_output.append(out)

    probs = filter(lambda x: x["diff"] < 0, process_output)
    probs.sort(key=lambda x: x['percentDiff'])

    return probs
