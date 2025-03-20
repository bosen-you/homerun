from utils import *
import os
from scipy.io import wavfile
from machine import Pin,SoftI2C
import ssd1306  

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)  #Init i2c
lcd = ssd1306.SSD1306_I2C(128,64,i2c)    

if __name__ == '__main__':
    try:
        action = int(input("輸入數字就好了\n1. transform\n2. compare\n3. encode\n4. decode\n"))
        if action == 1:
            lcd.fill(0)
            lcd.text("transform", 20, 52)       #set "" at (0,0)
            lcd.show()#display
            rate, audio, path = select_audio_file()
            waveform_img_path = os.path.join(path, "waveform.png")
            spectrum_img_path = os.path.join(path, "spectrum.png")

            # 繪製並顯示+儲存波形圖
            plot_waveform(audio, audio, rate, "Waveform Watermark", "encode", save_path=waveform_img_path)
            print(f"波形圖已保存至: {waveform_img_path}")
            
            # 繪製並顯示+儲存頻譜圖
            plot_frequency_spectrum(audio, rate, "Original Audio", save_path=spectrum_img_path)
            print(f"頻譜圖已保存至: {spectrum_img_path}")
            lcd.text('successfully', 5, 16)
            lcd.show()#display
        
        elif action == 2:
            lcd.fill(0)
            lcd.text("compare", 20, 52)       #set "" at (0,0)
            lcd.show()#display
            
            path1 = select_audio_file_path()
            path2 = select_audio_file_path()

            cho = int(input('輸入數字就好了\n1. 顯示數據比較\n2. 顯示圖片比較\n'))
            if cho == 1:
                lcd.text("data analysis", 5, 16)
                lcd.show()
                final = compare_audio(path1, path2)
                l = ['0% ~ 0%\nRisk-free', '20% ~ 40%\nSecure', '40% ~ 60%\nModerate', '60% ~ 80%\nDangerous', '80% ~ 100%\nHazardous']
                rate_check = [[0, 0], [20, 40], [40, 60], [60, 80], [80, 101]]
                
                for i in range(5):
                    if rate_check[i][1] > final >= rate_check[i][0]:
                        lcd.text(l[i], 10, 32)
                        break
                    
            elif cho == 2:
                lcd.text("graph analysis", 5, 16)
                chose = input('輸入數字就好了\n1. 波型圖\n2. 頻譜圖\n')
                if chose == '1':
                    lcd.text('waveform', 10, 32)
                    plot_waveform(path1, path2)
                elif chose == '2':
                    lcd.text('frequency form', 10, 32)
                    plot_spectrogram(path1, path2)
                else:
                    lcd.text("input format error", 10, 32)
                    lcd.show()
                    exit(1)
            else: 
                lcd.text('input format error', 0, 0)
                lcd.show()
                exit(1)
            
        elif action == 3:
            lcd.fill(0)
            lcd.text("encode",20, 52)       #set "" at (0,0)
            lcd.show()#display

            rate, audio, path = select_audio_file()

            encryption_id = generate_encryption_id()
            accelerated_audio = speed_up_audio(audio, rate, 2.0)
            encoded_audio = embed_watermark(accelerated_audio, encryption_id)

            output_name = input("請輸入加密後檔案的名稱: ")
            output_path = os.path.join(path, f"{output_name}_{encryption_id}.wav")
            wavfile.write(output_path, rate, encoded_audio)
            print(f"嵌入完成，結果已保存至: {output_path}")
            lcd.text('successfully', 5, 16)
            lcd.shoe()
           
        elif action == 4:
            lcd.fill(0)
            lcd.text("decode",20 ,52)       #set "" at (0,0)
            lcd.show()#display

            rate, audio, path = select_audio_file()
            extracted_id = extract_watermark(audio)
            psw = input("請輸入密鑰進行驗證: ")

            if psw == extracted_id:
                remove = input("是否移除水印並生成解密後音檔？(y/n): ").lower() == 'y'
                if remove:
                    output_name = input("請輸入解密後檔案的名稱: ")
                    output_path = os.path.join(path, f"{output_name}_watermark_removed.wav")
                    wavfile.write(output_path, rate, audio)
                    print(f"水印已移除，解密後的音頻已保存至: {output_path}")
                    lcd.text('successfully', 5, 16)

            else:
                lcd.text("input format error", 5, 16)
    
    except Exception as e:
        lcd.text('failed', 0, 0)
        print('程式碼錯誤：', e)
