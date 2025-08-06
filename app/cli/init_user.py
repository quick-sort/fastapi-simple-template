import argparse
import logging

from app.db.models.user import User, UserRole
from app.db.session import ASYNC_DB_SESSION

logger = logging.getLogger(__name__)


async def init_user(args):
    async with ASYNC_DB_SESSION() as session:
        await User.create(
            async_session=session,
            username=args.username,
            email=args.email,
            password=args.password,
            roles=[UserRole(args.role)],
        )
        await session.commit()
    logger.info(f"{args.role} user: {args.username}: {args.email} created")


def registry_command(parser: argparse.ArgumentParser):
    init_user_parser = parser.add_parser("init-user", help="Initialize user")
    init_user_parser.set_defaults(func=init_user)
    init_user_parser.add_argument("--username", help="Username", required=True)
    init_user_parser.add_argument("--email", help="Email", required=True)
    init_user_parser.add_argument("--password", help="Password", required=True)
    init_user_parser.add_argument(
        "--role", help="Role", choices=UserRole, default=UserRole.user
    )
    return init_user_parser
