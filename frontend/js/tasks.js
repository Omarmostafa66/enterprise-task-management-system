/* ═══ LOAD TASKS ═══ */
async function loadTasks(){
  try{
    const res   = await fetch(`${API_URL}/tasks/`,{headers:{'Authorization':`Bearer ${TOKEN}`}});
    const tasks = await res.json();
    ALL_TASKS = tasks;

    animNum(document.getElementById('tasksCountCard'),   tasks.length);
    const done = tasks.filter(t=>t.status==='Done').length;
    animNum(document.getElementById('doneTasksCard'),    done);
    animNum(document.getElementById('pendingTasksCard'), tasks.length-done);
    const pct = tasks.length ? Math.round((done/tasks.length)*100) : 0;

    setTimeout(()=>{
      document.getElementById('progressBar').style.width=`${pct}%`;
      document.getElementById('progressText').innerText=`${pct}%`;
    }, 100);

    filterTasks();
  }catch(e){
    console.error(e);
    document.getElementById('taskTableBody').innerHTML='<div class="empty-state"><p>Error connecting to server</p></div>';
  }
}

/* ═══ FILTER TASKS ═══ */
function filterTasks(){
  const s  = document.getElementById('searchTask').value.toLowerCase();
  const st = document.getElementById('statusFilter').value;
  const pr = document.getElementById('priorityFilter') ? document.getElementById('priorityFilter').value : '';
  const as = document.getElementById('assigneeFilter') ? document.getElementById('assigneeFilter').value : '';

  FILTERED_TASKS = ALL_TASKS.filter(t => {
    const matchSearch = t.title.toLowerCase().includes(s);
    const matchStatus = !st || t.status === st;
    const matchPriority = !pr || t.priority === pr;
    const matchAssignee = !as || String(t.assignee_id) === as;
    return matchSearch && matchStatus && matchPriority && matchAssignee;
  });

  CURRENT_PAGE = 1;
  applyPagination();
}

