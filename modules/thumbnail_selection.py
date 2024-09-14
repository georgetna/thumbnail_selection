# modules/thumbnail_selection.py

import os
from PIL import Image


def load_thumbnails_local(video_id):
    thumbnail_dir = os.path.join("thumbnails", str(video_id))
    thumbnails = []
    if os.path.exists(thumbnail_dir):
        for filename in os.listdir(thumbnail_dir):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                thumbnails.append(os.path.join(thumbnail_dir, filename))
    return thumbnails
