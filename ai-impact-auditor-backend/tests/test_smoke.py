from app.analysis import analyze
class X: pass
def test_analysis():
 e=X(); e.ai_signal=.8; e.evidence_strength=.9; e.issue_key='A'; e.text='AI-assisted'
 t=X(); t.issue_key='A'; t.hours=2; t.hourly_cost=50
 r=analyze([e],[t]); assert 'ai_score' in r and r['estimated_hours_saved']>=0
