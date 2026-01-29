// Clean single-file app.js
function qs(id){ return document.getElementById(id); }

function setStatus(connected){
  const s = qs('statusText');
  s.textContent = connected ? 'Connected' : 'Disconnected';
  s.className = connected ? 'status connected' : 'status disconnected';
}

function showOutput(obj, append = false){
  const out = qs('output');
  const str = typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2);
  if(append && out.textContent) out.textContent = out.textContent + '\n' + str;
  else out.textContent = str;
}

function showApiOutput(obj){
  const out = qs('apiOutput');
  const str = typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2);
  out.textContent = str;
}

async function callApi(){
  let base = qs('apiBase').value.trim();
  const path = qs('apiPath').value.trim();
  // allow empty base: default to current origin so "/status" calls localhost server
  if(!base){
    if(path.startsWith('http://') || path.startsWith('https://')){
      base = path;
      showOutput('Calling ' + base);
    } else {
      base = location.origin;
      showOutput('Calling ' + base + path);
    }
  } else {
    showOutput('Calling ' + base + path);
  }
  try{
    const resp = await fetch('/call', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ base, path })
    });
    const data = await resp.json();
    showApiOutput(data);
  }catch(e){
    showApiOutput('Error: ' + e.message);
  }
}

function saveBase(){
  const base = qs('apiBase').value.trim();
  if(base) localStorage.setItem('demo_api_base', base);
  alert('Saved');
}

function resetBase(){
  localStorage.removeItem('demo_api_base');
  qs('apiBase').value = '';
  alert('Reset');
}

async function checkServer(){
  try{
    const r = await fetch('/status');
    if(r.ok){ setStatus(true); return; }
  }catch(e){}
  setStatus(false);
}

function init(){
  const saved = localStorage.getItem('demo_api_base');
  if(saved) qs('apiBase').value = saved;

  console.log('app.init running');
  const callBtn = qs('callBtn');
  const clearBtn = qs('clearBtn');
  const saveBtn = qs('saveBtn');
  const resetBtn = qs('resetBtn');
  console.log({callBtn, clearBtn, saveBtn, resetBtn});
  if(callBtn) callBtn.addEventListener('click', ()=>{ console.log('callBtn clicked'); callApi(); });
  if(clearBtn) clearBtn.addEventListener('click', ()=>{ console.log('clearBtn clicked'); showOutput(''); showApiOutput(''); });
  if(saveBtn) saveBtn.addEventListener('click', ()=>{ console.log('saveBtn clicked'); saveBase(); });
  if(resetBtn) resetBtn.addEventListener('click', ()=>{ console.log('resetBtn clicked'); resetBase(); });

  checkServer();
  connectWS();
}

window.addEventListener('load', init);

// WebSocket with simple reconnect
let ws = null;
let wsReconnectTimer = null;
function connectWS(){
  if(ws) ws.close();
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = proto + '//' + location.host + '/ws';
  ws = new WebSocket(url);
  ws.addEventListener('open', ()=>{ setStatus(true); /* don't show raw open messages */ });
  ws.addEventListener('close', ()=>{ setStatus(false); scheduleReconnect(); });
  ws.addEventListener('error', (e)=>{ showOutput('WebSocket error'); ws.close(); });
  ws.addEventListener('message', (ev)=>{
    try{
      const data = JSON.parse(ev.data);
      showOutput(data);
    }catch(e){ showOutput(ev.data, true); }
  });
}

function scheduleReconnect(){
  if(wsReconnectTimer) return;
  wsReconnectTimer = setTimeout(()=>{ wsReconnectTimer = null; connectWS(); }, 3000);
}
function qs(id){ return document.getElementById(id); }

function setStatus(connected){
  const s = qs('statusText');
  s.textContent = connected ? 'Connected' : 'Disconnected';
  s.className = connected ? 'status connected' : 'status disconnected';
}

function showOutput(obj, append = false){
  const out = qs('output');
  const str = typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2);
  if(append && out.textContent) out.textContent = out.textContent + '\n' + str;
  else out.textContent = str;
}

async function callApi(){
  const base = qs('apiBase').value.trim();
  const path = qs('apiPath').value.trim();
  if(!base){ alert('Please set API Base'); return; }
  showOutput('Calling ' + base + path);
  try{
    const resp = await fetch('/call', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ base, path })
    });
    const data = await resp.json();
    showOutput(data);
  }catch(e){
    showOutput('Error: ' + e.message);
  }
}

function saveBase(){
  const base = qs('apiBase').value.trim();
  if(base) localStorage.setItem('demo_api_base', base);
  console.log('saveBase: saved', base);
  alert('Saved');
}

function resetBase(){
  localStorage.removeItem('demo_api_base');
  qs('apiBase').value = '';
  console.log('resetBase');
  alert('Reset');
}

async function checkServer(){
  try{
    const r = await fetch('/status');
    if(r.ok){ setStatus(true); return; }
  }catch(e){}
  setStatus(false);
}

function init(){
  const saved = localStorage.getItem('demo_api_base');
  if(saved) qs('apiBase').value = saved;

  qs('callBtn').addEventListener('click', callApi);
  qs('clearBtn').addEventListener('click', ()=> showOutput(''));
  qs('saveBtn').addEventListener('click', saveBase);
  qs('resetBtn').addEventListener('click', resetBase);

  checkServer();
  connectWS();
}

window.addEventListener('load', init);

// WebSocket with simple reconnect
let ws = null;
let wsReconnectTimer = null;
function connectWS(){
  if(ws) ws.close();
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = proto + '//' + location.host + '/ws';
  ws = new WebSocket(url);
  ws.addEventListener('open', ()=>{ setStatus(true); showOutput('WebSocket open'); });
  ws.addEventListener('close', ()=>{ setStatus(false); showOutput('WebSocket closed'); scheduleReconnect(); });
  ws.addEventListener('error', (e)=>{ showOutput('WebSocket error'); ws.close(); });
  ws.addEventListener('message', (ev)=>{
    try{
      const data = JSON.parse(ev.data);
      showOutput(data);
    }catch(e){ showOutput(ev.data, true); }
  });
}

function scheduleReconnect(){
  if(wsReconnectTimer) return;
  wsReconnectTimer = setTimeout(()=>{ wsReconnectTimer = null; connectWS(); }, 3000);
}
