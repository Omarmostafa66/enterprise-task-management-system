/* ═══ PASSWORD VISIBILITY TOGGLE ═══ */
function togglePasswordVisibility(inputId, icon) {
  const input = document.getElementById(inputId);
  if(input.type === 'password') {
    input.type = 'text';
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
  } else {
    input.type = 'password';
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
  }
}

/* ═══ AUTH MODE TOGGLE ═══ */
let isLoginMode = true;

function handleAuthEnter() {
  if (isLoginMode) login();
  else register();
}

function toggleAuthMode(e) {
  if (e) e.preventDefault();
  isLoginMode = !isLoginMode;

  const nameWrap = document.getElementById('regNameWrap');
  const roleWrap = document.getElementById('regRoleWrap');
  const btn = document.getElementById('loginBtn');
  const link = document.getElementById('toggleAuthLink');
  const sub = document.querySelector('.auth-sub');
  const errEl = document.getElementById('authErr');

  errEl.classList.remove('show');

  if (isLoginMode) {
    nameWrap.style.display = 'none';
    roleWrap.style.display = 'none';
    btn.innerHTML = '<i class="fa-solid fa-arrow-right-to-bracket"></i> Sign In';
    btn.setAttribute('onclick', 'login()');
    link.innerText = "Don't have an account? Create one";
    sub.innerText = "Enterprise Workflow Platform";
  } else {
    nameWrap.style.display = 'block';
    roleWrap.style.display = 'block';
    btn.innerHTML = '<i class="fa-solid fa-user-plus"></i> Create Account';
    btn.setAttribute('onclick', 'register()');
    link.innerText = "Already have an account? Sign in";
    sub.innerText = "Register a new enterprise account";
  }
}

/* ═══ REGISTER ═══ */
async function register() {
  const name  = document.getElementById('regName').value.trim();
  const email = document.getElementById('loginEmail').value.trim();
  const pass  = document.getElementById('loginPass').value;
  const role  = document.getElementById('regRole').value;
  const btn   = document.getElementById('loginBtn');
  const errEl = document.getElementById('authErr');
  const errMsg= document.getElementById('authErrMsg');

  errEl.classList.remove('show');

  if (!name) {
    flashErr('regName');
    shake(document.querySelector('.auth-card'));
    return;
  }
  if (!email || !isValidEmail(email)) {
    errMsg.textContent = 'Please enter a valid email address';
    errEl.classList.add('show');
    flashErr('loginEmail');
    shake(document.querySelector('.auth-card'));
    return;
  }
  if (!pass || !isStrongPassword(pass)) {
    errMsg.textContent = 'Password must be at least 8 characters (letters & numbers)';
    errEl.classList.add('show');
    flashErr('loginPass');
    shake(document.querySelector('.auth-card'));
    return;
  }

  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin-slow"></i> Registering...';
  btn.disabled = true;

  try {
    loadStart();
    const res = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, full_name: name, password: pass, role: role })
    });
    const data = await res.json();
    loadDone();

    if (res.ok) {
      /* Automatically login after successful registration */
      login();
    } else {
      errMsg.textContent = data.detail || 'Registration failed';
      errEl.classList.add('show');
      shake(document.querySelector('.auth-card'));
      btn.innerHTML = '<i class="fa-solid fa-user-plus"></i> Create Account';
      btn.disabled = false;
    }
  } catch(e) {
    loadDone();
    errMsg.textContent = 'Backend server offline';
    errEl.classList.add('show');
    btn.innerHTML = '<i class="fa-solid fa-user-plus"></i> Create Account';
    btn.disabled = false;
  }
}

/* ═══ LOGIN ═══ */
async function login(){
  const email = document.getElementById('loginEmail').value.trim();
  const pass  = document.getElementById('loginPass').value;
  const btn   = document.getElementById('loginBtn');
  const errEl = document.getElementById('authErr');
  const errMsg= document.getElementById('authErrMsg');

  errEl.classList.remove('show');

  if(!email || !isValidEmail(email)){
    errMsg.textContent = 'Please enter a valid email address';
    errEl.classList.add('show');
    flashErr('loginEmail');
    shake(document.querySelector('.auth-card'));
    return;
  }
  if(!pass){
    flashErr('loginPass');
    shake(document.querySelector('.auth-card'));
    return;
  }

  btn.innerHTML='<i class="fa-solid fa-circle-notch fa-spin-slow"></i> Signing in...';
  btn.disabled=true;

  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', pass);

  try{
    loadStart();
    const res  = await fetch(`${API_URL}/auth/login`,{
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body: params
    });
    const data = await res.json();
    loadDone();

    if(res.ok && data.access_token){
      localStorage.setItem('token', data.access_token);
      TOKEN = data.access_token;

      CURRENT_USER_ROLE = String(data.role)
       .toLowerCase()
       .replace("userrole.", "")
       .trim();
      CURRENT_USER_EMAIL = email;
      localStorage.setItem('role',  CURRENT_USER_ROLE);
      localStorage.setItem('email', CURRENT_USER_EMAIL);

      const card = document.querySelector('.auth-card');
      card.style.animation='scaleOut .28s ease forwards';
      setTimeout(()=>showDashboard(), 300);
    } else {
      errMsg.textContent = data.detail || 'Authentication failed';
      errEl.classList.add('show');
      shake(document.querySelector('.auth-card'));
      btn.innerHTML='<i class="fa-solid fa-arrow-right-to-bracket"></i> Sign In';
      btn.disabled=false;
    }
  } catch(e){
    loadDone();
    errMsg.textContent='Backend server offline';
    errEl.classList.add('show');
    btn.innerHTML='<i class="fa-solid fa-arrow-right-to-bracket"></i> Sign In';
    btn.disabled=false;
  }
}

