import os
from openai import OpenAI
from dotenv import load_dotenv
def configure():
  load_dotenv()


def openairun(msg):
  configure()
  api_key = os.getenv('api_key')
  client = OpenAI(api_key=api_key)
  with open('sysrole.txt', 'r') as file:
    # Read the entire content of the file
    sysrole = file.read()
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": sysrole},
      {"role": "user", "content": msg}
    ]
  )
  openairun = completion.choices[0].message.content
  print(openairun)
  return openairun
  # print(completion)
# openairun("whats is dsa")
