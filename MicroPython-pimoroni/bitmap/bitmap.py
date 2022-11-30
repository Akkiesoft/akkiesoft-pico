import struct

"""
Bitmap file decoder for Pimoroni PicoGraphics

example:
    import bitmap
    from picographics import PicoGraphics, DISPLAY_XXX
    display = PicoGraphics(display=DISPLAY_XXX)
    path = "a.bmp"
    bmp = bitmap.bitmap(path, display)
    bmp.decode(x=0, y=0, reverse=False, transparent=-1)

parameters:
    x=0, y=0       : Draw position to the display
    reverse=False  : Reverse color black/white.
    transparent=-1 : Specify 0 or 15 will skip drawing this color.

ref:
    https://ja.wikipedia.org/wiki/Windows_bitmap
    https://qiita.com/cat2151/items/4cc61731732fa644f762
"""

class bitmap:
    def __init__(self, path, display):
        self.path = path
        self.display = display
        self.disp_w, self.disp_h = display.get_bounds()
        self.pallet = []
        with open(self.path, 'rb') as f:
            self.__read_head(f)

    def __read_head(self, f):
        if f.read(2) != b"BM":
            raise Exception ("Not BMP file.")
        self.filesize     = self.__read4bytes(f)
        f.read(4)
        self.__offset     = self.__read4bytes(f)
        self.__headersize = self.__read4bytes(f)
        self.width        = self.__read4bytes(f)
        self.height       = self.__read4bytes(f)
        f.read(2)
        self.bpp          = struct.unpack('h', f.read(2))[0]

        if self.__read4bytes(f):
            raise NotImplementedError("Compressed bitmap is not supported.")
        f.read(12)

        self.colors = self.__read4bytes(f)
        if self.colors != 2:
            raise NotImplementedError("Only 2-color bitmap is supported.")

        # color pallet
        f.seek(14 + self.__headersize)
        for i in range(0, self.colors):
            c = struct.unpack('ssss', f.read(4))
            if c[0] == b'\xff' and c[1] == b'\xff' and c[2] == b'\xff':
                self.pallet.append(15)
            elif c[0] == b'\x00' and c[1] == b'\x00' and c[2] == b'\x00':
                self.pallet.append(0)

    def decode(self, x = 0, y = 0, reverse=False, transparent=-1):
        bit_back = -1
        skip = 0
        line = int(self.width / 8)
        if self.width % 4:
            # math.ceil
            line += 1
        if line % 4:
            skip = 4 - line % 4
        f = open(self.path, 'rb')
        f.seek(self.__offset)
        for iy in reversed(range(0, self.height)):
            py = y + iy
            if py < 0 or self.disp_h <= py:
                f.read(line + skip)
                continue
            for c_byte,byte in enumerate(f.read(line)):
                bits = f'{byte:08b}'
                for c,bit in enumerate(bits):
                    ix = (c_byte * 8) + c
                    if self.width <= ix:
                        break
                    px = x + ix
                    if px < 0 or self.disp_w <= px:
                        continue
                    if bit_back != bit:
                        p = 1 - int(bit) if reverse else int(bit)
                        if self.pallet[p] == transparent:
                            continue
                        self.display.set_pen(self.pallet[p])
                    self.display.pixel(px, py)
                    bit_back = bit
            if skip:
                f.read(skip)
        f.close()

    def __read4bytes(self, f):
        return struct.unpack('i', f.read(4))[0]
