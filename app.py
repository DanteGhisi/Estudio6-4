from flask import Flask, request
import controllers


app = Flask(__name__)

usuarios = [
    { # INDICE 0
        "id": 0,
        "nombre": "Felipe",
        "apellido": "Delicia"
    },
    { # INDICE 1
        "id": 1,
        "nombre": "Dante",
        "apellido": "Delicia"
    },
    { # INDICE 2
        "id": 2,
        "nombre": "Juancito",
        "apellido": "Peralta"
    },
    { # INDICE 3
        "id": 3,
        "nombre": "Felipe",
        "apellido": "Peralta"
    }
]

next_id = len(usuarios)


@app.get('/usuario')
def get_users():
    name = request.args.get('name', '') #Parameter

    resultados = []

    if name:
        for usuario in usuarios:
            if name in usuario['nombre']:
                resultados.append(usuario)
        
        return resultados, 200

    return usuarios, 200

@app.delete('/usuario/<int:user_id>')
def delete_user(user_id: int):
    fueEliminado = False

    for usuario in usuarios:
        if usuario['id'] == user_id:
            usuarios.remove(usuario)
            fueEliminado = True
            break  # Cortamos el for porque ya lo encontramos

    if fueEliminado:
        return "", 200
    
    return "Usuario no encontrado", 404

@app.post('/usuario')
def post_user():
    global next_id
    usuario = request.get_json()

    if not usuario.get("nombre") or not usuario.get("apellido"):
        return "Falta nombre o apellido", 400
    
    usuario['id'] = next_id
    next_id += 1
    usuarios.append(usuario)

    return "", 200

@app.get('/usuario/<int:user_id>')
def get_user(user_id: int):
    return controllers.get_user(user_id, usuarios)

@app.patch('/usuario/<int:user_id>')
def patch_user(user_id: int):
    body = request.get_json() #Body que llega desde el cliente.
    actual = controllers.get_user(user_id, usuarios) # [USUARIO, CODIGO]

    usuario = actual[0]
    status_code = actual[1]

    if status_code == 404:
        return "Usuario no encontrado", 404
    
    if body.get('nombre'):
        usuario['nombre'] = body['nombre']
    
    if body.get('apellido'):
        usuario['apellido'] = body['apellido']
    
    return "", 200

@app.put('/usuario/<int:user_id>')
def put_user(user_id: int):
    body = request.get_json() #Body que llega desde el cliente.

    indice = -1

    for usuario in usuarios:
        if usuario['id'] == user_id:
            indice = usuarios.index(usuario)
            break
    
    if indice == -1:
        return "Usuario no encontrado", 404
    
    usuarios[indice] = body

    return "", 200

# GET, PATCH, PUT, DELETE, POST