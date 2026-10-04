import os,requests
def github_events(repo):
 token=os.getenv('GITHUB_TOKEN')
 if not token: raise RuntimeError('GITHUB_TOKEN is not configured')
 r=requests.get(f'https://api.github.com/repos/{repo}/pulls',params={'state':'closed','per_page':100},headers={'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json'},timeout=30); r.raise_for_status(); out=[]
 for pr in r.json():
  out.append({'external_id':str(pr['id']),'event_type':'pull_request','actor':(pr.get('user') or {}).get('login'),'text':f"{pr.get('title','')}\n{pr.get('body') or ''}",'metadata':{'url':pr.get('html_url'),'merged':bool(pr.get('merged_at'))}})
 return out
def jira_issues(jql='ORDER BY updated DESC'):
 base,email,token=os.getenv('JIRA_BASE_URL'),os.getenv('JIRA_EMAIL'),os.getenv('JIRA_API_TOKEN')
 if not all([base,email,token]): raise RuntimeError('Jira credentials are not configured')
 r=requests.get(base.rstrip('/')+'/rest/api/3/search',params={'jql':jql,'maxResults':100},auth=(email,token),timeout=30); r.raise_for_status(); out=[]
 for i in r.json().get('issues',[]):
  f=i.get('fields',{}); out.append({'external_id':i['id'],'issue_key':i['key'],'event_type':'jira_issue','actor':(f.get('assignee') or {}).get('displayName'),'text':str(f.get('summary') or '')+' '+str(f.get('description') or ''),'metadata':{'status':(f.get('status') or {}).get('name')}})
 return out
