from api import app, db, request
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema, quotes_schema
from api import multi_auth

@app.route('/quotes', methods=["GET"])
def get_quotes():
    quotes = QuoteModel.query.all()
    return quotes_schema.dump(quotes)  # Возвращаем ВСЕ цитаты


@app.route('/authors/<int:author_id>/quotes', methods=["GET"])
def get_author_quotes(author_id):
    author = AuthorModel.query.get(author_id)
    quotes = author.quotes.all()
    return quotes_schema.dump(quotes), 200  # Возвращаем все цитаты автора


@app.route('/quotes/<int:quote_id>', methods=["GET"])
def get_quotes_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is not None:
        return quote_schema.dump(quote), 200
    return {"Error": "Quote not found"}, 404


@app.route('/authors/<int:author_id>/quotes', methods=["POST"])
@multi_auth.login_required
def create_quote(author_id):
    print("user = ", multi_auth.current_user())
    quote_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404
    quote = QuoteModel(author, quote_data["text"])
    db.session.add(quote)
    db.session.commit()
    return quote_schema.dump(quote), 201


@app.route('/quotes/<int:id>', methods=["PUT"])
def edit_quote(quote_id):
    quote_data = request.json
    quote = QuoteModel.query.get(quote_id)
    quote.text = quote_data["text"]
    db.session.commit()
    return quote_schema.dump(quote), 200


@app.route('/quotes/<int:quote_id>', methods=["DELETE"])
def delete_quote(quote_id):
    raise NotImplemented("Метод не реализован")
