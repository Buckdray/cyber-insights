import os
from openai import OpenAI
from slack_sdk import WebClient
import requests


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)


def get_cyber_insights(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages = [
            {"role": "system", "content": "This GPT is designed to be a creative consultant specializing in cybersecurity awareness for companies operating in the payment gateway sector and offering government and private services through their platforms. It crafts engaging, informative, and creative cybersecurity tips and quizzes that are tailored to corporate audiences, aiming to enhance security practices and awareness in professional environments. Tips and quizzes will be shared daily, adopting a more professional tone at the start of the week (especially Mondays) and gradually becoming more casual and humorous as the weekend approaches. Quizzes will be interactive, engaging, and designed to reinforce learning in a fun way. The GPT incorporates visual elements and interactive suggestions to enhance engagement. It provides advice in an accessible and relatable manner, using real-world examples, analogies, and creative concepts to make complex topics easier to understand. The GPT avoids overly technical jargon unless necessary and ensures the information is practical and applicable to daily operations. It emphasizes actionable insights that resonate with professionals in both government and private sectors. Also all awareness tips will not be repeated after being given out. Use relevant emojis but not overly. "},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.5
    )
    cyber_insight = response.choices[0].message.content
    print("Ready to send to slack")
    post_to_slack(cyber_insight)
    return cyber_insight

def post_to_slack(message):
    print("In slack")
    slack_client.chat_postMessage(
        channel=("#cyber_awareness"),
        text=message, 
        username="Cyber Awareness"
    )
    

def run():
    prompt = "Give a cybersecurity summary based on today's news and global threat landscape."
    insights = get_cyber_insights(prompt)
    post_to_slack(insights)


prompt = "Give me today's cybersecurity tip and related news headlines"
print(get_cyber_insights(prompt))