from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"knowledge"
def search_enterprise_context(query):
    q=query.lower()
    hits=[]
    for p in ROOT.glob("*.md"):
        text=p.read_text(encoding="utf-8")
        score=sum(term in text.lower() for term in q.split() if len(term)>3)
        if score: hits.append({"source":p.name,"score":score,"content":text})
    return sorted(hits,key=lambda x:x["score"],reverse=True)[:4]
