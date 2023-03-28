from api import ma
from api.models.user import UserModel


# Схема сериализации: dict --> json
class UserSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = UserModel
       fields = ('id', 'username')


# Схема десериализации: json --> dict
class UserCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    username = ma.String(required=True)
    password = ma.String(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_create_schema = UserCreateSchema()