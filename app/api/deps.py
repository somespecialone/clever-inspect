import re
from typing import Generator, Optional


from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

from ..db import engine, AsyncSession


async def get_session() -> Generator[AsyncSession, None, None]:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        session: AsyncSession
        try:
            yield session
        finally:
            await session.close()


class ItemInspectParams:
    def __init__(
        self,
        url: Optional[str] = None,
        s: Optional[int] = 0,
        a: Optional[int] = None,
        d: Optional[int] = None,
        m: Optional[int] = 0,
    ) -> None:
        self.s: int
        self.a: int
        self.d: int
        self.m: int

        self._parse_url(url) if url else self._parse_params(s, a, d, m)

    def _parse_url(self, url: str):
        try:
            search = re.search(r"[SM](\d+)A(\d+)D(\d+)$", url)

            self.s = int(search[1]) if search[0].startswith("S") else 0
            self.m = int(search[1]) if search[0].startswith("M") else 0
            self.a = int(search[2])
            self.d = int(search[3])

        except (TypeError, IndexError, ValueError):
            raise HTTPException(400, "Invalid inspect link")

    def _parse_params(self, s: int, a: int, d: int, m: int) -> None:
        if not s and not m:
            raise HTTPException(400, f"Missing required keyword-only argument: {'s' if not s else 'm'}")
        if not d or not a:
            raise HTTPException(400, f"Missing required keyword-only argument: {'d' if not d else 'a'}")

        self.s, self.m, self.a, self.d = s, m, a, d

    def dict(self) -> dict[str, int]:
        return {
            "s": self.s,
            "a": self.a,
            "d": self.d,
            "m": self.m,
        }
