import os
from tkinter import Tk, filedialog, Label, StringVar
from tkinter import ttk
from moviepy import VideoFileClip

VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpeg', '.mpg')

def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error in {file_path}: {e}")
        return 0

def get_total_duration_and_info(folder):
    total_duration = 0
    total_size = 0
    video_count = 0

    video_files = []

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(VIDEO_EXTENSIONS):
                full_path = os.path.join(root, file)
                video_files.append(full_path)

    total_videos = len(video_files)
    progress_bar["maximum"] = total_videos

    for i, path in enumerate(video_files, 1):
        total_duration += get_video_duration(path)
        total_size += os.path.getsize(path)
        video_count += 1
        progress_var.set(i)
        progress_bar.update()

    return total_duration, total_size, video_count

def seconds_to_hms(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return h, m, s

def format_size(bytes_val):
    mb = bytes_val / (1024 * 1024)
    gb = mb / 1024
    return f"{mb:.2f} MB / {gb:.2f} GB"

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        result_label.config(text="Processing...")
        size_label.config(text="")
        count_label.config(text="")
        root.update_idletasks()

        total_seconds, total_bytes, total_files = get_total_duration_and_info(folder)
        h, m, s = seconds_to_hms(total_seconds)
        size_str = format_size(total_bytes)

        result_label.config(
            text=f"Total video duration: {h}h {m}m {s}s"
        )
        size_label.config(text=f"Total size: {size_str}")
        count_label.config(text=f"Total videos: {total_files}")

# GUI setup
root = Tk()
root.title("Video Duration Calculator")
root.geometry("500x370")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

try:
    root.iconbitmap("myicon.ico")
except:
    pass

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 11),
                foreground="white",
                background="#2b2b4d",
                padding=10)
style.map("TButton",
          background=[("active", "#3e3e6c")])

style.configure("TLabel",
                font=("Segoe UI", 11),
                foreground="white",
                background="#1e1e2f",
                padding=5)

# Widgets
title_label = ttk.Label(root, text="Video Duration Calculator", style="TLabel")
title_label.pack(pady=10)

browse_button = ttk.Button(root, text="Select Folder", command=browse_folder)
browse_button.pack(pady=10)

progress_var = StringVar()
progress_bar = ttk.Progressbar(root, length=350, variable=progress_var)
progress_bar.pack(pady=10)

result_label = ttk.Label(root, text="Choose a folder to begin", style="TLabel", justify="center")
result_label.pack(pady=10)

size_label = ttk.Label(root, text="", style="TLabel", justify="center")
size_label.pack(pady=5)

count_label = ttk.Label(root, text="", style="TLabel", justify="center")
count_label.pack(pady=5)

author_label = ttk.Label(root, text="Developed by Sina HPK", style="TLabel")
author_label.pack(side="bottom", pady=10)

root.mainloop()
