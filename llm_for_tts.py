from groq import Groq
from dotenv import load_dotenv
from tts_output import stream_text_to_speech_calm,stream_text_to_speech_stern 
load_dotenv()

client = Groq()

threat_levels = {
    'car': 10,
    'person': 10,
    'bike': 5,
    'motorbike': 6,
    'truck': 9,
    'bus': 8,
    'tree': 0,
    'glasses': 0,
    'dog': 2,
    'cat': 1,
    'fire': 10,
    'sign': 1,
    'bicycle': 5,
    'scooter': 4,
    'ball': 2,
    'obstacle': 7,
    'person_with_helmet': 3,
    'traffic_light': 1,
}

def print_message(message_list):
    str1_calm=''
    str1_stern=''
    for i in message_list:
        if i[0].lower() in threat_levels:
            if i[1]>1:
                movement=f' moving, threat level: {threat_levels[i[0].lower()]}.\n'
                if threat_levels[i[0].lower()]>4:
                    str1_stern=i[0]+movement+str1_stern
                else:
                    str1_calm=i[0]+movement+str1_calm
            elif i[1]<-1:
                movement=f' moving, threat level: {threat_levels[i[0].lower()]-5 if threat_levels[i[0].lower()]>5 else 0}.\n'
                if threat_levels[i[0].lower()]>4:
                    str1_stern=i[0]+movement+str1_stern
                else:
                    str1_calm=i[0]+movement+str1_calm
            else:
                movement=f' not moving, threat level: 0\n'
                str1_calm=i[0]+movement+str1_calm

    if(str1_stern!=''):
    
        reply_stern=llm_reply(str1_stern)
        stream_text_to_speech_stern(reply_stern,"output_stern.mp3")
    
    if(str1_calm!=''):
        reply_calm=llm_reply(str1_calm)
        stream_text_to_speech_calm(reply_calm,"output_calm.mp3")
    
    
    
def llm_reply(str1):
    prompt = f''' Create a short spoken alert for a blind user.
    Combine repeated or similar detections
    Use calm tone for low threat, cautious for medium, and urgent/commanding for high.
    Keep it under 2 sentences and easy to understand. Threat level signifies a level of danger, it should only change tone of sentence.
    No preamble. Only return a third person sentence describing surrounding to person. No object is owned by person. Dont tell action to take.
    If nothing moving, mention what objects are present. Strictly refer to only classes in input string. Dont consider direction of movement.
    Dont mention words such as alert of high alert. Humanise the sentence.
    Input: "{str1}"'''
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
          {
            "role": "user",
            "content": prompt
          }
        ],
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
        stop=None
    )

    return (completion.choices[0].message.content)
    
