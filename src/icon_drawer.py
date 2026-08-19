import os
from PIL import Image, ImageDraw, ImageFont

class IconDrawer:
    def __init__(self, thresholds: dict = None):
        self.thresholds = thresholds or {"good": 50, "moderate": 110, "bad": 180}

    def _get_font(self, size: int):
        candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\consola.ttf",
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size=size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def _get_color(self, ping: float | None, loss: float = 0.0):
        if ping is None or loss >= 15.0:
            return (255, 75, 75, 255)  # Crimson Red

        good = self.thresholds.get("good", 50)
        mod = self.thresholds.get("moderate", 110)
        bad = self.thresholds.get("bad", 180)

        if ping < good:
            return (0, 230, 118, 255)    # Vibrant Emerald Green
        elif ping < mod:
            return (255, 193, 7, 255)    # Amber Yellow
        elif ping < bad:
            return (255, 112, 67, 255)   # Coral Orange
        return (255, 75, 75, 255)        # Red

    def create_tray_icon(self, ping: float | None, loss: float = 0.0, style: str = "badge") -> Image.Image:
        # Render at 256x256 and downscale with Lanczos for ultra-crisp antialiasing
        canvas_size = 256
        img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        accent = self._get_color(ping, loss)

        if style == "dot":
            dot_pad = 48
            draw.ellipse(
                [(dot_pad, dot_pad), (canvas_size - dot_pad, canvas_size - dot_pad)],
                fill=accent
            )
            return img.resize((64, 64), Image.Resampling.LANCZOS)

        if style == "badge":
            pad = 8
            draw.rounded_rectangle(
                [(pad, pad), (canvas_size - pad, canvas_size - pad)],
                radius=64,
                fill=(16, 18, 24, 250),
                outline=accent,
                width=16
            )

        # Draw number / text
        if ping is None:
            text = "X"
        elif ping >= 999:
            text = "999"
        else:
            text = str(int(round(ping)))

        font_size = 145 if len(text) <= 2 else (110 if len(text) == 3 else 85)
        font = self._get_font(font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (canvas_size - tw) / 2
        y = (canvas_size - th) / 2 - 12

        draw.text((x, y), text, font=font, fill=accent)

        return img.resize((64, 64), Image.Resampling.LANCZOS)
