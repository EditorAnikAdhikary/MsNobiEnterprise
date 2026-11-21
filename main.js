(function(){
var L='bn';try{if(localStorage.getItem('lang')==='en')L='en'}catch(e){}
function apply(){
 document.documentElement.lang=L;
 document.querySelectorAll('[data-en]').forEach(function(e){
  if(e.dataset.bn===undefined)e.dataset.bn=e.textContent;
  e.textContent=L==='en'?e.dataset.en:e.dataset.bn;
 });
 document.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===L)});
 var tt=document.querySelector('title');if(tt&&tt.dataset.en){if(!tt.dataset.bn)tt.dataset.bn=tt.textContent;document.title=L==='en'?tt.dataset.en:tt.dataset.bn}
}
document.querySelectorAll('.lang button').forEach(function(b){b.onclick=function(){L=b.dataset.l;try{localStorage.setItem('lang',L)}catch(e){}apply()}});
var bt=document.getElementById('burger'),nv=document.getElementById('nav');
if(bt)bt.onclick=function(){var o=nv.classList.toggle('open');bt.setAttribute('aria-expanded',o)};
var lb=document.getElementById('lb');
document.querySelectorAll('[data-g]').forEach(function(b){b.onclick=function(){
 var p=b.querySelector('.ph').cloneNode(true);var cap=document.createElement('div');cap.className='cap';
 cap.innerHTML='<span></span><button class="btn ghost" style="min-height:40px" type="button"></button>';
 cap.firstChild.textContent=b.getAttribute('aria-label');var c=cap.lastChild;c.textContent=L==='en'?'Close':'বন্ধ করুন';c.onclick=function(){lb.close()};
 lb.innerHTML='';lb.appendChild(p);lb.appendChild(cap);lb.showModal()}});
if(lb)lb.onclick=function(e){if(e.target===lb)lb.close()};
var f=document.getElementById('f');
if(f)f.onsubmit=function(e){e.preventDefault();var n=document.getElementById('fn');n.hidden=false;
 n.textContent=L==='en'?'This form is not connected to a backend yet; your message was NOT sent. Please call 01711-574939.':'এই ফর্মটি এখনও কোনো সার্ভারের সাথে যুক্ত নয়; আপনার বার্তা পাঠানো হয়নি। অনুগ্রহ করে ০১৭১১-৫৭৪৯৩৯ নম্বরে কল করুন।'};
apply();
})();
