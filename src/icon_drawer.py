from PIL import Image, ImageDraw, ImageFont
import os

class IconDrawer:
    def __init__(self, thresholds: dict = None):
        self.thresholds = thresholds or {"good": 50, "moderate": 110, "bad": 180}
        self.font = self._load_best_font()

    def _load_best_font(self):
        # Search for standard crisp Windows fonts
        font_candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf",  # Segoe UI Bold
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",   # Arial Bold
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
        ]
        for fpath in font_candidates:
            if os.path.exists(fpath):
                try:
                    return ImageFont.truetype(fpath, size=34)
                except Exception:
                    pass
        return ImageFont.load_default()

    def _get_status_color(self, ping: float | None, loss: float = 0.0):
        if ping is None or loss >= 20.0:
            # Disconnected / Timeout / High Loss
            return (239, 68, 68, 255), (185, 28, 28, 255)  # Bright Red / Dark Red
        
        good = self.thresholds.get("good", 50)
        mod = self.thresholds.get("moderate", 110)
        bad = self.thresholds.get("bad", 180)

        if ping < good:
            return (16, 185, 129, 255), (5, 150, 105, 255)   # Emerald Green
        elif ping < mod:
            return (245, 158, 11, 255), (217, 119, 6, 255)   # Amber Yellow
        elif ping < bad:
            return (249, 115, 22, 255), (234, 88, 12, 255)   # Orange
        else:
            return (239, 68, 68, 255), (185, 28, 28, 255)   # Red

    def create_tray_icon(self, ping: float | None, loss: float = 0.0, show_number: bool = True) -> Image.Image:
        size = 64
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        primary_color, secondary_color = self._get_status_color(ping, loss)

        # Draw outer rounded background pill / badge
        margin = 3
        draw.rounded_rectangle(
            [(margin, margin), (size - margin, size - margin)],
            radius=18,
            fill=(18, 20, 26, 240),      # Dark modern background
            outline=primary_color,        # Accent color border
            width=4
        )

        if not show_number:
            # Draw solid circular indicator
            dot_margin = 16
            draw.ellipse(
                [(dot_margin, dot_margin), (size - dot_margin, size - dot_margin)],
                fill=primary_color
            )
            return image

        # Determine text to render
        if ping is None:
            text = "✕"
            text_color = (239, 68, 68, 255)
        elif ping >= 999:
            text = "999"
            text_color = primary_color
        else:
            text = str(int(round(ping)))
            text_color = primary_color

        # Dynamic font sizing based on string length
        font_size = 34 if len(text) <= 2 else (26 if len(text) == 3 else 20)
        try:
            # Try to get dynamically sized font if possible
            for fpath in [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"]:
                if os.path.exists(fpath):
                    font = ImageFont.truetype(fpath, size=font_size)
                    break
            else:
                font = self.font
        except Exception:
            font = self.font

        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (size - text_w) / 2
        y = (size - text_h) / 2 - 4

        draw.text((x, y), text, font=font, fill=text_color)
        return image
