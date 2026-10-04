from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
def make_pdf(name,r):
 b=BytesIO(); d=SimpleDocTemplate(b,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42); s=getSampleStyleSheet(); story=[Paragraph('AI Impact Audit Report',s['Title']),Paragraph(name,s['Heading2']),Spacer(1,12),Paragraph('Executive summary',s['Heading2']),Paragraph(f"AI score: {r['ai_score']}/100. Safety: {r['safety_score']}%. Estimated time saved: {r['estimated_hours_saved']:.2f} hours (range {r['estimated_hours_saved_low']:.2f}–{r['estimated_hours_saved_high']:.2f}). Estimated savings: €{r['estimated_savings']:.2f}. AI cost: €{r['ai_cost']:.2f}. Net benefit: €{r['net_benefit']:.2f}.",s['BodyText']),Spacer(1,12),Paragraph('Confidence',s['Heading2']),Table([['Measure','Value'],['Attribution',f"{r['attribution_confidence']}%"],['Impact',f"{r['impact_confidence']}%"],['Low-value cases',str(r['low_value_cases'])]],colWidths=[260,160],style=TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#172033')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.5,colors.grey),('PADDING',(0,0),(-1,-1),7)])),Spacer(1,12),Paragraph('Calculation method',s['Heading2']),Paragraph('Time saved = modeled baseline time − observed AI-assisted time − review/rework penalty. Financial savings = estimated hours saved × loaded hourly cost. The MVP uses explicit assumptions and uncertainty ranges.',s['BodyText']),Spacer(1,10),Paragraph('Assumptions and limitations',s['Heading2'])]
 for x in r['assumptions']: story.append(Paragraph('• '+x,s['BodyText']))
 story += [Spacer(1,10),Paragraph('Recommendations',s['Heading2'])]
 for x in r['recommendations']: story.append(Paragraph('• '+x,s['BodyText']))
 d.build(story); return b.getvalue()
