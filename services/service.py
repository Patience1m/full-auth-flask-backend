from extension import db


def save(obj):
    db.session.add(obj)  # staged only, nothing sent yet
    try:
        db.session.commit()  # flush, then end transaction
    except Exception:
        db.session.rollback()  # required to reuse session
        raise
    return obj


def fetch(Model, pk_value):
    return db.session.get(Model, pk_value)  # obj or None


def fetch_by(Model, **filters):
    return Model.query.filter_by(**filters).first()  # obj or None


def paginate(Model, page, per_page, **filters):
    query = Model.query.filter_by(**filters).order_by(Model.id.desc())  # newest first
    return query.paginate(page=page, per_page=per_page, error_out=False)


def update(obj, **fields):
    try:
        for name, value in fields.items():
            setattr(obj, name, value)  # model validators run here
        db.session.commit()
    except Exception:
        db.session.rollback()  # drop half-applied changes
        raise
    return obj


def remove(obj):
    db.session.delete(obj)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
