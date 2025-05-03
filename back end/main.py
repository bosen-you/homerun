from utils import *
from scheduler import start_background_scheduler
from fastapi import Request, FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from scipy.io import wavfile
import io
import os
import requests

app = FastAPI()  
UPLOAD_DIR = 'static' 
os.makedirs(UPLOAD_DIR, exist_ok=True)

template = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    start_background_scheduler() 

@app.get('/')
async def root(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_background_scheduler)
    return template.TemplateResponse('index.html', {"request": request})

@app.post('/transform')
async def transform_audio(file: UploadFile = File(...), kind: str = Form(...), extra: str = Form(...)):
    try: 
        print(extra)
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)  
        if kind == 'waveform':
            png_photo, bmp_photo = plot_waveform(rate, audio, ('waveform' if not extra else extra))
            return JSONResponse(content={"status": "successfully", "photo": png_photo, "bmp_photo": bmp_photo})
        else:
            png_photo, bmp_photo = plot_frequency_spectrum(rate, audio, ("frequency_spectrum" if not extra else extra))
            return JSONResponse(content={"status": "successfully", "photo": png_photo, "bmp_photo": bmp_photo})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "falied", "message": f"{e}"})
     
@app.post('/compare')
async def compare_audio(file1: UploadFile = File(...), file2: UploadFile = File(...), kind: str = Form(...), extra: str = Form(...)):
    print(1)
    try: 
        binary_data1, binary_data2 = await file1.read(), await file2.read() 
        wav_io1, wav_io2 = io.BytesIO(binary_data1), io.BytesIO(binary_data2)

        rate1, audio1= wavfile.read(wav_io1) 
        rate2, audio2= wavfile.read(wav_io2)

        if kind == 'data':
            l = ['0% ~ 0%\n危險程度：Risk-free', '20% ~ 40%\n危險程度：Secure', '40% ~ 60%\n危險程度：Moderate', '60% ~ 80%\n危險程度：Dangerous', '80% ~ 100%\n危險程度：Hazardous']
            rate_check = [[0, 20], [21, 40], [41, 60], [61, 80], [81, 100]]
            another, final = compare_two_audio(wav_io1, wav_io2)
            
            for i in range(5):
                if rate_check[i][1] >= float(final) >= rate_check[i][0]:
                    print(f'{another}\n總平均{l[i]}')
                    return JSONResponse(content={"status": "successfully", "result": f'{another}\n總平均：{l[i]}'})
        elif kind == 'waveform':
            png_photo, bmp_photo = plot_waveform_compare(audio1, rate1, audio2, rate2, ('waveform' if not extra else extra))
            return JSONResponse(content={"status": "successfully", "photo": png_photo, "bmp_photo": bmp_photo})
 
        elif kind == 'spectrogram':
            png_photo, bmp_photo = plot_spectrogram_compare(audio1, rate1, audio2, rate2, ('frequency' if not extra else extra))
            return JSONResponse(content={"status": "successfully", "photo": png_photo, "bmp_photo": bmp_photo})
        
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

encryption_id = ''
@app.post('/encode')
async def encode_audio(file: UploadFile = File(...)):
    global encryption_id
    try:
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)
        encryption_id = generate_encryption_id()
        accelerated_audio = speed_up_audio(audio, 2.0)
        return JSONResponse(content={"status": "successfully", "photo": save_audio(accelerated_audio, rate//2+1), "key": encryption_id})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

@app.post('/decode')
async def decode_audio(file: UploadFile = File(...), psw: str = Form(...)):
    global encryption_id
    try: 
        binary_data = await file.read() 
        wav_io = io.BytesIO(binary_data)

        rate, audio = wavfile.read(wav_io)
        #extracted_id = extract_watermark(audio)

        print(encryption_id)
        if psw == encryption_id:
            audio = remove_watermark(audio)
            return JSONResponse(content={"status": "successfully", "photo": save_audio(audio, rate//2+1)})
        else:
             return JSONResponse(content={"status": "failed", "message": 'input format error'})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "failed", "message": f'{e}'})

@app.post('/data')
async def send_data(url: str = Form(...), data: str = Form(...), percent: str = Form(...)):
    print(1)
    esp_url = 'http://172.25.26.193:80/bmp'
    payload = {
        'url': url,
        'result': data,       # 注意：ESP32 side 可能用 'data' 或 'result'
        'per': percent        # 注意：ESP32 side 可能用 'percent' 或 'per'
    }
    response = requests.post(esp_url, data=payload)
    print(response.text())

