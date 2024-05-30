import math
import os
import time
import json
from main.plugins.helpers import TimeFormatter, humanbytes

FINISHED_PROGRESS_STR = "🟩"
MID_PROGRESS_STR = "🟨"
START_PROGRESS_STR = "🟥"
UN_FINISHED_PROGRESS_STR = "⬜️"
DOWNLOAD_LOCATION = "/app"

PROGRESS_SYMBOLS = {
    '🟥': (0, 30),
    '🟨': (30, 55),
    '🟧': (55, 80),
    '🟩': (80, 100),
}

async def progress_for_pyrogram(
    current,
    total,
    bot,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        status = DOWNLOAD_LOCATION + "/status.json"
        if os.path.exists(status):
            with open(status, 'r+') as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        # Find the appropriate symbol based on the progress range
        symbol = next((sym for sym, (start_range, end_range) in PROGRESS_SYMBOLS.items() if start_range <= percentage < end_range), '')

        num_segments = 10
        completed_segments = math.floor(percentage / (100 / num_segments))
        unfinished_segments = num_segments - completed_segments

        # Modified construction of the progress string
        progress = "**[{0}{1}]** | {2}%\n\n".format(
            ''.join([symbol for _ in range(completed_segments)]),
            ''.join([UN_FINISHED_PROGRESS_STR for _ in range(unfinished_segments)]),
            round(percentage, 2))

        tmp = progress + "📥 SIZE ➤ {0} of {1}\n\n⚡ SPEED ➤ {2}/s\n\n⏳ ETA ➤ {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            if not message.photo:
                await message.edit_text(
                    text="{}\n {}".format(
                        ud_type,
                        tmp
                    )
                )
            else:
                await message.edit_caption(
                    caption="{}\n {}".format(
                        ud_type,
                        tmp
                    )
                )
        except:
            pass
