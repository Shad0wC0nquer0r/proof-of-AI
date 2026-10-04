from pathlib import Path
import csv,io,json,os
from fastapi import FastAPI,Depends,HTTPException,UploadFile,File
from fastapi.responses import Response, HTMLResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .db import SessionLocal,init_db
from .models import Project,Evidence,TimeEntry
from .connectors import github_events,jira_issues
from .analysis import signal,analyze
from .report import make_pdf
load_dotenv(); init_db(); app=FastAPI(title='AI Impact Auditor API',version='0.1.0')
def db():
 s=SessionLocal()
 try: yield s
 finally: s.close()
@app.get('/health')
def health(): return {'ok':True}
@app.post('/projects')
def create_project(name:str,session:Session=Depends(db)):
 p=Project(name=name); session.add(p); session.commit(); session.refresh(p); return {'id':p.id,'name':p.name}
@app.post('/projects/{pid}/demo')
def demo(pid:int,session:Session=Depends(db)):
 if not session.get(Project,pid): raise HTTPException(404,'Project not found')
 rows=[('GH-101','PROJ-101','alice','AI-assisted implementation using Copilot; tests added.',.8,.9),('GH-102','PROJ-102','bob','Refactored manually after AI-generated first draft; rework required.',.7,.8),('J-101','PROJ-101','alice','Implement API endpoint and document with AI assistance.',.5,.6)]
 for eid,issue,actor,text,sig,strength in rows: session.add(Evidence(project_id=pid,source='demo',external_id=eid,issue_key=issue,event_type='artifact',actor=actor,text=text,ai_signal=sig,evidence_strength=strength))
 session.add_all([TimeEntry(project_id=pid,date='2026-09-29',user='alice',issue_key='PROJ-101',hours=2.5,hourly_cost=65),TimeEntry(project_id=pid,date='2026-09-30',user='bob',issue_key='PROJ-102',hours=3,hourly_cost=65)]); session.commit(); return {'loaded':3}
@app.post('/projects/{pid}/github/ingest')
def github(pid:int,repo:str,session:Session=Depends(db)):
 if not session.get(Project,pid): raise HTTPException(404,'Project not found')
 try: events=github_events(repo)
 except Exception as e: raise HTTPException(400,str(e))
 for x in events: session.add(Evidence(project_id=pid,source='github',external_id=x['external_id'],event_type=x['event_type'],actor=x['actor'],text=x['text'],metadata_json=json.dumps(x['metadata']),ai_signal=signal(x['text']),evidence_strength=.85 if signal(x['text'])>=.5 else .45))
 session.commit(); return {'imported':len(events)}
@app.post('/projects/{pid}/jira/ingest')
def jira(pid:int,jql:str='ORDER BY updated DESC',session:Session=Depends(db)):
 if not session.get(Project,pid): raise HTTPException(404,'Project not found')
 try: events=jira_issues(jql)
 except Exception as e: raise HTTPException(400,str(e))
 for x in events: session.add(Evidence(project_id=pid,source='jira',external_id=x['external_id'],issue_key=x['issue_key'],event_type=x['event_type'],actor=x['actor'],text=x['text'],metadata_json=json.dumps(x['metadata']),ai_signal=signal(x['text']),evidence_strength=.65 if signal(x['text']) else .25))
 session.commit(); return {'imported':len(events)}
@app.post('/projects/{pid}/time-tracking/import')
async def times(pid:int,file:UploadFile=File(...),session:Session=Depends(db)):
 if not session.get(Project,pid): raise HTTPException(404,'Project not found')
 rows=list(csv.DictReader(io.StringIO((await file.read()).decode('utf-8-sig'))))
 ok=0
 for r in rows:
  try: session.add(TimeEntry(project_id=pid,date=r['date'],user=r['user'],issue_key=r['issue_key'],hours=float(r['hours']),hourly_cost=float(r.get('hourly_cost') or os.getenv('DEFAULT_HOURLY_COST','60')))); ok+=1
  except: pass
 session.commit(); return {'imported':ok,'skipped':len(rows)-ok}
def result(pid,session):
 p=session.get(Project,pid)
 if not p: raise HTTPException(404,'Project not found')
 return p,analyze(p.evidence,p.time_entries)
@app.post('/projects/{pid}/analyze')
def run(pid:int,session:Session=Depends(db)):
 p,r=result(pid,session); return {'project_id':p.id,**r}
@app.get('/projects/{pid}/report')
def report(pid:int,session:Session=Depends(db)):
 p,r=result(pid,session); return {'project':p.name,**r}
@app.get('/projects/{pid}/report.pdf')
def pdf(pid:int,session:Session=Depends(db)):
 p,r=result(pid,session); return Response(make_pdf(p.name,r),media_type='application/pdf',headers={'Content-Disposition':f'attachment; filename="ai-impact-{pid}.pdf"'})

@app.get('/')
def home():
    return HTMLResponse((Path(__file__).parent / 'index.html').read_text(encoding='utf-8'))
