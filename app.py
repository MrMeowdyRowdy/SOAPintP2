from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from flask import Flask

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
soap_app = Application([AvailabilityService], 
                        tns='http://luxurystay.com/soap',
                        in_protocol=Soap11(validator='lxml'),
                        out_protocol=Soap11())

wsgi_app = WsgiApplication(soap_app)

# Configuración de Flask
app = Flask(__name__)

@app.before_first_request
def setup_db():
    Base.metadata.create_all(engine)

@app.route("/soap", methods=["POST"])
def soap():
    return wsgi_app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
