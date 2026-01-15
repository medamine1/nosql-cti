def serialize_mongo(doc):
    doc["_id"] = str(doc["_id"])
    from datetime import datetime
    for k, v in doc.items():
        if isinstance(v, datetime):
            doc[k] = v.isoformat()
    return doc
