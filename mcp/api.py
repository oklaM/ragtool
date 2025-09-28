from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from mcp.rag_service import RagMCPService
import os
app = FastAPI(title='RAG MCP API')
svc = RagMCPService()
MCP_API_KEY = os.getenv('MCP_API_KEY')
def check_api_key(x_api_key: str = Header(None)):
    if MCP_API_KEY and x_api_key != MCP_API_KEY:
        raise HTTPException(status_code=401, detail='Invalid API Key')
    return True
class SearchReq(BaseModel):
    query: str
    top_k: int = 5
@app.post('/mcp/search', dependencies=[Depends(check_api_key)])
def search(req: SearchReq):
    res = svc.search(req.query, top_k=req.top_k)
    return {'results': res}
@app.get('/health')
def health():
    return {'status':'ok'}
