import subprocess

def analyze_k8s_issue(kubectl_output):
    prompt = f"""
You are a Senior Site Reliability Engineer.

Analyze the following kubectl describe pod output.

1. Identify the root cause
2. Explain the issue clearly
3. Suggest the exact fix or command change

kubectl output:
{kubectl_output}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout


with open("pod_issue.txt", "r") as file:
    pod_output = file.read()

analysis = analyze_k8s_issue(pod_output)

print("\n====== AI Kubernetes Incident Analysis ======\n")
print(analysis)
