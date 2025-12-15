import subprocess
import json
import re

def analyze_k8s_issue(kubectl_output):
    prompt = f"""
You are a Senior Kubernetes SRE.

Return ONLY valid JSON.
NO explanations.
NO markdown.
NO backticks.
NO extra text.

JSON schema:
{{
  "issue_type": "",
  "root_cause": "",
  "severity": "LOW | MEDIUM | HIGH",
  "recommended_fix": "",
  "confidence": 0.0
}}

kubectl output:
{kubectl_output}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")
    return match.group(0)


with open("image_pull_issue.txt", "r") as f:
    pod_output = f.read()

raw_response = analyze_k8s_issue(pod_output)

print("\n====== RAW AI RESPONSE ======\n")
print(raw_response)

print("\n====== PARSED JSON ======\n")
try:
    json_str = extract_json(raw_response)
    parsed = json.loads(json_str)
    print(json.dumps(parsed, indent=2))
except Exception as e:
    print("❌ Failed to parse JSON:", e)
