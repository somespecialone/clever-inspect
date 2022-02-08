from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:

    class AsyncSession(AsyncSession):
        def add(self, instance, _warn=True):
            """Place an object in the ``Session``.

            Its state will be persisted to the database on the next flush
            operation.

            Repeated calls to ``add()`` will be ignored. The opposite of ``add()``
            is ``expunge()``.

            """
