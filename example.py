#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thala.voice_clip import create_sequence


(create_sequence("example.mp4", "example.csv", 
                 "60d19a15f1ac2ed842000000.png")
    .write_videofile("example.output.mp4",fps=24,codec='libx264'))


