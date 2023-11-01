import json
from datetime import datetime

from database import collection


async def aggregate_salaries(message: str) -> str:
    data = json.loads(message)
    dt_from, dt_upto, group_type = data['dt_from'], data['dt_upto'], data['group_type']
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {
            "_id": {"$dateTrunc": {"date": "$dt", "unit": group_type}},
            "totalValue": {"$sum": "$value"}}},
        {"$project": {
            "_id": 0,
            "label": {
                "$dateToString": {"format": "%Y-%m-%dT%H:%M:%S",
                                  "date": "$_id"}},
            "salary": "$totalValue"}}
    ]

    cursor = collection.aggregate(pipeline)
    dataset = []
    labels = []
    async for document in cursor:
        dataset.append(document['salary'])
        labels.append(document['label'])
    return json.dumps({"dataset": dataset, "labels": labels})
