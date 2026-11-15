import base64,re,os,sys
here=os.path.dirname(os.path.abspath(__file__))
t=open(os.path.join(here,'template.html')).read()
def uri(n):
    ext=n.rsplit('.',1)[1]; mime={'jpg':'image/jpeg','png':'image/png'}[ext]
    return 'data:%s;base64,%s'%(mime,base64.b64encode(open(os.path.join(here,'img',n),'rb').read()).decode())
# preview fragment (private artifact): images inlined, preview bar, forms are inert
pv=t.replace('{{EMBEDJS}}','').replace('{{CONTACTWIRE}}',"wire('contact-form','cf-status','Preview only: this form goes live when the site is published.');")
pv=pv.replace('{{PREVIEWBAR}}','<div class="pv">PRIVATE DESIGN PREVIEW. Not published. Forms and videos are placeholders.</div>')
pv=pv.replace('{{FORMMSG}}','Preview only: this form goes live when the site is published.').replace('{{LISTWIRE}}',"wire('list-form','ml-status','Preview only: the signup goes live when the site is published.');")
pv=re.sub(r'\{\{img:([^}]+)\}\}',lambda m:uri(m.group(1)),pv)
open(os.path.join(here,'preview.html'),'w').write(pv)
# full site document (relative images)
LW=r'''var lf=document.getElementById('list-form'),ls=document.getElementById('ml-status'),le=document.getElementById('ml-email');if(lf&&ls&&le){lf.addEventListener('submit',function(e){e.preventDefault();var v=le.value.trim();if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)){ls.textContent='Please enter a valid email address.';return;}ls.textContent='Sending.';var cb='mc'+Date.now(),sc=document.createElement('script'),done=false;window[cb]=function(d){done=true;sc.remove();if(d&&d.result==='success'){lf.reset();ls.textContent='Thank you. You are on the list.';}else if(d&&/already subscribed/i.test(d.msg||'')){ls.textContent='You are already on the list.';}else{ls.textContent='That did not go through. Please write to andrzej@parttimemystics.com.';}};sc.onerror=function(){if(!done)ls.textContent='That did not go through. Please write to andrzej@parttimemystics.com.';};sc.src='https://parttimemystics.us17.list-manage.com/subscribe/post-json?u=2f4a7f9a0e4ba7f455a1f1c88&id=666540b433&f_id=0092d2e3f0&EMAIL='+encodeURIComponent(v)+'&b_2f4a7f9a0e4ba7f455a1f1c88_666540b433=&c='+cb;document.body.appendChild(sc);});}'''
full=t.replace('{{CONTACTWIRE}}',"var cf=document.getElementById('contact-form'),cs=document.getElementById('cf-status');if(cf&&cs){cf.addEventListener('submit',function(e){e.preventDefault();cs.textContent='Sending.';fetch(cf.action,{method:'POST',body:new FormData(cf),headers:{'Accept':'application/json'}}).then(function(r){if(r.ok){cf.reset();cs.textContent='Thank you. We will be in touch.';}else{cs.textContent='That did not go through. Please write to booking@parttimemystics.com.';}}).catch(function(){cs.textContent='That did not go through. Please write to booking@parttimemystics.com.';});});}").replace('{{EMBEDJS}}',"(function(){var a=document.getElementById('lead-video');if(!a)return;a.addEventListener('click',function(e){e.preventDefault();var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+a.getAttribute('data-yt')+'?autoplay=1&rel=0';f.title='Outlaw, Part Time Mystics';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.style.cssText='width:100%;aspect-ratio:16/9;border:0;display:block;background:#2a1f17';a.replaceWith(f);});})();").replace('{{PREVIEWBAR}}','').replace('{{FORMMSG}}','Form not connected yet.').replace('{{LISTWIRE}}',LW)
full=re.sub(r'\{\{img:([^}]+)\}\}',lambda m:'img/'+m.group(1),full)
head,rest=full.split('<style>',1)
css,body=rest.split('</style>',1)
doc='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'+head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')+'<style>'+css+'</style>\n</head>\n<body>\n'+body+'\n</body>\n</html>\n'
open(os.path.join(here,'index.html'),'w').write(doc)
print(len(pv)//1024,'KB preview;',len(doc)//1024,'KB index')
