from starlette.types import ASGIApp, Message, Scope, Receive, Send

class AuthMiddleware:
    def __init__(self, app: ASGIApp, bypass:list[str]=None) -> None:
        self.app = app
        self.bypass = bypass

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message: Message) -> None:
            # ... Do something
            await send(message)

        await self.app(scope, receive, send_wrapper)