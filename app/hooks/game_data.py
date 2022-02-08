from app.services import game_data


async def game_data_startup():
    await game_data.load()
