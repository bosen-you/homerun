// 全域變數
let audioBuffer1 = null;
let audioBuffer2 = null;

document.getElementById('processBtn').addEventListener('click', () => {
  processAudioFiles();
});

// 處理上傳的兩個音檔
async function processAudioFiles() {
  const file1 = document.getElementById('audioFile1').files[0];
  const file2 = document.getElementById('audioFile2').files[0];

  if (!file1 || !file2) {
    alert('請選擇兩個音檔！');
    return;
  }

  // 檢查檔案是否為 .wav 格式
  if (!checkFileIsWav(file1) || !checkFileIsWav(file2)) {
    alert('請上傳 .wav 格式的音檔！');
    return;
  }

  try {
    // 解碼音檔
    audioBuffer1 = await decodeFile(file1);
    audioBuffer2 = await decodeFile(file2);

    // 模擬發送到後端（使用簡單的 function 代替）
    sendToBackend({ fileName: file1.name, fileSize: file1.size });
    sendToBackend({ fileName: file2.name, fileSize: file2.size });

    // 產生波形圖
    drawWaveform(audioBuffer1, document.getElementById('waveform1'));
    drawWaveform(audioBuffer2, document.getElementById('waveform2'));

    // 比對兩個音檔的相似度
    const similarity = compareAudioBuffers(audioBuffer1, audioBuffer2);
    document.getElementById('compareResult').textContent = 
      `相似度: ${(similarity * 100).toFixed(2)}%`;
  } catch (err) {
    console.error(err);
    alert('音檔處理失敗，請確認檔案格式或瀏覽器支援度。');
  }
}

// 檢查上傳的檔案是否為 .wav 格式（不區分大小寫）
function checkFileIsWav(file) {
  return file.name.toLowerCase().endsWith('.wav');
}

// 模擬發送資料到後端的 function
function sendToBackend(payload) {
  console.log("模擬發送到後端的資料：", payload);
  // 此處可改用 fetch() 或其他方式發送到真實的 API 端點
}

// 使用 Web Audio API 解碼音檔
function decodeFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const arrayBuffer = e.target.result;
        const decodedData = await audioContext.decodeAudioData(arrayBuffer);
        resolve(decodedData);
      } catch (decodeErr) {
        reject(decodeErr);
      }
    };
    reader.onerror = (err) => reject(err);
    reader.readAsArrayBuffer(file);
  });
}

// 繪製簡單波形
function drawWaveform(audioBuffer, canvas) {
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const data = audioBuffer.getChannelData(0); // 僅取第一個聲道
  const step = Math.ceil(data.length / canvas.width);
  const amp = canvas.height / 2;

  ctx.beginPath();
  ctx.moveTo(0, amp);
  for (let i = 0; i < canvas.width; i++) {
    const sample = data[i * step];
    const y = (1 + sample) * amp;
    ctx.lineTo(i, y);
  }
  ctx.strokeStyle = '#f00';
  ctx.stroke();
}

// 簡單比較兩個 AudioBuffer 的相似度
function compareAudioBuffers(buf1, buf2) {
  const data1 = buf1.getChannelData(0);
  const data2 = buf2.getChannelData(0);

  // 使用最短長度避免長度不一致
  const length = Math.min(data1.length, data2.length);

  let sumOfSquares = 0;
  for (let i = 0; i < length; i += 1000) { // 每 1000 個點取一次樣本
    const diff = data1[i] - data2[i];
    sumOfSquares += diff * diff;
  }

  const avgError = Math.sqrt(sumOfSquares / (length / 1000));
  let similarity = 1 - avgError;
  if (similarity < 0) similarity = 0;

  return similarity;
}
