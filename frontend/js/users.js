/* ═══ LOAD USERS LIST FOR ADMIN ═══ */
async function loadUsersList() {
    if (CURRENT_USER_ROLE !== 'admin') return;

    try {
        const res = await fetch(`${API_URL}/auth/users`, { headers: { 'Authorization': `Bearer ${TOKEN}` } });
        if (res.ok) {
            const users = await res.json();
            const list = document.getElementById('usersList');

            if(!users.length){
                list.innerHTML='<div class="empty-state"><i class="fa-solid fa-users-slash"></i><p>No users found</p></div>';
                return;
            }

            list.innerHTML = users.map((u, i) => {
                const isActive = u.is_active !== false;
                const statusBadge = isActive ?
                    `<span class="badge bl" style="font-size:9px;">Active</span>` :
                    `<span class="badge bh" style="font-size:9px;">Inactive</span>`;

                const toggleBtn = isActive ?
                    `<button onclick="toggleUserStatus(${u.id}, false)" class="btn-i delete-btn" title="Deactivate Account" style="background:rgba(240,75,93,.1); ${u.email === CURRENT_USER_EMAIL ? 'display:none' : ''}"><i class="fa-solid fa-user-slash" style="font-size:12px"></i></button>` :
                    `<button onclick="toggleUserStatus(${u.id}, true)" class="btn-i delete-btn" title="Activate Account" style="background:rgba(34,212,126,.1); color:var(--green); border-color:rgba(34,212,126,.2);"><i class="fa-solid fa-user-check" style="font-size:12px"></i></button>`;

                return `
                <div class="proj-item" style="animation-delay:${i * 0.05}s; opacity: ${isActive ? '1' : '0.6'};">
                    <div class="uc-avatar" style="${isActive ? '' : 'filter:grayscale(1);'}">${u.full_name.charAt(0).toUpperCase()}</div>
                    <div style="flex:1;min-width:0">
                        <div class="proj-name">${u.full_name} ${statusBadge}</div>
                        <div class="proj-sub">${u.email} &mdash; ID: ${u.id}</div>
                    </div>
                    
                    <button onclick="viewUserDetails(${u.id}, '${u.full_name}')" class="btn-i" title="View Details" style="background:transparent; border-color:var(--line2); color:var(--a);">
                        <i class="fa-solid fa-eye" style="font-size:12px"></i>
                    </button>

                    <select onchange="changeUserRole(${u.id}, this.value)" class="ssel" style="width:125px; ${u.email === CURRENT_USER_EMAIL || !isActive ? 'display:none' : ''}">
                        <option value="employee" ${u.role === 'employee' ? 'selected' : ''}>Employee</option>
                        <option value="project_manager" ${u.role === 'project_manager' ? 'selected' : ''}>Proj. Manager</option>
                        <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>Admin</option>
                    </select>
                    
                    ${toggleBtn}
                </div>`;
            }).join('');
        }
    } catch (e) {
        console.error("Failed to load users list", e);
    }
}

/* ═══ CHANGE USER ROLE ═══ */
function changeUserRole(userId, newRole) {
    customConfirm(`Change this user's role to ${newRole.toUpperCase()}?`, async () => {
        loadStart();
        const res = await fetch(`${API_URL}/auth/users/${userId}/role`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${TOKEN}` },
            body: JSON.stringify({ role: newRole })
        });
        loadDone();

        if (res.ok) {
            toast('User role updated successfully');
            loadUsersList();
            loadUsersForTaskAssignment();
            if(typeof loadManagersForProject === 'function') loadManagersForProject();
        } else {
            toast('Failed to update role', 'error');
            loadUsersList();
        }
    }, 'btn-p', 'Change Role');
}

/* ═══ TOGGLE USER STATUS (SOFT DELETE) ═══ */
function toggleUserStatus(userId, activate) {
    const actionText = activate ? "activate" : "deactivate";
    const warning = activate ? "They will regain access to the system." : "They will be locked out but their tasks will remain intact.";

    customConfirm(`Are you sure you want to ${actionText} this user? ${warning}`, async () => {
        loadStart();
        const method = activate ? 'PUT' : 'DELETE';
        const endpoint = activate ? `${API_URL}/auth/users/${userId}/activate` : `${API_URL}/auth/users/${userId}`;

        const res = await fetch(endpoint, {
            method: method,
            headers: { 'Authorization': `Bearer ${TOKEN}` }
        });
        loadDone();

        if (res.ok) {
            toast(`User ${actionText}d successfully`);
            loadUsersList();
            loadUsersForTaskAssignment();
            if(typeof loadManagersForProject === 'function') loadManagersForProject();
        } else {
            toast(`Failed to ${actionText} user`, 'error');
        }
    }, activate ? 'btn-p' : 'btn-d', activate ? 'Activate User' : 'Deactivate User');
}

/* ═══ VIEW USER DETAILS MODAL ═══ */
async function viewUserDetails(id, name) {
  document.getElementById('udTitle').innerText = name + " - Profile";
  const content = document.getElementById('udContent');

  content.innerHTML = `<div style="text-align:center; padding:20px;"><i class="fa-solid fa-circle-notch fa-spin"></i> Loading user history...</div>`;
  document.getElementById('userDetailsModal').classList.remove('hidden');

  try {
    const res = await fetch(`${API_URL}/auth/users/${id}/details`, {headers:{'Authorization':`Bearer ${TOKEN}`}});
    if(res.ok) {
        const data = await res.json();

        const projects = data.managed_projects || [];
        const tasks = data.assigned_tasks || [];

        const projHtml = projects.length ? projects.map(p => `<span class="badge bl" style="margin:2px;">#${p.id} ${p.name}</span>`).join('') : '<span style="color:var(--t2); font-size:12px;">No projects managed</span>';

        let tasksHtml = tasks.length ? tasks.map(t => `
        <div style="display:flex; justify-content:space-between; padding:8px 12px; background:var(--ink3); border:1px solid var(--line2); border-radius:6px; margin-bottom:6px;">
          <span style="font-size:12px; color:var(--t0);">${t.title}</span>
          <span class="badge ${t.status === 'Done' ? 'bl' : 'bm'}" style="font-size:9px;">${t.status}</span>
        </div>
        `).join('') : '<span style="color:var(--t2); font-size:12px;">No assigned tasks</span>';

        content.innerHTML = `
        <div style="margin-bottom:16px;">
          <div style="font-size:11px; color:var(--t2); margin-bottom:4px; text-transform:uppercase;">Contact Info</div>
          <div style="font-size:13px; color:var(--t0);">${data.email}</div>
        </div>
        <div style="margin-bottom:16px;">
          <div style="font-size:11px; color:var(--t2); margin-bottom:8px; text-transform:uppercase;">Managed Projects (${projects.length})</div>
          <div>${projHtml}</div>
        </div>
        <div>
          <div style="font-size:11px; color:var(--t2); margin-bottom:8px; text-transform:uppercase;">Assigned Tasks (${tasks.length})</div>
          <div style="max-height:180px; overflow-y:auto; padding-right:4px;">${tasksHtml}</div>
        </div>
      `;
    } else {
        content.innerHTML = `<div style="text-align:center; color:var(--red); padding:20px;">Failed to fetch details.</div>`;
    }
  } catch(e) {
    content.innerHTML = `<div style="text-align:center; color:var(--red); padding:20px;">Network error.</div>`;
  }
}

function closeUserDetailsModal() {
  document.getElementById('userDetailsModal').classList.add('hidden');
}