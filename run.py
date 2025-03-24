import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'default'))


print(app.url_map)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))