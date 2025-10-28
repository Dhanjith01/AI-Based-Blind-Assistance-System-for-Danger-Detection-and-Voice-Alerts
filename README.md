# 🦾 AI Assistant for the Blind

An **AI-powered assistive system** that helps visually impaired users by detecting objects and motion in real-time, understanding environmental danger levels, and providing **adaptive voice feedback** using expressive Text-to-Speech (TTS).

---

## 🚀 Features

- **Real-Time Object & Motion Detection** – Detects objects, people, and movement using **YOLOv8**.  
- **Context Understanding** – Uses **Groq’s GPT-OSS-20B LLM** to analyze scenes and generate responses according to detected danger levels.  
- **Adaptive Voice Feedback** – Integrates **Murf AI** for expressive voice output that changes tone:
  - 🟢 Calm when safe  
  - 🔴 Stern when danger is detected  
- **Multimodal Integration** – Combines **computer vision**, **natural language generation**, and **speech synthesis** in one system.  
- **Accessibility-Focused Design** – Aims to enhance situational awareness and safety for visually impaired users.

---

## 🧠 Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Object Detection | [YOLOv8](https://github.com/ultralytics/ultralytics) |
| Language Generation | [Groq API (GPT-OSS-20B)](https://groq.com/) |
| Text-to-Speech | [Murf AI](https://murf.ai/) |
| Programming Language | Python |
| Libraries | OpenCV, ultralytics, Groq, Murf, time, threading|

---

## ⚙️ System Architecture
1. **YOLOv8** detects objects and motion in real-time.  
2. The detected objects and movement data are sent to **Groq LLM**, which generates a short textual description based on danger level.  
3. The text is passed to **Murf AI**, which produces voice output — calm or stern depending on context.  
4. The user hears adaptive voice feedback through speakers or headphones.
