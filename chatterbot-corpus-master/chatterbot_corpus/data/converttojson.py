import os
import yaml, json
from collections import defaultdict
for f in os.walk("./chatterbot-corpus-master\\chatterbot_corpus\\data\\arabic"):
    f=f[2]
print(f)
parsed_yaml=[]
#with open("./chatterbot-corpus-master\\chatterbot_corpus\\data\\english\\ai.yml", 'r') as file:
#    data = yaml.safe_load(file)["conversations"]
for file in list(f):
    with open(f"./chatterbot-corpus-master\\chatterbot_corpus\\data\\arabic\\{file}", 'r', encoding="utf8") as file:
        data = yaml.safe_load(file)["conversations"]
        parsed_yaml.extend(data)
print(parsed_yaml)
#print(data)
# Group responses by tag
grouped_responses = defaultdict(list)
for item in parsed_yaml:
    tag = item[0]
    response = item[1]
    grouped_responses[tag].append(response)

# Create JSON structure with grouped responses
json_data = json.dumps(
    {"intents": [{"tag":tag.replace(" ","_"),"patterns": [tag], "responses": responses} for tag, responses in grouped_responses.items()]}, 
    indent=2, 
    ensure_ascii=False).encode('utf-8')

print(json_data)
with open('intents.Corpus.ar.json', 'wb') as output_file:
    output_file.write(json_data)