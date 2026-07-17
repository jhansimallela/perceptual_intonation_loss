import streamlit as st,pandas as pd,os
from datetime import datetime
os.makedirs('responses',exist_ok=True)
st.set_page_config(page_title='Pilot')
if 'started' not in st.session_state:
 st.title('Pilot');pid=st.text_input('Participant ID');cons=st.checkbox('I agree'); 
 if st.button('Start'):
  st.session_state.started=True;st.session_state.pid=pid;st.session_state.i=0;st.session_state.df=pd.read_csv('trials.csv');st.rerun()
 st.stop()
df=st.session_state.df;i=st.session_state.i
if i>=len(df): st.success('Done');st.stop()
r=df.iloc[i]
st.progress((i+1)/len(df));st.write(f'Trial {i+1}/{len(df)}')
st.write('Original');st.audio(os.path.join('original',r.filename))
st.write('Generated');st.audio(os.path.join('generated',r.filename))
st.info(r.transcript)
ans=None
if r.question=='word': ans=st.radio('Which word?',str(r.words).split('|')+['No noticeable difference'])
elif r.question=='severity': ans=st.radio('Severity',[1,2,3,4,5],horizontal=True)
else: ans=st.radio('Similarity',[1,2,3,4,5],horizontal=True)
if st.button('Submit'):
 out=os.path.join('responses',st.session_state.pid+'_responses.csv')
 row=pd.DataFrame([{'participant':st.session_state.pid,'trial':r.trial,'filename':r.filename,'question':r.question,'response':ans,'timestamp':datetime.now()}])
 row.to_csv(out,mode='a',header=not os.path.exists(out),index=False)
 st.session_state.i+=1;st.rerun()
