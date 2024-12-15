Para lanzar el proyecto en una terminal y dentro de la carpeta del mismo ejecutar:

docker build -t soap-service .

docker run -d -p 5000:5000 --name soap-container soap-service

Se puede acceder al servicio a través de 

http://localhost:5000/soap?wsdl

Pruebas
Puedes probar el servicio SOAP utilizando herramientas como Postman o clientes llamando al endpoint getAvailability con parámetros como:

start_date: "2024-12-15"
end_date: "2024-12-17"
room_type: "Single"

Esto devolverá una respuesta en formato XML con la lista de habitaciones disponibles.