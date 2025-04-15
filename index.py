# .venv\Scripts\activate para activar el entorno virtual

from flask import Flask, render_template
import base64
from flask_sqlalchemy import SQLAlchemy
from PIL import Image  # Requiere `pip install pillow`
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mi_tienda' 
db = SQLAlchemy(app)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

@app.route('/')
def main():
    productos = Productos.query.all()
    for producto in productos:
        if producto.imagen:
            try:
    # Intenta decodificar como base64 primero
                imagen_decodificada = base64.b64decode(producto.imagen)
                img = Image.open(io.BytesIO(imagen_decodificada))
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                producto.imagen = base64.b64encode(buffered.getvalue()).decode('utf-8')
            except:
    # Si falla, trata como binario directo
                try:
                    img = Image.open(io.BytesIO(producto.imagen))
        # ... mismo proceso que arriba
                except Exception as e:
                    print(f"Error en ambos intentos (ID {producto.id}): {e}")
    return render_template('index.html', prods=productos)

@app.route('/producto/<int:producto_id>')
def producto(producto_id):
    productos = Productos.query.get_or_404(producto_id)
    if productos.imagen:
            try:
    # Intenta decodificar como base64 primero
                imagen_decodificada = base64.b64decode(productos.imagen)
                img = Image.open(io.BytesIO(imagen_decodificada))
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG")
                productos.imagen = base64.b64encode(buffered.getvalue()).decode('utf-8')
            except:
    # Si falla, trata como binario directo
                try:
                    img = Image.open(io.BytesIO(productos.imagen))
        # ... mismo proceso que arriba
                except Exception as e:
                    print(f"Error en ambos intentos (ID {productos.id}): {e}")
    return render_template('producto.html', producto=productos)


if __name__ == '__main__':
    app.run(debug=True)