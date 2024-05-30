try:
    from flask_cors import CORS
    print("Flask-CORS está correctamente instalado y disponible.")
except ImportError:
    print("Flask-CORS no está instalado o no se puede encontrar.")
