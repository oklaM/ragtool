import os, httpx
API_URL = os.getenv('MCP_URL','http://localhost:8000/mcp/search')
API_KEY = os.getenv('MCP_API_KEY','change_me_secure')

def query(q, top_k=5):
    headers={'x-api-key':API_KEY}
    resp = httpx.post(API_URL, json={'query':q, 'top_k':top_k}, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

if __name__=='__main__':
    import sys
    q=' '.join(sys.argv[1:]) or 'What is backtrader?'
    print(query(q))
