Para lanzar el proyecto en una terminal y dentro de la carpeta del mismo ejecutar:

docker build -t soap-service .

docker run -d -p 5000:5000 --name soap-container soap-service

Se puede acceder al servicio a través de 

http://localhost:5000/soap?wsdl

Pruebas
Puedes probar el servicio SOAP utilizando herramientas como Postman o clientes llamando al endpoint getAvailability con parámetros como:

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://luxurystay.com/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <tns:get_availability>
            <tns:start_date>2024-12-15</tns:start_date>
            <tns:end_date>2024-12-17</tns:end_date>
            <tns:room_type>Single</tns:room_type>
        </tns:get_availability>
    </soapenv:Body>
</soapenv:Envelope>

obteneiendo una respuesta:

<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://luxurystay.com/soap">
    <soap11env:Body>
        <tns:get_availabilityResponse>
            <tns:get_availabilityResult>
                <tns:string>&lt;room&gt;&lt;id&gt;1&lt;/id&gt;&lt;type&gt;Single&lt;/type&gt;&lt;date&gt;2024-12-15&lt;/date&gt;&lt;status&gt;available&lt;/status&gt;&lt;/room&gt;</tns:string>
                <tns:string>&lt;room&gt;&lt;id&gt;4&lt;/id&gt;&lt;type&gt;Single&lt;/type&gt;&lt;date&gt;2024-12-17&lt;/date&gt;&lt;status&gt;available&lt;/status&gt;&lt;/room&gt;</tns:string>
            </tns:get_availabilityResult>
        </tns:get_availabilityResponse>
    </soap11env:Body>
</soap11env:Envelope>