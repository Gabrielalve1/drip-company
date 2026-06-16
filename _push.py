import os, base64, json, urllib.request, subprocess

TOKEN = open('.env.git').read().split('=',1)[1].strip()
REPO = "Gabrielalve1/drip-company"
API = f"https://api.github.com/repos/{REPO}"

def req(method, url, data=None):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "drip-push",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(r) as resp:
        return json.load(resp)

# files tracked by git (clean list)
files = subprocess.check_output(["git","ls-files"]).decode().splitlines()
files = [f for f in files if f and not f.startswith('.env')]
print(f"{len(files)} arquivos")

# 1. create blobs
tree = []
for f in files:
    raw = open(f,'rb').read()
    b64 = base64.b64encode(raw).decode()
    blob = req("POST", f"{API}/git/blobs", {"content": b64, "encoding": "base64"})
    tree.append({"path": f, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print("blob:", f)

# 2. create tree (fresh, no base = clean repo state)
tree_obj = req("POST", f"{API}/git/trees", {"tree": tree})
print("tree:", tree_obj["sha"])

# 3. create commit (no parents = overwrite history clean)
commit = req("POST", f"{API}/git/commits", {
    "message": "Drip Company - site completo: catalogo masculino, carrinho WhatsApp, mobile polish, fotos reais",
    "tree": tree_obj["sha"],
})
print("commit:", commit["sha"])

# 4. force update main ref
try:
    req("PATCH", f"{API}/git/refs/heads/main", {"sha": commit["sha"], "force": True})
    print("ref main atualizada (force)")
except Exception as e:
    req("POST", f"{API}/git/refs", {"ref": "refs/heads/main", "sha": commit["sha"]})
    print("ref main criada")

print("OK PUSH COMPLETO")
