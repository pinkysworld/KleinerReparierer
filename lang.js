(function(){
  // English by default; German only when chosen (or the browser is German)
  var l;
  try{l=localStorage.getItem('kr_lang')}catch(e){}
  if(!l){l=(navigator.language||'en').slice(0,2)==='de'?'de':'en'}
  document.documentElement.lang=l;
  window.toggleLang=function(){
    l=l==='de'?'en':'de';document.documentElement.lang=l;
    try{localStorage.setItem('kr_lang',l)}catch(e){}
  };
})();
