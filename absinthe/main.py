from dotenv import load_dotenv
from hypercorn.config import Config as HyperConfig
from hypercorn.asyncio import serve
from quart import Quart
from api.routes import api_bp
from quart_cors import cors

import asyncio

load_dotenv()

def create_app():
    app = Quart(__name__)
    cors(app, allow_origin="*localhost*") 
    app.register_blueprint(api_bp)
    return app

async def main():
    app = create_app()
    config = HyperConfig()
    config.bind = ["0.0.0.0:9339"]
    config.use_reloader = True
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())
