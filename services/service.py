from extension import db

def save(obj):
    db.session.add(obj)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return obj

def fetch(Model, pk_value):
    return db.session.get(Model, pk_value)

def fetch_by(Model, **filters):
    return Model.query.filter_by(**filters).first()

def paginate(Model, page, per_page, **filters):
    query = Model.query.filter_by(**filters).order_by(Model.id.desc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def update(obj, **fields):
    try:
        for name, value in fields.items():
            setattr(obj, name, value)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return obj

def remove(obj):
    db.session.delete(obj)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
