from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from flask import Flask, request, Response

# Configuración de la base de datos
DATABASE_URL = 'sqlite:///availability.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Modelo de la tabla availability
class Availability(Base):
    __tablename__ = 'availability'
    room_id = Column(Integer, primary_key=True)
    room_type = Column(String, nullable=False)
    available_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

# Servicio SOAP
class AvailabilityService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def get_availability(ctx, start_date, end_date, room_type):
        try:
            # Conversión de fechas
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Consulta a la base de datos
            available_rooms = session.query(Availability).filter(
                Availability.room_type == room_type,
                Availability.available_date.between(start_date, end_date),
                Availability.status == 'available'
            ).all()

            # Generar respuesta en XML
            for room in available_rooms:
                yield f"<room><id>{room.room_id}</id><type>{room.room_type}</type><date>{room.available_date}</date><status>{room.status}</status></room>"

        except Exception as e:
            yield f"<error>{str(e)}</error>"

# Configuración de la aplicación SOAP
soap_app = Application(
    [AvailabilityService],
    tns='http://luxurystay.com/soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)

# Configuración de Flask
app = Flask(__name__)

# Configuración de la base de datos y datos de prueba
with app.app_context():
    # Crear la estructura de la base de datos
    Base.metadata.create_all(engine)

    # Insertar datos de prueba si la tabla está vacía
    if not session.query(Availability).first():
        sample_data = [
            Availability(room_id=1, room_type='Single', available_date=datetime(2024, 12, 15).date(), status='available'),
            Availability(room_id=2, room_type='Double', available_date=datetime(2024, 12, 15).date(), status='maintenance'),
            Availability(room_id=3, room_type='Suite', available_date=datetime(2024, 12, 16).date(), status='available'),
            Availability(room_id=4, room_type='Single', available_date=datetime(2024, 12, 17).date(), status='available'),
            Availability(room_id=5, room_type='Double', available_date=datetime(2024, 12, 17).date(), status='available'),
        ]
        session.add_all(sample_data)
        session.commit()
        print("Datos de prueba insertados.")

@app.route("/soap", methods=["POST", "GET"])
def soap():
    if request.method == "GET":
        # Delegar la solicitud GET al WsgiApplication para generar el WSDL
        environ = request.environ.copy()
        environ['QUERY_STRING'] = 'wsdl'

        def start_response(status, headers):
            """Callable WSGI start_response"""
            response_headers = [(key, value) for key, value in headers]
            response_headers.append(('Content-Type', 'application/xml'))
            return Response(status=status, headers=response_headers)

        response = wsgi_app(environ, start_response)
        return Response(response, content_type="application/xml")
    else:
        # Manejar solicitudes SOAP normales
        return wsgi_app



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