/* ═══ LOGOUT (WITH CUSTOM MODAL) ═══ */
function logout(){
  if(typeof customConfirm === 'function') {
    customConfirm("Are you sure you want to log out and end the session?", () => {
      executeLogout();
    }, 'btn-d', 'Logout');
  } else {
    if(confirm("Log out?")) executeLogout();
  }
}

function executeLogout() {
  document.querySelector('#dashboardSection .page').style.opacity='0';
  document.querySelector('#dashboardSection .page').style.transition='opacity .3s';
  setTimeout(()=>{ localStorage.clear(); location.reload(); }, 300);
}

/* ═══ SHOW DASHBOARD ═══ */
function showDashboard(){
  document.getElementById('authSection').classList.add('hidden');
  document.getElementById('dashboardSection').classList.remove('hidden');
  loadDashboard();
  setTimeout(()=>applyRoleUI(), 350);
}

/* ═══ ROLE UI ═══ */
function applyRoleUI(){
  const role = CURRENT_USER_ROLE || 'employee';

  /* Topbar user chip */
  const email = CURRENT_USER_EMAIL || '';
  document.getElementById('ucEmail').textContent = email;
  const initials = email ? email[0].toUpperCase() : 'U';
  document.getElementById('ucAvatar').textContent = initials;

  const chip = document.getElementById('ucRoleChip');
  chip.className = 'uc-role';
  if(role==='admin')           { chip.classList.add('r-admin');    chip.textContent='Admin'; }
  else if(role==='project_manager'){ chip.classList.add('r-pm');   chip.textContent='Proj. Manager'; }
  else                         { chip.classList.add('r-employee'); chip.textContent='Employee'; }

  /* Session card */
  const rt = document.getElementById('roleTitle');
  const rs = document.getElementById('roleSubtext');
  if(role==='admin')           { rt.textContent='Administrator';    rs.textContent='Full access granted'; }
  else if(role==='project_manager'){ rt.textContent='Project Manager'; rs.textContent='Project & task management'; }
  else                         { rt.textContent='Employee';         rs.textContent='Task view & status updates'; }

  /* Panel visibility */
  const cpPanel = document.getElementById('createProjectPanel');
  const dtPanel = document.getElementById('deployTaskPanel');
  const userPanel = document.getElementById('usersManagementPanel');
  const auditPanel = document.getElementById('auditLogsPanel');

  if(role==='admin') {
    if(userPanel) userPanel.style.display='block';
    if(auditPanel) auditPanel.style.display='block';
  } else if(role==='employee'){
    if(cpPanel) cpPanel.style.display='none';
    if(dtPanel) dtPanel.style.display='none';
    document.querySelectorAll('.delete-btn').forEach(b=>b.style.display='none');
  } else if(role==='project_manager'){
    if(cpPanel) cpPanel.style.display='none';
  }
}

/* ═══ PROFILE MODAL LOGIC ═══ */
function openProfile() {
  document.getElementById('profEmail').value = CURRENT_USER_EMAIL || 'N/A';

  let roleFormatted = (CURRENT_USER_ROLE || 'employee').replace('_', ' ');
  document.getElementById('profRole').value = roleFormatted;

  document.getElementById('profPass').value = '';
  document.getElementById('profileModal').classList.remove('hidden');
}

function closeProfile() {
  document.getElementById('profileModal').classList.add('hidden');
}

async function updateProfile() {
  const passInput = document.getElementById('profPass');
  const newPass = passInput.value;

  if (!newPass) {
    /* If empty, no changes are made. Close modal */
    closeProfile();
    return;
  }

  if (!isStrongPassword(newPass)) {
    flashErr('profPass');
    toast('Password must be at least 8 characters with letters & numbers', 'error');
    shake(document.querySelector('.modal'));
    return;
  }

  const btn = document.getElementById('profSaveBtn');
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin-slow"></i> Saving...';
  btn.disabled = true;

  try {
    loadStart();
    /* NOTE: Requires a matching PUT endpoint at the backend to handle this request */
    const res = await fetch(`${API_URL}/users/me`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${TOKEN}` },
      body: JSON.stringify({ password: newPass })
    });
    loadDone();

    if (res.ok) {
      toast('Password updated successfully');
      closeProfile();
    } else {
      const data = await res.json();
      toast(data.detail || 'Update failed', 'error');
      shake(document.querySelector('.modal'));
    }
  } catch(e) {
    loadDone();
    toast('Backend server offline', 'error');
  } finally {
    btn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes';
    btn.disabled = false;
  }
}

/* ═══ REFRESH ═══ */
function refreshDash(){
  const icon = document.getElementById('ri');
  icon.classList.add('fa-spin-slow');
  loadStart();

  const promises = [loadProjects(), loadTasks()];
  if (CURRENT_USER_ROLE === 'admin' && typeof loadUsersList === 'function') promises.push(loadUsersList());
  if (CURRENT_USER_ROLE !== 'employee' && typeof loadUsersForTaskAssignment === 'function') promises.push(loadUsersForTaskAssignment());

  Promise.all(promises)
    .finally(()=>{ setTimeout(()=>icon.classList.remove('fa-spin-slow'),600); loadDone(); });
}

function loadDashboard(){
  loadProjects();
  loadTasks();
  if (CURRENT_USER_ROLE === 'admin' && typeof loadUsersList === 'function') loadUsersList();
  if (CURRENT_USER_ROLE !== 'employee' && typeof loadUsersForTaskAssignment === 'function') loadUsersForTaskAssignment();
}