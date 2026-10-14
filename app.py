import os
import re
import glob
import random
import subprocess
import gradio as gr

def generate_mindbender_video(topic_choice):
    for f in ["voice.mp3", "bgm.wav", "subs.ass", "MindBender_US_Viral.mp4"]:
        if os.path.exists(f): os.remove(f)

    topics = {
        "3 Dark Psychology Tricks Used By Billionaires": "Billionaires do not use luck to control markets. They use dark psychology. First, the scarcity illusion. By making products artificially limited, your brain panics and buys instantly. Second, anchored pricing. The first high price you see makes the next expensive item feel like a massive discount. And third, manufactured urgency. When a timer ticks down, your logical brain shuts down, and impulse takes over. Mastering these three shifts your entire perspective. Subscribe to MindBender for more psychological secrets.",
        "Why Casinos Are Designed To Trap Your Mind": "Have you ever wondered why casinos have zero clocks and zero windows? It is not an accident; it is absolute psychological warfare. Casinos trap your mind by locking you in a timeless loop where day and night do not exist. The carpets have chaotic patterns to keep your eyes focused upward, and the slot machines use near-miss psychology to trigger a dopamine spike, making you feel like a winner right before you lose everything. Your brain is being hacked every single second. Hit subscribe to uncover more hidden truths with MindBender.",
        "How McDonald's Tricks Your Brain Into Spending More": "McDonalds spent millions engineering a multi-billion dollar mind trap. Notice how their signs are always bright red and yellow? These exact colors trigger hunger and impulsive behavior in the human subconscious. Furthermore, the warm smell of fried oil is pumped directly into the dining area from their vents to activate your salivary glands even when you are full. And when the cashier asks, 'Would you like to make that large?', it is a textbook choice architecture trap. You just got manipulated. Stay sharp, and subscribe to MindBender."
    }

    script_text = topics.get(topic_choice, topics["3 Dark Psychology Tricks Used By Billionaires"])

    # 1. Generate Voice
    subprocess.run([
        "edge-tts", "--voice", "en-US-AndrewMultilingualNeural",
        "--rate=+5%", "--pitch=-1Hz", "--text", script_text,
        "--write-media", "voice.mp3", "--write-subtitles", "subs.vtt"
    ])

    try:
        vo_dur = float(subprocess.check_output(
            "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 voice.mp3",
            shell=True
        ).decode('utf-8').strip())
    except Exception:
        vo_dur = 25.0

    # 2. Render Video with Background & Text
    output_file = "MindBender_US_Viral.mp4"
    render_cmd = f'ffmpeg -y -f lavfi -i "testsrc2=size=1080x1920:rate=30" -i voice.mp3 -filter_complex "[0:v]eq=contrast=1.3:brightness=-0.7,boxblur=15:5,drawtext=text=\'{topic_choice}\':fontcolor=white:fontsize=65:x=(w-text_w)/2:y=(h-text_h)/2:enable=\'between(t,0,{vo_dur})\'[v];[1:a]volume=2.0[a]" -map "[v]" -map "[a]" -t {vo_dur} -c:v libx264 -crf 20 -pix_fmt yuv420p -preset superfast -c:a aac -b:a 128k "{output_file}"'
    subprocess.run(render_cmd, shell=True)

    for f in ["voice.mp3", "subs.vtt"]:
        if os.path.exists(f): os.remove(f)

    return output_file

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 MindBender AI - US High-CPM Video Engine (Render)")
    gr.Markdown("Select a topic and generate your professional US English short instantly!")
    
    topic_input = gr.Dropdown(
        choices=[
            "3 Dark Psychology Tricks Used By Billionaires",
            "Why Casinos Are Designed To Trap Your Mind",
            "How McDonald's Tricks Your Brain Into Spending More"
        ],
        label="Select Viral Topic",
        value="3 Dark Psychology Tricks Used By Billionaires"
    )
    
    generate_btn = gr.Button("🚀 Generate Viral Short", variant="primary")
    video_output = gr.Video(label="Generated Masterpiece")
    
    generate_btn.click(fn=generate_mindbender_video, inputs=topic_input, outputs=video_output)

demo.launch(server_name="0.0.0.0", server_port=7860)
