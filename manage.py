from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config["TESTING"] = False

"""
DATABASES
"""
db = SQLAlchemy(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://postgres:postgres@localhost:5432/ultrablog"


# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "postgres://dwahtxakujsjqo:6caf66755eee6c3732bcf76af174e30d3a06c0d119e9b617669736696d0cb120@ec2-54-204-39-43.compute-1.amazonaws.com:5432/df1cmvd52cphuf"

"""
MYSQL AND SQLITE CONFIGURATION
--------------------------------------------------------------
file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://kamseupai:kampungantapisukses@localhost/ultrablog"
--------------------------------------------------------------
"""


class DataModels(db.Model):
    __tablename__ = "diarypost"
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(25))
    konten = db.Column(db.TEXT)
    featureImage = db.Column(db.String(150))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False


"""
DATA SERIALIZERS
"""

ma = Marshmallow(app)


class UltrablogSchemaClass(ma.ModelSchema):
    class Meta:
        model = DataModels


data_serializers = UltrablogSchemaClass(many=True)
data_serializer = UltrablogSchemaClass(many=False)


"""
RESTFUL API 
"""
api = Api(app)


class Diary(Resource):
    def get(self):
        payload = DataModels.query.all()
        response = data_serializers.dump(payload)
        if payload:
            return {"data": response}, 200
        else:
            return {"message": "data kosong"}, 404

    def post(self):
        model = DataModels()
        data = request.json
        print("INI ADALAH DATANYA : \n", data)
        # return ""

        model.judul = data.get("judul")
        model.konten = data.get("konten")
        model.featureImage = data.get("featureImage")
        try:
            model.save()
            return {"message": "sukses menyimpan data"}, 200
        except:
            raise
            return {"message": "gagal menyimpan, coba lagi"}, 400

    def delete(self):
        payload = DataModels.query.all()
        try:
            if payload:
                for data in payload:
                    DataModels.delete(data)
                return {"message": "Semua data sukses dihapus"}, 200
            else:
                return {"message": "Data kosong"}, 404
        except:
            return {"message": "Semua data gagal dihapus"}, 400


class DiaryId(Resource):
    def get(self, id):
        payload = DataModels.query.get(id)
        response = data_serializer.dump(payload)
        if payload:
            return {"data": response}, 200
        else:
            return {"message": "data kosong"}, 400

    def delete(self, id):
        payload = DataModels.query.get(id)
        if DataModels.delete(payload):
            return {"message": "data sukses dihapus"}, 200
        else:
            return {"message": "data gagal dihapus"}, 400


api.add_resource(Diary, "/", methods=["GET", "POST", "DELETE"])
api.add_resource(DiaryId, "/<int:id>", methods=["GET", "DELETE"])


if __name__ == "__main__":
    manager.run()
