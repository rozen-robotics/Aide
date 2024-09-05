import io
import numpy as np
import torch
from pydub import AudioSegment
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Инициализация модели и процессора
processor = Wav2Vec2Processor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-russian")
model = Wav2Vec2ForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-russian")

def recognize_speech_from_audio(audio_bytes):
    # Преобразование байтов в аудио данные
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")

    # Преобразование частоты дискретизации аудио данных в 16000 Гц
    audio = audio.set_frame_rate(16000)

    # Преобразование аудио данных в тензор
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    input_values = processor(audio_data, sampling_rate=16000, return_tensors="pt").input_values

    # Получение логитов из модели
    with torch.no_grad():
        logits = model(input_values).logits

    # Получение предсказаний
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    print(transcription)
    return transcription