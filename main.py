import asyncio
from src.GameManager import GameManager


async def main():
    game_manager = GameManager()
    await game_manager.start_application()


if __name__ == "__main__":
    asyncio.run(main())
