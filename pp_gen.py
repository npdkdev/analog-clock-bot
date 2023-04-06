import datetime
import math

from PIL import Image, ImageDraw, ImageFont


def gen(dest="clock.png"):
    # Get Current Time
    now = datetime.datetime.now()

    def color():
        maghrib = ["#004D47", "#EFD26E", "#B3903E", "#FFFFFF"]
        malem = ["#021B31", "#042036", "#FFC36D", "#FFFFFF"]
        subuh = ["#7C2A5A", "#CF9738", "#EED674", "#FFFFFF"]
        siang = ["#FBF3EA", "#C88931", "#C88931", "#021B31"]

        hour = now.time().hour
        # hour = 18
        if hour >= 18:
            return maghrib
        elif hour >= 12:
            return siang
        elif hour >= 4:
            return subuh
        else:
            return malem

    # Create Image
    img = Image.new("RGB", (600, 600), color=color()[0])

    # Create Draw Object
    d = ImageDraw.Draw(img)

    # Define font
    font_number = ImageFont.truetype("font/KetupatFree.ttf", 30)
    font_text = ImageFont.truetype("font/KetupatFree.ttf", 45)
    font_text3 = ImageFont.truetype("font/Dabir.ttf", 20)
    font = ImageFont.truetype("font/Philosopher.ttf", 20)
    font_text2 = ImageFont.truetype("font/BerkshireSwash.ttf", 26)

    # Define center of the clock
    center = (img.width / 2, img.height / 2)

    # Define Hour, Minute, Second Hands
    hour_hand_length = img.width / 4
    minute_hand_length = img.width / 3.5
    second_hand_length = img.width / 2.5

    def render_text(pos, text, font, col):
        cx = center[0]
        cy = center[1] + 30
        cbbox = d.textbbox((0, 0), text, font=font)
        cw = cbbox[2] - cbbox[0]
        ch = cbbox[3] - cbbox[1]
        cx -= cw / 2
        cy -= ch / 2
        d.text((cx + pos[0], cy + pos[1]), text, font=font, fill=col)

    # Draw center name
    hijriah = "1444H / 2023M"
    bykhenji = "KHenjiah by @npdk.me"
    ramadhan = "Ramadhan"
    # cx = center[0]
    # cy = center[1] + 30
    # cbbox = d.textbbox((0, 0), ramadhan, font=font_text)
    # cw = cbbox[2] - cbbox[0]
    # ch = cbbox[3] - cbbox[1]
    # cx -= cw / 2
    # cy -= ch / 2
    render_text((0, -110), ramadhan, font_text, color()[2])
    render_text((0, 20), bykhenji, font_text2, color()[2])
    render_text((0, 100), hijriah, font, color()[2])

    # d.text((cx, cy), "Ramadhan", font=font_text, fill=color()[2])
    # d.text((cx, cy+30), "Ramadhan", font=font_text2, fill=color()[2])
    # d.text((cx, cy+60), "Ramadhan", font=font, fill=color()[1])
    # d.text((cx, cy+60), "KHenjiah by @npdk.me", font=font_text2, fill=color()[2])
    # d.text((cx, cy+90), "1444 H/ 2023 M", font=font, fill=color()[2])
    # d.text((center[0] // 2, center[1] // 2), "KHenjiahh", font=font, fill=color()[2])

    # Draw Clock
    for i in range(60):
        angle = math.radians(i * 6)
        offset = 20 if i % 5 == 0 else 10
        d.line(
            [
                (
                    center[0] + math.sin(angle) * (second_hand_length - offset),
                    center[1] - math.cos(angle) * (second_hand_length - offset),
                ),
                (
                    center[0] + math.sin(angle) * second_hand_length,
                    center[1] - math.cos(angle) * second_hand_length,
                ),
            ],
            fill=color()[3],
            width=5,
        )

    # Hour Hand
    hour_angle = math.radians((now.hour % 12) * 30 + (now.minute / 2))
    d.line(
        [
            (center[0], center[1]),
            (
                center[0] + math.sin(hour_angle) * hour_hand_length,
                center[1] - math.cos(hour_angle) * hour_hand_length,
            ),
        ],
        fill=color()[3],
        width=9,
    )

    # Minute Hand
    minute_angle = math.radians(now.minute * 6)
    d.line(
        [
            (center[0], center[1]),
            (
                center[0] + math.sin(minute_angle) * minute_hand_length,
                center[1] - math.cos(minute_angle) * minute_hand_length,
            ),
        ],
        fill=color()[3],
        width=5,
    )

    # Second Hand
    # second_angle = math.radians(now.second * 6)
    # d.line([(center[0], center[1]),
    # 		(center[0] + math.sin(second_angle) * second_hand_length,
    # 		 center[1] - math.cos(second_angle) * second_hand_length)],
    # 	   fill=(255, 0, 0, 255), width=2)
    # Add Numbers to Clock
    for i in range(1, 13):
        angle = math.radians(i * 30)
        # w, h = d.textsize(str(i), font=font)
        # x = center[0] + math.sin(angle) * (second_hand_length - 30) - w / 2
        # y = center[1] - math.cos(angle) * (second_hand_length - 30) - h / 2
        # d.text((x, y), str(i), font=font, fill='black')

        # angle = math.pi * 2 / 12 * i
        x = center[0] + math.sin(angle) * (second_hand_length - 40)
        y = center[1] - math.cos(angle) * (second_hand_length - 40)
        bbox = d.textbbox((0, 0), str(i), font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x -= w / 2
        y -= h / 2
        d.text((x - 3, y - 13), str(i), font=font_number, fill=color()[2])

    d.ellipse(
        (center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5), fill=color()[3]
    )

    # Display or Save the Image
    # img.show()
    img.save("clock.png")
    return dest
