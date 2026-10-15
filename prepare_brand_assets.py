"""Build web-ready brand assets from the approved Mock Interactive artwork."""

from pathlib import Path

from PIL import Image


PROJECT = Path(__file__).resolve().parent
STYLING = PROJECT.parent.parent / "Styling" / "Themes"
LOGOS = PROJECT.parent.parent / "Styling" / "Logos"
OUTPUT = PROJECT / "static" / "images" / "brand"
OUTPUT.mkdir(parents=True, exist_ok=True)


def export_background() -> None:
    source = STYLING / "Backgrounds" / "Mock_Interactive_Ember_Crown_Castle_Symmetrical.png"
    with Image.open(source) as image:
        hero = image.convert("RGB")
        hero.save(OUTPUT / "ember-crown-world.webp", "WEBP", quality=95, method=6)


def export_supporting_backgrounds() -> None:
    sources = {
        "mountain-relief.webp": STYLING / "Backgrounds" / "Mock_Interactive_Menu_Background_Mountain_Relief_4K.png",
        "expedition-map.webp": STYLING / "Backgrounds" / "Mock_Interactive_Menu_Background_Expedition_Map_4K.png",
        "compass-atlas.webp": STYLING / "Backgrounds" / "Mock_Interactive_Menu_Background_Compass_Atlas_4K.png",
        "ember-foundry.webp": STYLING / "Future" / "Mock_Interactive_Theme_Option_4_Ember_Foundry_4K.png",
    }
    for output_name, source in sources.items():
        with Image.open(source) as image:
            image.convert("RGB").save(OUTPUT / output_name, "WEBP", quality=86, method=6)


def export_wordmark() -> None:
    source = STYLING / "Mock_Interactive_Wordmark.png"
    with Image.open(source) as image:
        mark = image.convert("RGBA").crop((165, 60, 1605, 455))
        pixels = mark.load()
        for y in range(mark.height):
            for x in range(mark.width):
                red, green, blue, _ = pixels[x, y]
                brightness = max(red, green, blue)
                if brightness <= 5:
                    alpha = 0
                elif brightness >= 60:
                    alpha = 255
                else:
                    alpha = round((brightness - 5) / 55 * 255)
                pixels[x, y] = (red, green, blue, alpha)
        mark.save(OUTPUT / "mock-interactive-wordmark.png", optimize=True)


def export_site_icons() -> None:
    """Create crisp square browser and search icons from the approved disc logo."""
    source = LOGOS / "Mock_Interactive_Logo_2_4096_px.png"
    with Image.open(source) as image:
        disc = image.convert("RGBA")
        alpha_box = disc.getchannel("A").getbbox()
        if alpha_box:
            disc = disc.crop(alpha_box)

        def render(size: int) -> Image.Image:
            canvas = Image.new("RGBA", (size, size), (5, 5, 5, 255))
            maximum = (round(size * 0.94), round(size * 0.94))
            icon = disc.copy()
            icon.thumbnail(maximum, Image.Resampling.LANCZOS)
            position = ((size - icon.width) // 2, (size - icon.height) // 2)
            canvas.alpha_composite(icon, position)
            return canvas.convert("RGB")

        for size in (48, 192, 512):
            render(size).save(OUTPUT / f"favicon-{size}.png", optimize=True)
        render(180).save(OUTPUT / "apple-touch-icon.png", optimize=True)
        render(256).save(
            PROJECT / "static" / "favicon.ico",
            format="ICO",
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        )


if __name__ == "__main__":
    export_background()
    export_supporting_backgrounds()
    export_wordmark()
    export_site_icons()
