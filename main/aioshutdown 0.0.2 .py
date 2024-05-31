import asyncio
from aioshutdown import SIGTERM, SIGINT, SIGHUP
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

async def my_task(sleep: int):
    try:
        while True:
            logging.info("Sleep from task #%s", sleep)
            await asyncio.sleep(sleep)
    except asyncio.CancelledError as exc:
        # Received an exit signal. In this place we gracefully complete the work.
        signal = exc.args[0] # NOTE: works in Python >= 3.9 only: https://docs.python.org/3/library/asyncio-future.html?highlight=Changed%20in%20version%203.9:%20Added%20the%20msg%20parameter.#asyncio.Future.cancel
        logging.warning("Received %s signal. Shutting down...", signal.value)

# Usage with `run_forever`

with SIGTERM | SIGHUP | SIGINT as loop:
    tasks = [loop.create_task(my_task(i)) for i in range(1, 10)]
    loop.run_forever()

# Usage with `run_until_complete`

with SIGTERM | SIGHUP | SIGINT as loop:
    tasks = [loop.create_task(my_task(i)) for i in range(1, 10)]
    loop.run_until_complete(asyncio.gather(*results))