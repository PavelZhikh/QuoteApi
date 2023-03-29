from api import app, db, request
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, user_create_schema
from marshmallow import ValidationError
from api import multi_auth
from utilities.tools import get_object_or_404


# url: /users/<int:user_id>
@app.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    # user = UserModel.query.get(user_id)
    return user_schema.dump(user)

# url: /users
@app.route('/users')
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users)

# url: /users
@app.route('/users', methods=["POST"])
@multi_auth.login_required
def create_user():
    user_data = request.json
    try:
        user_data = user_create_schema.load(user_data)
    except ValidationError as err:
        return err.messages, 422

    user = UserModel(**user_data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201