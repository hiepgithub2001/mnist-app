from flask_sqlalchemy import SQLAlchemy
from model.model import MLModel

class MLModelRepository:
    def __init__(self, db : SQLAlchemy):
        self.db = db

    def add_model(self, model_script, hash_value):
        model = MLModel(model_script=model_script, hash=hash_value, name='Test Name')
        self.db.session.add(model)
        self.db.session.commit()
        return model

    def get_model_by_id(self, model_id):
        return self.db.session.query(MLModel).filter(MLModel.id == model_id).first()

    def get_model_by_hash(self, model_MD5_hash):
        return self.db.session.query(MLModel).filter(MLModel.hash == model_MD5_hash).first()

    def get_all_models(self):
        return self.db.session.query(MLModel).all()

    def update_model(self, model_id, model_script=None, hash_value=None):
        model = self.db.session.query(MLModel).filter(MLModel.id == model_id).first()
        if model:
            if model_script is not None:
                model.model_script = model_script
            if hash_value is not None:
                model.hash = hash_value
            self.db.session.commit()

    def delete_model(self, model_id):
        model = self.db.session.query(MLModel).filter(MLModel.id == model_id).first()
        if model:
            self.db.session.delete(model)
            self.db.session.commit()