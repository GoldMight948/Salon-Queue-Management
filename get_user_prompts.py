import json

transcript_path = r"C:\Users\AAHAN\.gemini\antigravity\brain\c4f6e75b-ac4a-4d5d-8add-6761cabe56ae\.system_generated\logs\transcript.jsonl"

user_prompts = []
try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            role = data.get('role') or data.get('author') or (data.get('message', {}).get('role'))
            # Check content
            text = ""
            if 'content' in data:
                text = data['content']
            elif 'message' in data and 'content' in data['message']:
                text = data['message']['content']
            
            # If it's a user turn
            if role == 'user' or data.get('type') == 'user':
                user_prompts.append(text)
            elif 'user_turn' in data:
                user_prompts.append(data['user_turn'])
except Exception as e:
    print("Error reading transcript:", e)

print(f"Found {len(user_prompts)} entries:")
for i, p in enumerate(user_prompts):
    print(f"--- Prompt {i+1} ---")
    print(p[:300])
