from fastapi import FastAPI

def add_middlewares(app: FastAPI):
    
    from .token import add_middleware
    add_middleware(app)
    from .basic import add_middleware
    add_middleware(app)
    from .cookie import add_middleware
    add_middleware(app)
    from .api_key import add_middleware
    add_middleware(app)


__all__ = [
    'add_middlewares'
]