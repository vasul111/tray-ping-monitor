import os
from PIL import Image, ImageDraw, ImageFont

class IconDrawer:
    def __init__(self, thresholds: dict = None):
        self.thresholds = thresholds or {"good": 50, "moderate": 110, "bad": 180}
        self.font = self._find_font()

    def _find_font(self):
        candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf"
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size=32)
                except Exception:
                    pass
        return ImageFont.load_default()

    def _get_colors(self, ping: float | None, loss: float = 0.0):
        if ping is None or loss >= 15.0:
            return (239, 68, 68, 255)  # Red (timeout/drop)

        good = self.thresholds.get("good", 50)
        mod = self.thresholds.get("moderate", 110)
        bad = self.thresholds.get("bad", 180)

        if ping < good:
            return (16, 185, 129, 255)  # Green
        elif ping < mod:
            return (245, 158, 11, 255)  # Amber
        elif ping < bad:
            return (249, 115, 22, 255)  # Orange
        return (239, 68, 68, 255)       # Red

    def create_tray_icon(self, ping: float | None, loss: float = 0.0, show_number: bool = True) -> Image.Image:
        size = 64
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        accent = self._get_colors(ping, loss)

        # Background rounded badge
        pad = 2
        draw.rounded_rectangle(
            [(pad, pad), (size - pad, size - pad)],
            radius=16,
            fill=(15, 17, 23, 245),
            outline=accent,
            width=4
        )

        if not show_number:
            draw.ellipse([(18, 18), (46, 46)], fill=accent)
            return image

        if ping is None:
            text = "✕"
        elif ping >= 999:
            text = "999"
        else:
            text = str(int(round(ping)))

        font_size = 32 if len(text) <= 2 else (24 if len(text) == 3 else 18)
        try:
            for path in [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"]:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, size=font_size)
                    break
            else:
                font = self.font
        except Exception:
            font = self.font

        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (size - tw) / 2
        y = (size - th) / 2 - 3

        draw.text((x, y), text, font=font, fill=accent)
        return image
