import asyncio
from services.brw_api import BRWAPI


async def main():
    brw = BRWAPI()
    schedule = await brw.get_schedule_for_date("Пинск", "Минск", "2025-01-01")
    print(schedule)

if __name__ == '__main__':
    asyncio.run(main())
