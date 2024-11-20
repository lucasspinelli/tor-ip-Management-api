from app import create_app
from app.database import init_db
from app.logging_config import setup_logger

app = create_app()

setup_logger()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
