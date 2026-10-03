import logging

import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.auth import AuthContext, User
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from app.models import AdminBootstrapLock, UserAccount


async def ensure_account(sub: str, email: str, name: str) -> str:
    async with rx.asession() as session:
        async with session.begin():
            await session.execute(
                insert(UserAccount)
                .values(
                    sub=sub, email=email[:320], name=name[:255], role="member"
                )
                .on_conflict_do_nothing(index_elements=[UserAccount.sub])
            )
            claimed = await session.scalar(
                insert(AdminBootstrapLock)
                .values(id=1, admin_sub=sub)
                .on_conflict_do_nothing(index_elements=[AdminBootstrapLock.id])
                .returning(AdminBootstrapLock.admin_sub)
            )
            if claimed:
                await session.execute(
                    update(UserAccount)
                    .where(UserAccount.sub == sub)
                    .values(role="admin")
                )
            role = await session.scalar(
                select(UserAccount.role).where(UserAccount.sub == sub)
            )
    return str(role or "member")


class RoleState(rx.State):
    role: str = rxe.field("member", auth=False)

    @rxe.event(auth=False, background=True)
    async def refresh_current_role(self):
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            async with self:
                self.role = "member"
            return
        email = str(claims.get("email", ""))[:320]
        name = str(claims.get("name", ""))[:255]
        try:
            role = await ensure_account(sub, email, name)
            async with self:
                self.role = role
        except Exception as e:
            logging.exception(f"Error: {e}")
            async with self:
                self.role = "member"


async def is_admin(ctx: AuthContext) -> bool:
    claims = await User.current() or {}
    sub = str(claims.get("sub", "")).strip()
    if not sub:
        return False
    async with rx.asession() as session:
        role = await session.scalar(
            select(UserAccount.role).where(UserAccount.sub == sub)
        )
    return role == "admin"
