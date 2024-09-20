import asyncio
from hypercorn.config import Config as HyperConfig
from hypercorn.asyncio import serve
from quart import Quart
from api.routes import api_bp

def create_app():
    app = Quart(__name__)
    app.register_blueprint(api_bp)
    return app

async def main():
    app = create_app()
    config = HyperConfig()
    config.bind = ["127.0.0.1:5000"]
    config.use_reloader = True
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())