/* ═══ PAGINATION LOGIC ═══ */
function applyPagination() {
  const totalPages = Math.ceil(FILTERED_TASKS.length / ITEMS_PER_PAGE) || 1;
  if (CURRENT_PAGE > totalPages) CURRENT_PAGE = totalPages;

  const startIndex = (CURRENT_PAGE - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedItems = FILTERED_TASKS.slice(startIndex, endIndex);

  renderTasks(paginatedItems);

  const pageInfo = document.getElementById('pageInfo');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  if(pageInfo) pageInfo.innerText = `Page ${CURRENT_PAGE} of ${totalPages}`;
  if(prevBtn) prevBtn.disabled = (CURRENT_PAGE === 1);
  if(nextBtn) nextBtn.disabled = (CURRENT_PAGE === totalPages);
}

function prevPage() {
  if (CURRENT_PAGE > 1) {
    CURRENT_PAGE--;
    applyPagination();
  }
}

function nextPage() {
  const totalPages = Math.ceil(FILTERED_TASKS.length / ITEMS_PER_PAGE) || 1;
  if (CURRENT_PAGE < totalPages) {
    CURRENT_PAGE++;
    applyPagination();
  }
}

/* ═══ RENDER TASKS ═══ */
function renderTasks(tasks){
  const body = document.getElementById('taskTableBody');
  if(!tasks.length){
    body.innerHTML='<div class="empty-state"><i class="fa-solid fa-inbox"></i><p>No tasks found</p></div>';
    return;
  }
  const ic = {High:'hi', Medium:'mi', Low:'li'};
  const bc = {High:'bh', Medium:'bm', Low:'bl'};
  const pi = {High:'fa-circle-exclamation', Medium:'fa-circle-minus', Low:'fa-circle-arrow-down'};

  body.innerHTML = tasks.map((t,i)=> {
    let statusOptions = '';
    const isDone = t.status === 'Done';
    const disableSelect = isDone ? 'disabled style="opacity:0.6; cursor:not-allowed;"' : '';

    if (t.status === 'To Do') {
        statusOptions = `<option selected>To Do</option><option>In Progress</option>`;
    } else if (t.status === 'In Progress') {
        statusOptions = `<option>To Do</option><option selected>In Progress</option><option>Done</option>`;
    } else if (t.status === 'Done') {
        statusOptions = `<option selected>Done</option>`;
    }

    return `
    <div class="tc" id="tc-${t.id}" style="animation-delay:${i*.04}s">
      <div class="tc-icon ${ic[t.priority]||'li'}">
        <i class="fa-solid ${pi[t.priority]||'fa-circle-arrow-down'}"></i>
      </div>
      <div class="tc-meta">
        <div class="tc-id">TASK-${String(t.id).padStart(4,'0')}</div>
        <div class="tc-name">${t.title}</div>
      </div>
      <div class="tc-actions">
        <select onchange="updateTaskStatus(${t.id},this.value)" class="ssel" ${disableSelect}>
          ${statusOptions}
        </select>
        <span class="badge ${bc[t.priority]||'bl'}">${t.priority}</span>
        <button
          onclick="deleteTask(${t.id})"
          class="btn-i delete-btn"
          title="Delete task"
          style="${CURRENT_USER_ROLE==='employee'?'display:none':''}"
        >
          <i class="fa-solid fa-trash" style="font-size:12px"></i>
        </button>
      </div>
    </div>`
  }).join('');
}

/* ═══ LOAD PROJECTS DROPDOWN FOR TASK DEPLOYMENT ═══ */
async function loadProjectsForTaskDeployment() {
  if (CURRENT_USER_ROLE === 'employee') return;
  try {
    const res = await fetch(`${API_URL}/projects/`, {headers:{'Authorization':`Bearer ${TOKEN}`}});
    if (res.ok) {
      const projects = await res.json();
      const sel = document.getElementById('taskProjId');
      if (sel) {
        sel.innerHTML = '<option value="">Select Project</option>' +
          projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      }
    }
  } catch(e) { console.error("Error fetching projects for dropdown"); }
}

/* ═══ CREATE TASK ═══ */
async function createTask(){
  const title  = document.getElementById('taskTitle').value.trim();
  const projId = document.getElementById('taskProjId').value;
  const priority = document.getElementById('taskPriority').value;
  const assignee = document.getElementById('taskAssignee') ? document.getElementById('taskAssignee').value : '';

  if(!title)  { flashErr('taskTitle');  return; }
  if(!projId) { flashErr('taskProjId'); toast('Please select a project', 'error'); return; }

  const payload = { title, priority, project_id: parseInt(projId), status: "To Do" };
  if(assignee) payload.assignee_id = parseInt(assignee);

  try {
    loadStart();
    const res = await fetch(`${API_URL}/tasks/`,{
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':`Bearer ${TOKEN}`},
      body: JSON.stringify(payload)
    });
    loadDone();

    if(res.ok){
      document.getElementById('taskTitle').value='';
      loadTasks();
      toast('Task deployed successfully');
    } else {
      const e = await res.json();
      toast(e.detail||'Task creation failed','error');
    }
  } catch(e) {
    loadDone();
    toast('Failed to connect to server', 'error');
  }
}

/* ═══ UPDATE STATUS ═══ */
async function updateTaskStatus(id, status){
  try {
    const res = await fetch(`${API_URL}/tasks/${id}`,{
      method:'PUT',
      headers:{'Content-Type':'application/json','Authorization':`Bearer ${TOKEN}`},
      body: JSON.stringify({status})
    });
    if(res.ok){
      loadTasks();
      toast('Status updated');
    } else {
      const e = await res.json();
      toast(e.detail||'Update failed','error');
      loadTasks();
    }
  } catch(e) {
    toast('Network error', 'error');
    loadTasks();
  }
}

/* ═══ DELETE TASK ═══ */
function deleteTask(id){
  if(typeof customConfirm === 'function') {
    customConfirm(`Are you sure you want to delete task #${id}? This action cannot be undone.`, async () => {
      executeTaskDeletion(id);
    }, 'btn-d', 'Delete Task');
  } else {
    if(confirm(`Delete task #${id}?`)) executeTaskDeletion(id);
  }
}

async function executeTaskDeletion(id) {
  const card = document.getElementById(`tc-${id}`);
  if(card){
    card.style.transition='opacity .22s,transform .22s';
    card.style.opacity='0';
    card.style.transform='translateX(16px)';
  }
  try {
    const res = await fetch(`${API_URL}/tasks/${id}`,{
      method:'DELETE',
      headers:{'Authorization':`Bearer ${TOKEN}`}
    });
    if(res.ok){ setTimeout(()=>loadTasks(), 230); toast('Task deleted'); }
    else { toast('Unauthorized action','error'); loadTasks(); }
  } catch(e) {
    toast('Network error during deletion', 'error');
    loadTasks();
  }
}

/* ═══ LOAD ASSIGNEES DROPDOWN ═══ */
async function loadUsersForTaskAssignment() {
  if (CURRENT_USER_ROLE === 'employee') return;
  try {
    const res = await fetch(`${API_URL}/auth/users`, {headers:{'Authorization':`Bearer ${TOKEN}`}});
    if (res.ok) {
      const users = await res.json();
      const sel = document.getElementById('taskAssignee');
      if (sel) {
        // Only active users can be assigned tasks
        const activeUsers = users.filter(u => u.is_active !== false);
        sel.innerHTML = '<option value="">Unassigned</option>' +
          activeUsers.map(u => `<option value="${u.id}">${u.full_name} (${u.role})</option>`).join('');
      }
    }
  } catch(e) { console.error("Error fetching users for assignment"); }
}