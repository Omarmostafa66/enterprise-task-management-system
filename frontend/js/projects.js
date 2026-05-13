/* ═══ LOAD PROJECTS ═══ */
async function loadProjects() {

  try {

    const res = await fetch(
      `${API_URL}/projects/`,
      {
        headers: {
          'Authorization': `Bearer ${TOKEN}`
        }
      }
    );

    const projects = await res.json();

    bump('projCount', projects.length);

    const list =
      document.getElementById('projectList');

    /* Populate the Projects Dropdown in Deploy Task Panel */
    if (CURRENT_USER_ROLE !== 'employee') {

      const taskProjSel =
        document.getElementById('taskProjId');

      if (taskProjSel) {

        taskProjSel.innerHTML =
          '<option value="">Select Project</option>' +

          projects.map(
            p => `
              <option value="${p.id}">
                ${p.name}
              </option>
            `
          ).join('');
      }
    }

    if (res.ok) {

      if (!projects.length) {

        list.innerHTML =
          '<div class="empty-state"><i class="fa-solid fa-folder-open"></i><p>No projects yet</p></div>';

        return;
      }

      list.innerHTML = projects.map((p, i) => {

        const dueDate =
          p.due_date
            ? new Date(p.due_date).toLocaleDateString()
            : 'No Deadline';

        const priorityClass = {
          Low:'bl',
          Medium:'bm',
          High:'bh',
          Critical:'bh'
        };

        const statusClass = {
          Planning:'bm',
          Active:'bl',
          'On Hold':'bm',
          Completed:'bl',
          Cancelled:'bh'
        };

        return `

        <div
          class="proj-item"
          style="
            animation-delay:${i * .05}s;
            cursor:pointer;
          "
          onclick="viewProject(${p.id}, '${p.name}')"
        >

          <div class="proj-num">
            #${p.id}
          </div>

          <div style="flex:1;min-width:0">

            <div
              style="
                display:flex;
                align-items:center;
                gap:8px;
                flex-wrap:wrap;
                margin-bottom:4px;
              "
            >

              <div class="proj-name">
                ${p.name}
              </div>

              <span class="badge ${priorityClass[p.priority] || 'bm'}">
                ${p.priority}
              </span>

              <span class="badge ${statusClass[p.status] || 'bm'}">
                ${p.status}
              </span>

            </div>

            <div class="proj-sub">

              Project ID ${p.id}

              •

              Due:
              ${dueDate}

            </div>

          </div>

          <i
            class="fa-solid fa-chevron-right"
            style="
              color:var(--t3);
              font-size:10px;
              flex-shrink:0
            "
          ></i>

        </div>

      `;
      }).join('');
    }

  } catch (e) {

    console.error(e);
  }
}

/* ═══ LOAD PROJECT MANAGERS ONLY ═══ */
async function loadManagersForProject() {

  if (CURRENT_USER_ROLE === 'employee') return;

  try {

    const res = await fetch(
      `${API_URL}/auth/users`,
      {
        headers: {
          'Authorization': `Bearer ${TOKEN}`
        }
      }
    );

    if (res.ok) {

      const users = await res.json();

      const sel =
        document.getElementById('projManager');

      if (sel) {

        /*
          Only Project Managers are allowed
          to manage projects
        */
        const managers = users.filter(
          u =>
            u.role === 'project_manager' &&
            u.is_active !== false
        );

        sel.innerHTML =
          '<option value="">Select Project Manager</option>' +

          managers.map(
            u => `
              <option value="${u.id}">
                ${u.full_name}
              </option>
            `
          ).join('');

        /*
          Empty state if no Project Managers exist
        */
        if (!managers.length) {

          sel.innerHTML = `
            <option value="">
              No Project Managers Available
            </option>
          `;
        }
      }
    }

  } catch (e) {

    console.error(
      "Error fetching project managers"
    );
  }
}

/* ═══ CREATE PROJECT ═══ */
async function createProject() {

  const name =
    document.getElementById('projName')
      .value
      .trim();

  const desc =
    document.getElementById('projDesc')
      .value
      .trim() ||
      "No description provided";

  const managerId =
    document.getElementById('projManager')
      .value;

  const status =
    document.getElementById('projStatus').value;

  const priority =
    document.getElementById('projPriority').value;

  const dueDate =
    document.getElementById('projDueDate').value;

  if (!name) {

    flashErr('projName');

    return;
  }

  if (!managerId) {

    flashErr('projManager');

    toast(
      'Please assign a project manager',
      'error'
    );

    return;
  }

  loadStart();

  try {

    const payload = {
      name,
      description: desc,
      manager_id: parseInt(managerId),
      status,
      priority,
      due_date: dueDate || null
    };

    const res = await fetch(
      `${API_URL}/projects/`,
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${TOKEN}`
        },

        body: JSON.stringify(payload)
      }
    );

    loadDone();

    if (res.ok) {

      document.getElementById('projName').value = '';

      document.getElementById('projDesc').value = '';

      document.getElementById('projManager').value = '';

      document.getElementById('projStatus').value =
        'Planning';

      document.getElementById('projPriority').value =
        'Medium';

      document.getElementById('projDueDate').value = '';

      /*
        Reload projects to update:
        - Projects list
        - Task deployment dropdown
      */
      loadProjects();

      toast(
        'Project created successfully'
      );

    } else {

      const err = await res.json();

      toast(
        err.detail || 'Project creation failed',
        'error'
      );
    }

  } catch (e) {

    loadDone();

    toast(
      'Server connection failed',
      'error'
    );
  }
}