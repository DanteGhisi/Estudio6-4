def get_user(user_id: int, usuarios: list):
    response_usuario = None

    for usuario in usuarios:
        if usuario['id'] == user_id:
            response_usuario = usuario

            break
    
    if response_usuario:
        return response_usuario, 200
    
    return "Usuario no encontrado", 404