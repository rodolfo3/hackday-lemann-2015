import datetime
import csv
r = csv.reader(open("../../dados/k.csv").readlines())

converter = {
  'turma': lambda x: eval(x),
  'com dificuldade': int,
  'precisa_praticar': int,
  'praticado': int,
  'nivel1': int,
  'nivel2': int,
  'dominado': int,
  'pontos': int,
  'exerciseminutes': float,
  'videominutes': float,
  'totalminutes': float,
  'semana': lambda x: datetime.datetime(*map(int, x.replace("Week", "").split("_")))
}

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

head = r.next()
all_data = []
for row in r:
  pdata = {k: converter.get(k, lambda x: x)(v) if v else None for k,v in zip(head, row)}
  all_data.append(pdata)

import pymongo
db = pymongo.MongoClient("mongodb://hackday-lemann:hacklemann@ds063449.mongolab.com:63449/hackday-lemann")
# db = pymongo.Connection()
lll =  list(chunks(all_data, 100))
for i,d in enumerate(lll):
    print datetime.datetime.now().isoformat(), i, "/", len(lll)
    db["hackday-lemann"].weekly.insert(d)
