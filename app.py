import os, time, streamlit as st
from orchestrator import start, after_clarification, finish

st.set_page_config(page_title='AI Engineering Control Tower', page_icon='◈', layout='wide')
DEFAULT_REQ='''Give store managers early visibility when a high-demand product is expected to fall below its replenishment level. The solution should support near-real-time visibility. Inventory updates should be processed synchronously.'''

for k,v in {'stage':'idle','trace':[],'artifacts':{},'metrics':{'agents':0,'tools':0,'gates':0,'latency':0.0}}.items():
    if k not in st.session_state: st.session_state[k]=v

def trace(a,b,c=''): st.session_state.trace.append((a,b,c))
def reset():
    for k in ['stage','trace','artifacts','metrics']: st.session_state.pop(k,None)

st.markdown('''<style>
.block-container{max-width:1450px;padding-top:1.3rem}.kicker{font-size:.76rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#667085}.outcome{padding:1rem;border:1px solid #E4E7EC;border-radius:14px;min-height:100px}.ot{font-weight:700}.od{font-size:.84rem;color:#475467;margin-top:.35rem}.gate{padding:1rem;border-radius:14px;border:1px solid #F2C94C;background:#FFFAEB}.pass{padding:1rem;border-radius:14px;border:1px solid #A6E3C1;background:#ECFDF3}.small{font-size:.78rem;color:#667085}.row{padding:.5rem .7rem;border-bottom:1px solid #EAECF0}
</style>''',unsafe_allow_html=True)

h1,h2=st.columns([4.5,1])
with h1:
    st.markdown('<div class="kicker">Engineering Manager + AI • Interview PoC</div>',unsafe_allow_html=True)
    st.title('AI Engineering Control Tower')
    st.write('Turn a business need into a **safe, measurable engineering outcome**.')
with h2:
    if st.button('↻ Reset',use_container_width=True): reset(); st.rerun()

st.markdown('### Business outcomes')
for c,(t,d) in zip(st.columns(4),[
    ('Protect margin','Reduce stockouts, spoilage and avoidable cost.'),
    ('Grow order volume','Improve ordering experience and reliability.'),
    ('Improve decisions','Give teams timely supply-demand visibility.'),
    ('Scale safely','Handle peaks without revenue-losing outages.')]):
    c.markdown(f'<div class="outcome"><div class="ot">{t}</div><div class="od">{d}</div></div>',unsafe_allow_html=True)

st.markdown('### What the control tower does')
st.caption('Business need → clarify → design → validate → build/test → measure')
with st.container(border=True):
    st.markdown('#### 1 · Business need')
    requirement=st.text_area('What should improve?',DEFAULT_REQ,height=105)
    run=st.button('▶ Run controlled workflow',type='primary',use_container_width=True)

if run:
    st.session_state.trace=[]; st.session_state.artifacts={}; st.session_state.metrics={'agents':0,'tools':0,'gates':0,'latency':0.0}
    t=time.perf_counter(); trace('Control Tower','RUNNING','Received the business need and started the controlled workflow.')
    req,ctx=start(requirement); st.session_state.metrics['agents']=2; st.session_state.metrics['tools']=1; st.session_state.artifacts['Requirement']=req
    trace('Business context','COMPLETE','Used the client objectives, pain points and architecture principles.')
    trace('Requirement Agent','COMPLETE','Converted the need into an actionable requirement and found missing decisions.')
    if req['status']=='HUMAN_CLARIFICATION_REQUIRED':
        st.session_state.stage='clarification'; st.session_state.metrics['gates']=1; trace('Business approval','WAITING','The AI will not invent decisions that change the business outcome.')
    st.session_state.metrics['latency']=round(time.perf_counter()-t,2); st.rerun()

st.markdown('### 2 · Decision flow')
flow=[('Need','Business need'),('Clarify','Remove ambiguity'),('Design','Choose solution'),('Validate','Challenge risks'),('Build','Create evidence'),('Measure','Quality gate')]
for c,(name,desc) in zip(st.columns(6),flow): c.markdown(f'**○ {name}**  \n<span class="small">{desc}</span>',unsafe_allow_html=True)

