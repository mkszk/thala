
import csv
import re
import os
import hashlib
from moviepy.editor import *

from .voice_file import create_voice_file


RE_RUBY = re.compile(r"｜([^《]*)《([^》]*)》")


DEFAULT_PARAMS = {
    "OUTPUT_SIZE": (1280,720),
    "MOVIE_CROP": (0,80,720,1520),
    "MOVIE_RESIZE": (360,720),
    "MOVIE_VOLUME": 0.1,
    "IMAGE_RESIZE": (920,720),
    "FONT_NAME": "Yu-Mincho",
    "FONT_COLOR": "black",
    "FONT_SIZE": 54,
    "TEXT_OFFSET": (360+20,130),
    "TEXT_RESIZE": (920-20*2,720-130*2),
    "TEMP_DIR": "temp",
}


def create_voice_clip(text, duration_seconds, params={}):
    """
    良い感じの音声クリップを作る
    """
    # デフォルトパラメータを採用
    for (k,v) in DEFAULT_PARAMS.items():
        if k not in params:
            params[k] = v
    # 音声クリップを作る
    if not os.path.exists(params["TEMP_DIR"]):
        os.makedirs(params["TEMP_DIR"])
    if os.path.isdir(params["TEMP_DIR"]):
        hashed = hashlib.sha1(text.encode()).hexdigest()
        temp_wav = os.path.join(params["TEMP_DIR"], f"{hashed}.wav")
    create_voice_file(RE_RUBY.sub(r"\2", text).replace("\n",""),
        duration_seconds, temp_wav)
    return AudioFileClip(temp_wav)
    


def create_subtitle_clip(text, duration_seconds, params={}):
    """
    良い感じの字幕クリップを作る
    """
    # デフォルトパラメータを採用
    for (k,v) in DEFAULT_PARAMS.items():
        if k not in params:
            params[k] = v
    # 字幕
    video2 = (TextClip(RE_RUBY.sub(r"\1", text),
                       font=params["FONT_NAME"],
                       color=params["FONT_COLOR"],
                       font_size=params["FONT_SIZE"],
                       align="West"))
    scale = 1.0
    for (siz,lim) in zip(video2.size,params["TEXT_RESIZE"]):
        if lim <= siz*scale:
            scale = lim/siz
    video2 = (video2.resize(scale)
                .with_position(params["TEXT_OFFSET"]))
    return video2


def create_sequence(video_file, csv_file, image_file, params={}):
    """
    良い感じのシーケンスを作る
    """
    # デフォルトパラメータを採用
    for (k,v) in DEFAULT_PARAMS.items():
        if k not in params:
            params[k] = v
    # ベース動画を作る
    game = (VideoFileClip(video_file, audio=True)
                .crop(*params["MOVIE_CROP"])
                .resize(params["MOVIE_RESIZE"]))
    back = (ImageClip(image_file)
                .resize(params["IMAGE_RESIZE"]))
    base = clips_array([[game, back]])
    with open(csv_file, encoding="utf-8") as f:
        data = [(float(tim),float(spd),txt) for (tim,spd,txt) in csv.reader(f)]
        data.append([game.end, 1.0, ""])
        video1_list = []
        video2_list = []
        audio_list = []
        timsum = 0.0
        for ((tim1,spd,txt),(tim2,_,_)) in zip(data[:-1],data[1:]):
            duration_seconds = (tim2 - tim1)/spd
            # ビデオ切り取り
            video1 = (base
                        .subclip(tim1, tim2)
                        .multiply_speed(spd)
                        .multiply_volume(params["MOVIE_VOLUME"]))
            video1_list.append(video1)
            # 字幕生成
            video2_list.append(create_subtitle_clip(txt, duration_seconds, params)
                        .with_start(timsum)
                        .with_duration(duration_seconds))
            # 音声生成
            audio_list.append(create_voice_clip(txt, duration_seconds, params)
                        .with_start(timsum))
            # 時刻更新
            timsum += duration_seconds
        # 連結
        final = CompositeVideoClip([concatenate_videoclips(video1_list),*video2_list])
        final.audio = CompositeAudioClip([final.audio, *audio_list])
        return final

