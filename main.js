(function(){
var L='bn';try{L=localStorage.getItem('lang')==='en'?'en':'bn'}catch(e){}
var root=document.documentElement,bnTitle=document.title,bnDesc=(document.querySelector('meta[name=description]')||{}).content;
function apply(l){
 L=l;root.lang=l;
 document.querySelectorAll('[data-en]').forEach(function(e){if(e.dataset.bn===undefined)e.dataset.bn=e.innerHTML;e.innerHTML=l==='en'?e.dataset.en:e.dataset.bn});
 document.querySelectorAll('img[data-alt-en]').forEach(function(i){if(!i.dataset.altBn)i.dataset.altBn=i.alt;i.alt=l==='en'?i.dataset.altEn:i.dataset.altBn});
 document.title=l==='en'?root.dataset.titleEn:bnTitle;
 var m=document.querySelector('meta[name=description]');if(m)m.content=l==='en'?root.dataset.descEn:bnDesc;
 document.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l)});
 try{localStorage.setItem('lang',l)}catch(e){}
}
document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.l)})});
if(L==='en')apply('en');
var nav=document.getElementById('nav'),bt=document.getElementById('burger');
if(bt)bt.addEventListener('click',function(){var o=nav.classList.toggle('open');bt.setAttribute('aria-expanded',o)});
var lb;
document.querySelectorAll('.gi').forEach(function(g){g.addEventListener('click',function(){
 if(!lb){lb=document.createElement('dialog');lb.addEventListener('click',function(e){if(e.target===lb)lb.close()});document.body.appendChild(lb)}
 var cap=L==='en'?g.dataset.en:g.dataset.bn,x=L==='en'?'Close':'বন্ধ করুন';
 lb.innerHTML='<figure class="ph"><img alt="" src="'+g.dataset.src+'" onerror="this.remove()"></figure><div class="cap"><span></span><button class="btn ghost" type="button" style="min-height:40px">'+x+'</button></div>';
 lb.querySelector('span').textContent=cap;lb.querySelector('button').onclick=function(){lb.close()};lb.querySelector('img').alt=cap;lb.showModal();
})});
var f=document.getElementById('enq');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var n=document.getElementById('enq-note');n.hidden=false;n.innerHTML=L==='en'?n.dataset.en:n.dataset.bn});
})();
