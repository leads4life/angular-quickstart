(function(){
  /* TOC scroll-spy */
  var toc=document.getElementById('toc');
  if(toc&&'IntersectionObserver' in window){
    var links={};
    toc.querySelectorAll('a[href^="#"]').forEach(function(a){links[a.getAttribute('href').slice(1)]=a;});
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting&&links[en.target.id]){
          Object.keys(links).forEach(function(k){links[k].classList.remove('active');});
          links[en.target.id].classList.add('active');
        }
      });
    },{rootMargin:'-20% 0px -70% 0px'});
    Object.keys(links).forEach(function(id){var s=document.getElementById(id);if(s)io.observe(s);});
  }

  /* Filter chips */
  document.querySelectorAll('.chips[data-target]').forEach(function(group){
    var scope=document.querySelector(group.getAttribute('data-target'));
    if(!scope)return;
    var empty=scope.querySelector('.filter-empty');
    group.addEventListener('click',function(e){
      var chip=e.target.closest('[data-filter]');
      if(!chip)return;
      group.querySelectorAll('[data-filter]').forEach(function(c){c.setAttribute('aria-pressed',c===chip?'true':'false');});
      var f=chip.getAttribute('data-filter'),shown=0;
      scope.querySelectorAll('[data-tags]').forEach(function(item){
        var ok=f==='all'||(' '+item.getAttribute('data-tags')+' ').indexOf(' '+f+' ')>-1;
        item.hidden=!ok;if(ok)shown++;
      });
      scope.querySelectorAll('.menu-block').forEach(function(b){
        b.hidden=!b.querySelector('[data-tags]:not([hidden])');
      });
      if(empty)empty.hidden=shown>0;
      var live=document.getElementById(group.getAttribute('data-live'));
      if(live)live.textContent=shown+' dishes shown';
    });
  });

  /* Hours: %%CITY%%, FL keeps Eastern time */
  var rows=document.querySelectorAll('tr[data-days]');
  if(rows.length){
    var now=new Date(),day,mins;
    try{
      var parts=new Intl.DateTimeFormat('en-US',{timeZone:'%%TZ%%',weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now);
      var get=function(t){for(var i=0;i<parts.length;i++)if(parts[i].type===t)return parts[i].value;};
      day=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(get('weekday'));
      mins=parseInt(get('hour'),10)*60+parseInt(get('minute'),10);
    }catch(err){day=now.getDay();mins=now.getHours()*60+now.getMinutes();}
    var toMin=function(s){var p=s.split(':');return +p[0]*60+ +p[1];};
    var openNow=false,todayRow=null;
    rows.forEach(function(r){
      if(r.getAttribute('data-days').split(' ').indexOf(String(day))>-1){
        r.classList.add('today');todayRow=r;
        var o=toMin(r.getAttribute('data-open')),c=toMin(r.getAttribute('data-close'));
        if(mins>=o&&mins<c)openNow=true;
      }
    });
    document.querySelectorAll('[data-open-status]').forEach(function(el){
      if(!todayRow)return;
      el.hidden=false;
      el.textContent=openNow?'Open now':'Closed now';
      el.classList.add(openNow?'is-open':'is-closed');
    });
  }

  /* Demo forms: validate, then say honestly that nothing was sent */
  document.querySelectorAll('form[data-demo-form]').forEach(function(form){
    var status=form.querySelector('.form-status')||(form.nextElementSibling&&form.nextElementSibling.classList.contains('form-status')?form.nextElementSibling:null);
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var bad=null;
      form.querySelectorAll('[required]').forEach(function(f){
        var ok=f.value.trim()!==''&&(!f.checkValidity||f.checkValidity());
        f.setAttribute('aria-invalid',ok?'false':'true');
        if(!ok&&!bad)bad=f;
      });
      if(!status)return;
      status.hidden=false;
      if(bad){
        status.classList.add('err');
        var lab=form.querySelector('label[for="'+bad.id+'"]');
        status.textContent='Please check '+(lab?lab.textContent.replace('*','').trim():'the highlighted field')+' and try again.';
        bad.focus();
        return;
      }
      status.classList.remove('err');
      status.textContent=form.getAttribute('data-done')||'Thanks. This form is not connected yet, so nothing was sent. Please call us instead.';
    });
  });
})();