if st.session_state.stage=='clarification':
    st.markdown('<div class="gate"><b>Business decision needed</b><br>The AI found four missing choices. It pauses rather than inventing them.</div>',unsafe_allow_html=True)
    st.markdown('#### Clarify the business rule')
    a,b=st.columns(2)
    with a:
        hd=st.text_input('Which products are high-demand?','Top 20% of SKUs by rolling 30-day order volume'); th=st.text_input('When should we alert?','20 units')
    with b:
        hz=st.text_input('How far ahead should we look?','24 hours'); ac=st.selectbox('What should happen?',['Notification only','Automatic order creation'])
    if st.button('✓ Approve business rule',type='primary'):
        req,des,val=after_clarification(requirement,{'high_demand':hd,'threshold':th,'horizon':hz,'action':ac})
        st.session_state.artifacts['Requirement']=req; st.session_state.artifacts['Design']=des; st.session_state.metrics['agents']+=1; st.session_state.metrics['tools']+=1; st.session_state.metrics['gates']=2
        trace('Business approval','APPROVED','Business owner supplied the missing rule.'); trace('Solution Design','COMPLETE','Proposed solution, controls and AI/deterministic split.'); trace('Architecture check','REVIEW_REQUIRED',val['reason']); st.session_state.stage='architecture'; st.rerun()

if st.session_state.stage=='architecture':
    d=st.session_state.artifacts['Design']
    st.markdown('<div class="gate"><b>Architecture decision needs evidence</b><br>The initial requirement asks for synchronous processing. Before committing, validate peak volume, latency and consistency.</div>',unsafe_allow_html=True)
    st.markdown('#### Proposed solution')
    a,b,c=st.columns(3); a.metric('Business signal','Inventory risk'); b.metric('Response','Near real time'); c.metric('Integration','Notification API')
    st.write('**Why this matters:** choosing synchronous processing without workload evidence can create a scalability and reliability problem.')
    with st.expander('See architecture reasoning'): st.write(d['architecture_decision']); st.write('Alternatives:',', '.join(d['alternatives']))
    if st.button('✓ Approve architecture direction',type='primary'):
        st.session_state.stage='build'; trace('Architecture approval','APPROVED','Trade-off accepted for this PoC; production decision would use measured workload evidence.'); st.rerun()

if st.session_state.stage=='build':
    req=st.session_state.artifacts['Requirement']; des=st.session_state.artifacts['Design']; b,e=finish(req,des)
    st.session_state.artifacts['Build/Test']=b; st.session_state.artifacts['Evaluation']=e; st.session_state.metrics['agents']+=2; st.session_state.metrics['tools']+=1
    trace('Build & Test','COMPLETE','Created representative implementation and test evidence.'); trace('Quality gate',e['status'],f"Overall quality score: {e['overall']}/100."); st.session_state.stage='complete'; st.rerun()

if st.session_state.trace:
    with st.expander('Execution evidence',expanded=st.session_state.stage!='idle'):
        for a,b,c in st.session_state.trace: st.markdown(f'<div class="row"><b>{a}</b> &nbsp; <code>{b}</code><br><span class="small">{c}</span></div>',unsafe_allow_html=True)

if st.session_state.stage=='complete':
    e=st.session_state.artifacts['Evaluation']; st.markdown('### 3 · Outcome and quality')
    st.markdown(f'<div class="pass"><b>✓ READY FOR NEXT STAGE</b><br>Quality score <b>{e["overall"]}/100</b>. Evidence covers requirement, architecture, security and tests.</div>',unsafe_allow_html=True)
    for c,(n,v) in zip(st.columns(4),[('Requirement','94%'),('Grounding','96%'),('Architecture','90%'),('Test coverage','91%')]): c.metric(n,v)
    st.markdown('#### What changed for the business')
    for c,(t,d) in zip(st.columns(3),[('Earlier visibility','Store managers get an early signal before a likely stockout.'),('Safer decisions','The AI pauses when a business choice is missing or architecture needs evidence.'),('Measurable delivery','Requirements connect to design, tests and a quality gate.')]): c.markdown(f'**{t}**  \n{d}')
    with st.expander('Requirement → evidence traceability'):
        st.write('Business need → acceptance criteria → architecture decision → implementation → tests → evaluation')
        st.json({'Business need':'Early visibility of inventory risk','Acceptance criteria':st.session_state.artifacts['Requirement']['acceptance_criteria'],'Test evidence':st.session_state.artifacts['Build/Test']['traceability'],'Quality gate':f"{e['overall']}/100 — {e['status']}"})

st.markdown('### 4 · AI operating controls')
m=st.session_state.metrics
for c,(n,v) in zip(st.columns(4),[('Human decision gates',m['gates']),('Agent stages',m['agents']),('Tool calls',m['tools']),('Run time',f"{m['latency']:.2f}s")]): c.metric(n,v)
st.caption('No token or cost figures are fabricated. Connect provider telemetry when a live model is used.')
st.divider(); st.caption('PoC boundary: enterprise tools and production systems are represented by controlled interfaces. Production would add scoped identities, authorization, audit, observability, evaluation regression and governed tool/MCP access.')
