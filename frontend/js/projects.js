/* ═══ LOAD PROJECTS ═══ */
async function loadProjects() {
  try {
    const res = await fetch(`${API_URL}/projects/`, { headers: { 'Authorization': `Bearer ${TOKEN}` } });
    const projects = await res.json();

    bump('projCount', projects.length);
    animNum(document.getElementById('projectsCountCard'), projects.length);

    const list = document.getElementById('projectList');

    /* Populate the Projects Dropdown in Deploy Task Panel */
    if (CURRENT_USER_ROLE !== 'employee') {
      const taskProjSel = document.getElementById('taskProjId');
      if (taskProjSel) {
        taskProjSel.innerHTML = '<option value="">Select Project</option>' +
          projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      }
    }

    if (res.ok) {
      if (!projects.length) {
        list.innerHTML = '<div class="empty-state"><i class="fa-solid fa-folder-open"></i><p>No projects yet</p></div>';
        return;
      }

      list.innerHTML = projects.map((p, i) => `
        <div class="proj-item" style="animation-delay:${i * .05}s; cursor:pointer;" onclick="viewProject(${p.id}, '${p.name}')">
          <div class="proj-num">#${p.id}</div>
          <div style="flex:1;min-width:0">
            <div class="proj-name">${p.name}</div>
            <div class="proj-sub">Project ID ${p.id}</div>
          </div>
          <i class="fa-solid fa-chevron-right" style="color:var(--t3);font-size:10px;flex-shrink:0"></i>
        </div>`).join('');
    }
  } catch (e) {
    console.error(e);
  }
}

/* ═══ LOAD MANAGERS DROPDOWN FOR PROJECT CREATION ═══ */
async function loadManagersForProject() {
  if (CURRENT_USER_ROLE === 'employee') return;
  try {
    const res = await fetch(`${API_URL}/auth/users`, { headers: { 'Authorization': `Bearer ${TOKEN}` } });
    if (res.ok) {
      const users = await res.json();
      const sel = document.getElementById('projManager');
      if (sel) {
        /* Filter out normal employees, only Admins or PMs can manage a project */
        const managers = users.filter(u => u.role === 'admin' || u.role === 'project_manager');
        sel.innerHTML = '<option value="">Select Manager</option>' +
          managers.map(u => `<option value="${u.id}">${u.full_name} (${u.role})</option>`).join('');
      }
    }
  } catch (e) {
    console.error("Error fetching managers");
  }
}

/* ═══ CREATE PROJECT ═══ */
async function createProject() {
  const name = document.getElementById('projName').value.trim();
  const desc = document.getElementById('projDesc').value.trim() || "No description provided";
  const managerId = document.getElementById('projManager').value;

  if (!name) {
    flashErr('projName');
    return;
  }
  if (!managerId) {
    flashErr('projManager');
    toast('Please assign a project manager', 'error');
    return;
  }

  loadStart();
  try {
    const res = await fetch(`${API_URL}/projects/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${TOKEN}` },
      body: JSON.stringify({ name, description: desc, manager_id: parseInt(managerId) })
    });

    loadDone();

    if (res.ok) {
      document.getElementById('projName').value = '';
      document.getElementById('projDesc').value = '';
      document.getElementById('projManager').value = '';

      /* Reload projects to update both the list and the Deploy Task dropdown */
      loadProjects();

      toast('Project created successfully');
    } else {
      toast('Only admins can create projects', 'error');
    }
  } catch (e) {
    loadDone();
    toast('Server connection failed', 'error');
  }
}

/* ═══ VIEW DETAILED PROJECT MODAL ═══ */
async function viewProject(id, name) {
  document.getElementById('pmTitle').innerText = name;
  const content = document.getElementById('pmContent');

  content.innerHTML = `<div style="text-align:center; padding:20px;"><i class="fa-solid fa-circle-notch fa-spin"></i> Loading details...</div>`;
  document.getElementById('projectModal').classList.remove('hidden');

  try {
    const res = await fetch(`${API_URL}/projects/${id}`, { headers: { 'Authorization': `Bearer ${TOKEN}` } });
    const project = await res.json();

    if (res.ok) {
      const tasks = project.tasks || [];
      const doneTasks = tasks.filter(t => t.status === 'Done').length;
      const progress = tasks.length ? Math.round((doneTasks / tasks.length) * 100) : 0;

      let tasksHtml = tasks.length ? tasks.map(t => `
        <div style="padding:10px; background:var(--ink3); border:1px solid var(--line2); border-radius:8px; margin-bottom:8px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <strong style="color:var(--t0); font-size:13px;">${t.title}</strong>
            <span class="badge ${t.status === 'Done' ? 'bl' : 'bm'}">${t.status}</span>
          </div>
          <div style="font-size:11px; color:var(--t2);">Assignee ID: ${t.assignee_id || 'Unassigned'} | Priority: ${t.priority}</div>
        </div>
      `).join('') : '<p style="font-size:12px; color:var(--t2); text-align:center;">No tasks deployed for this project yet.</p>';

      content.innerHTML = `
        <div style="margin-bottom:16px;">
          <div style="font-size:12px; color:var(--t2); margin-bottom:4px;">Project Description:</div>
          <div style="font-size:13px; color:var(--t0);">${project.description || 'No description provided.'}</div>
        </div>
        <div style="margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; font-size:12px; color:var(--t2); margin-bottom:6px;">
            <span>Completion Progress</span>
            <span style="color:var(--t0); font-weight:600;">${progress}%</span>
          </div>
          <div class="prog-track" style="margin-top:0; height:6px;"><div class="prog-fill" style="width:${progress}%"></div></div>
        </div>
        <div>
          <div style="font-size:12px; color:var(--t2); margin-bottom:10px; border-bottom:1px solid var(--line2); padding-bottom:6px;">Tasks Overview (${tasks.length})</div>
          <div style="max-height:220px; overflow-y:auto; padding-right:4px;">${tasksHtml}</div>
        </div>
      `;
    } else {
      content.innerHTML = `<div style="text-align:center; color:var(--red); padding:20px;">Failed to load project details.</div>`;
    }
  } catch (e) {
    content.innerHTML = `<div style="text-align:center; color:var(--red); padding:20px;">Network error.</div>`;
  }
}

function closeProjectModal() {
  document.getElementById('projectModal').classList.add('hidden');
}

/* ═══ INITIALIZATION LISTENER ═══ */
document.addEventListener('DOMContentLoaded', () => {
  if (typeof TOKEN !== 'undefined' && TOKEN) {
    loadManagersForProject();
  }
});