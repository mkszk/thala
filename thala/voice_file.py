
from pydub import AudioSegment


def create_voice_file(text, duration_seconds, temp_wav):
    """
    良い感じの音声ファイルを作る
    """
    # 速度調整
    speed = 1.0
    while True:
        try:
            # pyopenjtalkを使えるなら実行
            import pyopenjtalk
            from scipy.io import wavfile
            x, sr = pyopenjtalk.tts(text, speed=speed)
            # TODO:ファイル経由を止める
            wavfile.write(temp_wav, sr, x.astype(np.int16))
        except:
            # VOICEVOXを使えるなら実行
            import requests
            import urllib.parse
            import json
            quoted = urllib.parse.quote(text)
            headers = {
                "accept": "audio/wav",
                "Content-Type": "application/json",
            }
            audio_query = requests.post("http://localhost:50021/"+
                f"audio_query?speaker=0&text={quoted}")
            audio_json = json.loads(audio_query.content)
            audio_json["speedScale"] = speed
            audio_data = requests.post("http://localhost:50021/"+
                "synthesis?speaker=0",
                data=json.dumps(audio_json),
                headers=headers)
            with open(temp_wav, "wb") as f:
                # TODO:ファイル経由を止める
                f.write(audio_data.content)
        # TODO:ファイル経由を止める
        voice = AudioSegment.from_wav(temp_wav)
        # 時間枠に収まっているなら終了
        if voice.duration_seconds < duration_seconds:
            return True
        else:
            # 時間枠に収まらないなら速度調整を少し上げる
            speed_new = voice.duration_seconds / duration_seconds
            if speed + 0.1 < speed_new:
                speed = speed_new
            else:
                speed += speed + 0.1


if __name__ == "__main__":
    create_voice_file("これはテスト音声です。分量が長くても時間範囲に収めます。", 3, "test.wav")

