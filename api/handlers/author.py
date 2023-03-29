from api import app, db, request
from api.models.author import AuthorModel
from api.schemas.author import author_schema, authors_schema
from marshmallow import ValidationError
from api import multi_auth
from utilities.tools import get_object_or_404


# Сериализация:
#      MA       FLASK
# obj ---> dict ---> json
@app.route('/authors', methods=["GET"])
def get_authors():
    authors = AuthorModel.query.all()
    return authors_schema.dump(authors)


@app.route('/authors/<int:author_id>', methods=["GET"])
def get_author_by_id(author_id):
    # author = AuthorModel.query.get(author_id)
    # if not author:
    #     return f"Author id={author_id} not found", 404
    author = get_object_or_404(AuthorModel, author_id)
    return author_schema.dump(author)


@app.route('/authors', methods=["POST"])
@multi_auth.login_required
def create_author():
    json_data = request.json
    try:
        author_data = author_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    author = AuthorModel(**author_data)
    db.session.add(author)
    db.session.commit()
    return author_schema.dump(author), 201


@app.route('/authors/<int:author_id>', methods=["PUT"])
def edit_author(author_id):
    author_data = request.json
    author = get_object_or_404(AuthorModel, author_id)
    author.name = author_data["name"]
    db.session.commit()
    return author_schema.dump(author), 200


@app.route('/authors/<int:author_id>', methods=["PUT"])
def delete_author(quote_id):
    raise NotImplemented("Метод не реализован")
