from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
import re
from user import User
import requests

db = dbase.dbConnection()

app = Flask(__name__)
url = "https://gorest.co.in/public/v2/users"

#Rutas de la aplicación
@app.route('/')
def home():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()          
    #    print("Datos obtenidos:", data)
    users = db['users']
    userssReceived = users.find()
    user = list(userssReceived)
    for valor in data:
        user.append(valor)
    return render_template('index.html', users = user)

#Method Post
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['users']
    id = request.form['id']
    name = request.form['name']
    genero = request.form['genero']
    phone = request.form['phone']
    email = request.form['email']

    if id and name and genero and email and phone:
        patronNombre = "^[0-9]+$"  # El patrón regex para solo números
        if (len(name)> 100 or len(name) < 4 or re.match(patronNombre, name)):
            return redirect(url_for('home', error="Nombre no cumple con los caracteres"))
        elif (len(id) < 4 or len(id) > 11):
            return redirect(url_for('home', error="Nombre no cumple con los caracteres"))
        product = User(id, name, genero,  phone, email)
        products.insert_one(product.toDBCollection())
        response = jsonify({
            'id' : id,
            'name' : name,
            'genero' : genero,
            'phoe' : phone,
            'email' : email
        })
        return redirect(url_for('home'))
    else:
        return notFound()

#Method delete
@app.route('/delete/<string:user_id>')
def delete(user_id):
    users = db['users']
    users.delete_one({'id' : user_id})
    return redirect(url_for('home'))

#Method Put
@app.route('/edit/<string:user_id>', methods=['POST'])
def edit(user_id):
    users = db['users']
    name = request.form['name']
    genero = request.form['genero']
    phone = request.form['phone']
    email = request.form['email']

    if name and genero and email:
        users.update_one({'id' : user_id}, {'$set' : {'name' : name, 'genero' : genero, 'phone': phone,'email' : email}})
        response = jsonify({'message' : 'Señor ' + name + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == '__main__':
    app.run(debug=True, port=4000)