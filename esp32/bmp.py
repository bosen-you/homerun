from utils.inital import DeviceManager
import urequests, ustruct

def display_bmp_from_url(url):
    print("Downloading image...")
    response = urequests.get(url)
    bmp = response.content
    response.close()

    # BMP 標頭資訊
    data_offset = int.from_bytes(bmp[10:14], 'little')
    width = int.from_bytes(bmp[18:22], 'little')
    height = int.from_bytes(bmp[22:26], 'little')
    bpp = int.from_bytes(bmp[28:30], 'little')

    if width != 128 or height != 64 or bpp != 1:
        print("Unsupported BMP format. Must be 128x64 1-bit.")
        return

    row_size = ((width + 31) // 32) * 4  # BMP 每行四位元對齊

    # 解析並顯示像素（從下到上）
    for y in range(height):
        row = bmp[data_offset + (height - 1 - y) * row_size : data_offset + (height - y) * row_size]
        for x in range(width):
            byte_index = x // 8
            bit_index = 7 - (x % 8)
            bit = (row[byte_index] >> bit_index) & 1
            oled.pixel(x, y, bit)
        oled.show()
    print("Image displayed.")
    
