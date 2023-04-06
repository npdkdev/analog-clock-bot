import asyncio
import datetime
import os
import subprocess
import speedtest

from pyrogram import Client, filters
from pyrogram.enums import ParseMode

import pp_gen

api_id = 99999
api_hash = "000000"

app = Client(
    "khenjiaha",
    api_id=api_id,
    api_hash=api_hash,
)


async def main():
    async with app:

        @app.on_message(filters.command(commands=["ping"], prefixes="!") & filters.me)
        async def ping(client, message):
            # msg: Message
            try:
                speed = speedtest.Speedtest()
                speed.get_best_server()
                speed.download()
                speed.results.share()
                res = speed.results.dict()
            except Exception as e:
                await message.reply_text(f"``chuaaks ngelag`")
                print(e)
                return
            await message.reply_text(f"**PONG!!** `{res['ping'] * 1000:.3f}ms`")

        @app.on_message()
        async def msg(client, message):
            msg = message.text
            if msg == "-nfetch" and message.from_user.is_self is True:
                output = subprocess.check_output(
                    [
                        "neofetch",
                        "--config",
                        "/home/npdk/.config/neofetch/config-stdout.conf",
                        "--stdout",
                    ]
                )
                await message.reply_text(text=output.decode("utf-8"))
            else:
                pass
                # if message.chat.id != -1001473548283:
                #     return
                #
                # if msg is None or len(msg) < 4:
                #     return
                # text = msg.split(" ")
                # if len(text) < 2:
                #     return
                # if text[0] == "/ai":
                #     input = " ".join(text[1:])
                #     reply = await message.reply_text(
                #         "<code>Sabar ya tot...</code>", parse_mode=ParseMode.HTML
                #     )
                #     output = subprocess.check_output(["ask", input])
                #     await reply.edit_text(text=output.decode("utf-8"))
                #

        async def checkUpdate():
            await app.set_profile_photo(photo=pp_gen.gen("clock.png"))

        async def update():
            photos = [p async for p in app.get_chat_photos("me")]
            for pho in photos:
                await app.delete_profile_photos(pho.file_id)
            await asyncio.sleep(1)
            if len(photos) <= 0:
                await checkUpdate()
            else:
                photos = [p async for p in app.get_chat_photos("me")]
                for pho in photos:
                    await app.delete_profile_photos(pho.file_id)
                await checkUpdate()

        async def alwaysUpdate():
            while True:
                now = datetime.datetime.now() + datetime.timedelta(seconds=45)
                timestr = now.strftime("%H:%M")
                await app.update_profile(
                    first_name="Waktu Itu Berharga | ", last_name=timestr
                )
                await update()
                await asyncio.sleep(60)

        await alwaysUpdate()

        # await asyncio.run(profile_picture_loop())


app.run(main())
