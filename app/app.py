from flask import Flask, jsonify, request, Response
from BookModel import *
from settings import *
import json
import os

import jwt, datetime

# Configure a key
app.config['SECRET_KEY'] = 'meow'

#books = [
#    {
#        'name': 'Green Eggs and Ham',
#        'price': 7.99,
#        'isbn': 978039400165
#    },
#    {
#        'name': 'The Cat in the Hat',
#        'price': 6.99,
#        'isbn': 9782371000193
#    }
#]

#update 1
@app.route('/login')
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/')
def hello_world():
    return 'Hello World!'
    
#GET /books
@app.route('/books')
def get_books():
    token = request.args.get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({'error': 'Need a valid token to view this page'}), 401
    return jsonify({'books': Book.get_all_books()})
    
#Define valid book object
def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

#POST /books
@app.route('/books', methods=['POST'])
def add_book():
    #return jsonify(request.get_json())
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Try a valid format? =)"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
    
@app.route('/books/<int:isbn>')
def get_books_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)
    

#PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()

   #if(not valid_put_request_data(request_data)):
   #    invalidBookObjectErrorMsg = {
   #        "error": "Valid book must be passed in the request",
   #        "helpstring": "Require name and price. ISBN is the URL"
   #    }
   #    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
   #    return response
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number was not found, thus unable to delete"
    }    
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

    
if __name__ == '__main__':
#    app.run(host="0.0.0.0", debug = True, port=8000) #need to use local host of your machine (cmd > ipconfig) #correct
    app.run(host="127.0.0.1", debug = True, port=8000) #need to use local host of your machine (cmd > ipconfig)  #incorrect
