from gfx_pack import GfxPack
import bitmap

gp = GfxPack()
display = gp.display
display.set_backlight(0.4)

image = bitmap.bitmap("/uhatporter.bmp", display)
image.decode(x=-35, y=-45, reverse=True)
display.update()