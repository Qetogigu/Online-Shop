from ext import app
from routes import index, about, create_product, edit_product, delete_product, registration, authorisation, logout

app.run(debug=True, host='0.0.0.0')

