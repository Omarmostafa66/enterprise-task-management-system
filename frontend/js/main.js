const API_URL = "http://localhost:8000";
let TOKEN = localStorage.getItem("token");
let ALL_TASKS = [];
let FILTERED_TASKS = [];
let CURRENT_PAGE = 1;
const ITEMS_PER_PAGE = 5;
let CURRENT_USER_ROLE  = null;
let CURRENT_USER_EMAIL = null;

/* Init from storage */
CURRENT_USER_ROLE  = localStorage.getItem('role');
CURRENT_USER_EMAIL = localStorage.getItem('email');

/* Loading bar */
const LB = document.getElementById('loadingBar');
function loadStart(){ LB.style.width='40%'; LB.style.opacity='1'; }
function loadDone() { LB.style.width='100%'; setTimeout(()=>{ LB.style.opacity='0'; setTimeout(()=>LB.style.width='0',300); },300); }

/* Toast */
function toast(msg, type='success'){
  const wrap = document.getElementById('toastWrap');
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.innerHTML = `<i class="fa-solid ${type==='success'?'fa-circle-check':'fa-circle-exclamation'}"></i>${msg}`;
  wrap.appendChild(t);
  setTimeout(()=>{ t.style.animation='toastOut .3s ease forwards'; setTimeout(()=>t.remove(),300); }, 3200);
}

/* Ripple */
document.addEventListener('click', e=>{
  const btn = e.target.closest('.btn-p,.btn-d');
  if(!btn) return;
  const r = document.createElement('span');
  r.className='rpl';
  const rect = btn.getBoundingClientRect();
  r.style.left=(e.clientX-rect.left)+'px';
  r.style.top=(e.clientY-rect.top)+'px';
  btn.appendChild(r);
  setTimeout(()=>r.remove(), 650);
});

/* Count anim */
function animNum(el, target){
  const from = parseInt(el.innerText)||0;
  if(from===target) return;
  const dur=520, t0=performance.now();
  const run = ts=>{
    const p = Math.min((ts-t0)/dur,1);
    const ease = 1-Math.pow(1-p,3);
    el.innerText = Math.round(from+(target-from)*ease);
    if(p<1) requestAnimationFrame(run);
  };
  requestAnimationFrame(run);
}

/* Bump */
function bump(id, val){
  const el = document.getElementById(id);
  if(!el) return;
  el.innerText = val;
  el.classList.remove('bump');
  void el.offsetWidth;
  el.classList.add('bump');
}

/* Flash error */
function flashErr(id){
  const el = document.getElementById(id);
  if(!el) return;
  el.classList.add('err');
  el.focus();
  setTimeout(()=>el.classList.remove('err'),1400);
}

/* Shake */
function shake(el){
  if(!el) return;
  el.style.animation='shake .4s ease';
  setTimeout(()=>el.style.animation='',500);
}

/* ═══ CUSTOM CONFIRMATION MODAL LOGIC ═══ */
let confirmActionCallback = null;

function customConfirm(msg, callback, btnClass = 'btn-d', btnText = 'Confirm') {
  document.getElementById('confirmMessage').innerText = msg;
  const btn = document.getElementById('confirmBtn');
  btn.className = `btn ${btnClass}`;
  btn.innerText = btnText;
  confirmActionCallback = callback;
  document.getElementById('confirmModal').classList.remove('hidden');
}

function closeConfirmModal() {
  document.getElementById('confirmModal').classList.add('hidden');
  confirmActionCallback = null;
}

document.getElementById('confirmBtn')?.addEventListener('click', () => {
  if (confirmActionCallback) confirmActionCallback();
  closeConfirmModal();
});

/* Restore on load */
if(TOKEN) showDashboard();

/* ═══ VALIDATION HELPERS ═══ */
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function isStrongPassword(pwd) {
  /* At least 8 characters long, must contain at least one letter and one number */
  const re = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/;
  return re.test(pwd);
}

/* ═══ LOAD AUDIT LOGS FOR ADMIN ═══ */
async function loadAuditLogs() {
  if (CURRENT_USER_ROLE !== 'admin') return;
  const list = document.getElementById('auditList');
  if(!list) return;

  try {
    const res = await fetch(`${API_URL}/auth/audit-logs`, {headers:{'Authorization':`Bearer ${TOKEN}`}});
    if(res.ok) {
      const data = await res.json();
      const logs = data.logs || [];

      if(!logs.length || (logs.length === 1 && logs[0].includes("No logs"))) {
        list.innerHTML = `<div class="empty-state"><i class="fa-solid fa-check-double"></i><p>No system activity recorded yet.</p></div>`;
        return;
      }

      /* Reverse array to show newest logs on top */
      list.innerHTML = logs.reverse().map((log, i) => `
        <div style="padding:8px 10px; border-bottom:1px solid var(--line2); font-family:var(--mono); font-size:11px; color:var(--t1); animation-delay:${i*0.02}s;" class="tc">
           ${log.replace(/\|/g, '<span style="color:var(--line3); margin:0 6px;">|</span>')}
        </div>
      `).join('');
    }
  } catch(e) {
    list.innerHTML = `<div class="empty-state"><p>Error connecting to audit service.</p></div>`;
  }
}