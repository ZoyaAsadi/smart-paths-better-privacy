<%@ taglib prefix="cms" uri="http://www.opencms.org/taglib/cms" %>

<!-- Always keep Klaro banner on top and hide the Mercury banner -->
<style>
  #mercury-privacy-banner { display: none !important; }
  .cm-wrapper { z-index: 999999 !important; }
</style>

<!-- 1) Klaro config must be loaded before the library -->
<script defer src="<cms:link>%(link.weak:/system/modules/zoya.consent/resources/js/klaro-config.js:f055adb6-88aa-11f0-b717-c6305a13d92a)</cms:link>?v=8"></script>

<!-- 2) Klaro itself (data-config must be 'klaroConfig') -->
<script defer data-config="klaroConfig"
        src="<cms:link>%(link.weak:/system/modules/zoya.consent/resources/js/klaro.js:795a2ae9-88ac-11f0-b717-c6305a13d92a)</cms:link>?v=8"></script>

<!-- 3) Automatically send consent data to the OpenCms server -->
<script>
(function () {
  var ENDPOINT = '/opencms/system/modules/com.zoya.consents/elements/consent-save.jsp';

  function getCookie(name){
    var hit = document.cookie.split('; ').find(function (r){ return r.indexOf(name + '=') === 0; });
    return hit ? hit.split('=').slice(1).join('=') : '';
  }

  // Input can be raw URL-encoded or JSON; output is always a clean JSON string
  function normalize(raw){
    if (!raw) return '';
    try { raw = decodeURIComponent(raw); } catch(e){}
    // Remove surrounding double quotes if present (some builds do this)
    if (raw.length > 1 && raw[0] === '"' && raw[raw.length - 1] === '"') {
      raw = raw.slice(1, -1);
    }
    // If it's valid JSON, serialize it to a standardized JSON string
    try { return JSON.stringify(JSON.parse(raw)); } catch(e) { /* raw already plain JSON text */ }
    return raw;
  }

  function postConsents(rawJson){
    if (!rawJson) return;
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      credentials: 'same-origin',
      body: 'consents=' + encodeURIComponent(rawJson)
    }).catch(function(e){ /* optional: console.error(e) */ });
  }

  function sendFromCookies(){
    // First try 'ol-consent' (the cookie name set in your config), fallback to 'klaro'
    var raw = normalize(getCookie('ol-consent') || getCookie('klaro'));
    postConsents(raw);
  }

  // Path A: Official Klaro event (if enabled)
  document.addEventListener('klaro:save', function(ev){
    // Some builds put the state in ev.detail.state
    var raw = '';
    if (ev && ev.detail && ev.detail.state) {
      try { raw = JSON.stringify(ev.detail.state); } catch(e){}
    }
    if (!raw) { sendFromCookies(); } else { postConsents(raw); }
  });

  // Path B: Backup — send once on page load if cookie exists
  window.addEventListener('load', function(){
    sendFromCookies();
  });

  // Path C: General backup — send shortly after clicking Klaro modal buttons
  document.addEventListener('click', function(ev){
    var btn = ev.target.closest('#klaro [type="submit"], #klaro button');
    if (!btn) return;
    setTimeout(sendFromCookies, 300);
  });
})();
</script>
<%@ taglib prefix="cms" uri="http://www.opencms.org/taglib/cms" %>

<!-- Always keep Klaro banner on top and hide the Mercury banner -->
<style>
  #mercury-privacy-banner { display: none !important; }
  .cm-wrapper { z-index: 999999 !important; }
</style>

<!-- 1) Klaro config must be loaded before the library -->
<script defer src="<cms:link>%(link.weak:/system/modules/zoya.consent/resources/js/klaro-config.js:f055adb6-88aa-11f0-b717-c6305a13d92a)</cms:link>?v=8"></script>

<!-- 2) Klaro itself (data-config must be 'klaroConfig') -->
<script defer data-config="klaroConfig"
        src="<cms:link>%(link.weak:/system/modules/zoya.consent/resources/js/klaro.js:795a2ae9-88ac-11f0-b717-c6305a13d92a)</cms:link>?v=8"></script>

<!-- 3) Automatically send consent data to the OpenCms server -->
<script>
(function () {
  var ENDPOINT = '/opencms/system/modules/com.zoya.consents/elements/consent-save.jsp';

  function getCookie(name){
    var hit = document.cookie.split('; ').find(function (r){ return r.indexOf(name + '=') === 0; });
    return hit ? hit.split('=').slice(1).join('=') : '';
  }

  // Input can be raw URL-encoded or JSON; output is always a clean JSON string
  function normalize(raw){
    if (!raw) return '';
    try { raw = decodeURIComponent(raw); } catch(e){}
    // Remove surrounding double quotes if present (some builds do this)
    if (raw.length > 1 && raw[0] === '"' && raw[raw.length - 1] === '"') {
      raw = raw.slice(1, -1);
    }
    // If it's valid JSON, serialize it to a standardized JSON string
    try { return JSON.stringify(JSON.parse(raw)); } catch(e) { /* raw already plain JSON text */ }
    return raw;
  }

  function postConsents(rawJson){
    if (!rawJson) return;
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      credentials: 'same-origin',
      body: 'consents=' + encodeURIComponent(rawJson)
    }).catch(function(e){ /* optional: console.error(e) */ });
  }

  function sendFromCookies(){
    // First try 'ol-consent' (the cookie name set in your config), fallback to 'klaro'
    var raw = normalize(getCookie('ol-consent') || getCookie('klaro'));
    postConsents(raw);
  }

  // Path A: Official Klaro event (if enabled)
  document.addEventListener('klaro:save', function(ev){
    // Some builds put the state in ev.detail.state
    var raw = '';
    if (ev && ev.detail && ev.detail.state) {
      try { raw = JSON.stringify(ev.detail.state); } catch(e){}
    }
    if (!raw) { sendFromCookies(); } else { postConsents(raw); }
  });

  // Path B: Backup — send once on page load if cookie exists
  window.addEventListener('load', function(){
    sendFromCookies();
  });

  // Path C: General backup — send shortly after clicking Klaro modal buttons
  document.addEventListener('click', function(ev){
    var btn = ev.target.closest('#klaro [type="submit"], #klaro button');
    if (!btn) return;
    setTimeout(sendFromCookies, 300);
  });
})();
 // </script>


 // <script>
(function () {
  function getCookie(name){
    var parts = document.cookie.split('; ').filter(function (r){ return r.startsWith(name + '='); });
    if (!parts.length) return '';
    return decodeURIComponent(parts[0].split('=').slice(1).join('='));
  }
  function postConsents(rawJson){
    fetch('/opencms/system/modules/com.zoya.consents/elements/consent-save.jsp', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
      credentials: 'same-origin',
      body: 'consents=' + encodeURIComponent(rawJson || '{}')
    }).catch(console.error);
  }

  // A) When the user clicks Klaro buttons
  document.addEventListener('klaro:save', function (ev) {
    var raw = '';
    try {
      // Some builds send the state inside the event object
      if (ev && ev.detail && ev.detail.state) raw = JSON.stringify(ev.detail.state);
    } catch(e){}
    if (!raw) raw = getCookie('ol-consent') || getCookie('klaro'); // fallback
    if (raw) postConsents(raw);
  });

  // B) Backup: also send once on page load if a cookie exists
  window.addEventListener('load', function () {
    var raw = getCookie('ol-consent') || getCookie('klaro');
    if (raw) postConsents(raw);
  });
})();
</script>
