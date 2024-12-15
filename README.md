Para lanzar el proyecto en una terminal y dentro de la carpeta del mismo ejecutar:

docker build -t soap-service .

docker run -d -p 5000:5000 --name soap-container soap-service

Se puede acceder al servicio a través de 

http://localhost:5000/soap?wsdl