# API para manejo de pedidos de un restaurante

Ofrece la solicitud de pedidos por parte de clientes registrados,
la asignación (aleatoria) de repartidores encargados de las entregas y 
el inventario de los productos ofrecidos por el restaurante.

A continuación las funcionalidades por tipo de usuario:

## Administrador

- Administración completa de productos y líneas de productos.
- Consulta de los pedidos recibidos.

## Cliente

- Consulta de productos ofrecidos.
- Creación y actualización de pedidos de acuerdo con los productos disponibles.
- Cancelación de pedidos.

## Repartidor

- Consulta y actualización de estado de pedidos asignados.


# Requisitos de ejecución

1. Crea un archivo `.env` en la raíz del proyecto siguiendo el ejemplo de `env_example.txt`.

2. Para inicializar el entorno virtual, instalar todas las dependencias, poblar la base de datos con datos iniciales y ejecutar la api, realice los siguientes comandos:

    ~~~bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    python seeding.py
    uvicorn main:app --port 8000
    ~~~

    > **Nota:** El puerto es de su elección.

    > **Importante:** No debe existir ningún archivo `.sqlite` inicialmente para una creación limpia de la base de datos.

    Para realizar pruebas, tendrá cuatro usuarios con los siguientes emails:

    - *admin@mail.com*
    - *client1@mail.com*
    - *client2@mail.com*
    - *delivery@mail.com*

    Todos poseen la misma contraseña: *12345678*

3. Para acceder a la documentación generada por la librería FASTAPI, ingrese en el navegador la url [http://localhost:8000/docs](http://localhost:8000/docs)

    > **Importante:** Para probar los endpoints, es necesario iniciar sesión con alguno de los usuarios existentes, esto por medio del endpoint **'/login'**.
