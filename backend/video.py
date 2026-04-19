import os
from moviepy import ImageClip, concatenate_videoclips, VideoFileClip, AudioFileClip

def make_video():
    img_folder = "assets/images"
    out_folder = "assets/output"
    os.makedirs(out_folder, exist_ok=True)

    if not os.path.exists(img_folder):
        return "no_images"

    files = sorted(os.listdir(img_folder))
    clips = []

    for f in files:
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(img_folder, f)
            clip = ImageClip(path).with_duration(3)
            clips.append(clip)

    if len(clips) == 0:
        return "no_images"

    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(os.path.join(out_folder, "video.mp4"), fps=24)
    video.close()
    return "ok"


def merge_audio():
    video_path = "assets/output/video.mp4"
    audio_path = "assets/audio/voice.mp3"

    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        return "missing_files"

    vid = VideoFileClip(video_path)
    aud = AudioFileClip(audio_path)

    # If audio is longer than video, loop the video to match audio duration
    if aud.duration > vid.duration:
        loops = int(aud.duration / vid.duration) + 1
        vid = concatenate_videoclips([vid] * loops).subclipped(0, aud.duration)

    # Trim audio to video length to keep them in sync
    aud = aud.subclipped(0, vid.duration)

    final = vid.with_audio(aud)
    final.write_videofile("assets/output/final.mp4", fps=24)
    final.close()
    vid.close()
    aud.close()
    return "ok"
