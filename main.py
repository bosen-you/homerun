from .utils import *
import os
from scipy.io import wavfile 

if __name__ == '__main__':
    try:
        action = int(input("輸入數字就好了\n1. transform\n2. compare\n3. encode\n4. decode\n"))
        if action == 1:
            rate, audio, desktop_path = select_audio_file()
            waveform_img_path = os.path.join(desktop_path, "waveform.png")
            spectrum_img_path = os.path.join(desktop_path, "spectrum.png")

            # 繪製並顯示+儲存波形圖
            plot_waveform(audio, audio, rate, "Waveform Watermark", "encode", save_path=waveform_img_path)
            print(f"波形圖已保存至: {waveform_img_path}")

            # 繪製並顯示+儲存頻譜圖
            plot_frequency_spectrum(audio, rate, "Original Audio", save_path=spectrum_img_path)
            print(f"頻譜圖已保存至: {spectrum_img_path}")
        elif action == 2:
            rate1, audio1, desktop_path = select_audio_file()
            rate2, audio2, _ = select_audio_file()

            cho = int(input('輸入數字就好了\n1. 顯示數據比較\n2. 顯示圖片比較\n'))
            if cho == 1:
                final = analyze_audio_similarity(rate1, audio1, rate2, audio2)
                l = ['0% ~ 20%\nRisk-free', '20% ~ 40%\nSecure', '40% ~ 60%\nModerate', '60% ~ 80%\nDangerous', '80% ~ 100%\nHazardous']
                rate_check = [[0, 20], [20, 40], [40, 60], [60, 80], [80, 101]]
                
                for i in range(5):
                    if rate_check[i][1] > final >= rate_check[i][0]:
                        print(l[i])
                        break
                    
            elif cho == 2:
                plot_audio_comparison(rate1, audio1, desktop_path, audio2)
            else: 
                print("輸入格式錯誤")
                exit(1)
            
        elif action == 3:
            rate, audio, desktop_path = select_audio_file()

            encryption_id = generate_encryption_id()
            accelerated_audio = speed_up_audio(audio, rate, 2.0)
            encoded_audio = embed_watermark(accelerated_audio, encryption_id)

            output_name = input("請輸入加密後檔案的名稱: ")
            output_path = os.path.join(desktop_path, f"{output_name}_{encryption_id}.wav")
            wavfile.write(output_path, rate, encoded_audio)
            print(f"嵌入完成，結果已保存至: {output_path}")
           
        elif action == 4:
            rate, audio, desktop_path = select_audio_file()
            extracted_id = extract_watermark(audio)
            psw = input("請輸入密鑰進行驗證: ")

            if psw == extracted_id:
                remove = input("是否移除水印並生成解密後音檔？(y/n): ").lower() == 'y'
                if remove:
                    output_name = input("請輸入解密後檔案的名稱: ")
                    output_path = os.path.join(desktop_path, f"{output_name}_watermark_removed.wav")
                    wavfile.write(output_path, rate, audio)
                    print(f"水印已移除，解密後的音頻已保存至: {output_path}")

            else:
                print("密鑰錯誤！操作中止。")

        else:
            print("無效選項，請重新執行程式！")
    
    except Exception as e:
        print(f"程式執行錯誤: {e}")
