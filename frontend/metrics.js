// frontend/metrics.js

document.addEventListener('DOMContentLoaded', () => {
    loadMetrics();
});

const token = localStorage.getItem('token');

// Cargar todas las métricas
async function loadMetrics() {
    const errorDiv = document.getElementById('metricsError');
    errorDiv.textContent = '';

    try {
        // Verificar autenticación
        if (!token) {
            window.location.href = 'login.html';
            return;
        }

        // Cargar datos de cuentas y tareas en paralelo
        const [accountsRes, tasksRes] = await Promise.all([
            fetch('/api/accounts', {
                headers: { 'Authorization': `Bearer ${token}` }
            }),
            fetch('/api/tasks/', {
                headers: { 'Authorization': `Bearer ${token}` }
            })
        ]);

        // Verificar autenticación en las respuestas
        if (accountsRes.status === 401 || tasksRes.status === 401) {
            window.location.href = 'login.html';
            return;
        }

        if (!accountsRes.ok || !tasksRes.ok) {
            throw new Error('Error al cargar los datos');
        }

        const accounts = await accountsRes.json();
        const tasks = await tasksRes.json();

        // Actualizar métricas generales
        updateGeneralMetrics(accounts, tasks);

        // Actualizar estadísticas por plataforma
        updatePlatformStats(accounts);

        // Actualizar estadísticas de tareas por tipo
        updateTaskTypeStats(tasks);

        // Calcular y mostrar tasa de éxito
        updateSuccessRate(tasks);

    } catch (err) {
        errorDiv.textContent = `Error: ${err.message}`;
    }
}

// Actualizar métricas generales
function updateGeneralMetrics(accounts, tasks) {
    // Total de cuentas
    document.getElementById('totalAccounts').textContent = accounts.length;

    // Total de tareas
    document.getElementById('totalTasks').textContent = tasks.length;

    // Contar tareas por estado
    const tasksByStatus = tasks.reduce((acc, task) => {
        acc[task.status] = (acc[task.status] || 0) + 1;
        return acc;
    }, {});

    document.getElementById('completedTasks').textContent = tasksByStatus.completed || 0;
    document.getElementById('pendingTasks').textContent = tasksByStatus.pending || 0;
    document.getElementById('inProgressTasks').textContent = tasksByStatus.in_progress || 0;
    document.getElementById('failedTasks').textContent = tasksByStatus.failed || 0;
}

// Actualizar estadísticas por plataforma
function updatePlatformStats(accounts) {
    const platformContainer = document.getElementById('platformStats');

    // Contar cuentas por plataforma
    const platformCounts = accounts.reduce((acc, account) => {
        const platform = account.platform || 'Desconocida';
        acc[platform] = (acc[platform] || 0) + 1;
        return acc;
    }, {});

    // Crear elementos HTML para cada plataforma
    if (Object.keys(platformCounts).length === 0) {
        platformContainer.innerHTML = '<div class="loading">No hay cuentas registradas</div>';
        return;
    }

    platformContainer.innerHTML = '';
    for (const [platform, count] of Object.entries(platformCounts)) {
        const statItem = document.createElement('div');
        statItem.className = 'stat-item';
        statItem.innerHTML = `
            <span class="stat-name">${platform}</span>
            <span class="stat-count">${count}</span>
        `;
        platformContainer.appendChild(statItem);
    }
}

// Actualizar estadísticas de tareas por tipo
function updateTaskTypeStats(tasks) {
    const taskTypeContainer = document.getElementById('taskTypeStats');

    // Contar tareas por tipo
    const typeCounts = tasks.reduce((acc, task) => {
        const type = task.type || 'Sin tipo';
        acc[type] = (acc[type] || 0) + 1;
        return acc;
    }, {});

    // Crear elementos HTML para cada tipo
    if (Object.keys(typeCounts).length === 0) {
        taskTypeContainer.innerHTML = '<div class="loading">No hay tareas registradas</div>';
        return;
    }

    taskTypeContainer.innerHTML = '';
    for (const [type, count] of Object.entries(typeCounts)) {
        const statItem = document.createElement('div');
        statItem.className = 'stat-item';
        statItem.innerHTML = `
            <span class="stat-name">${type}</span>
            <span class="stat-count">${count}</span>
        `;
        taskTypeContainer.appendChild(statItem);
    }
}

// Calcular y mostrar tasa de éxito
function updateSuccessRate(tasks) {
    if (tasks.length === 0) {
        document.getElementById('successPercentage').textContent = '0%';
        document.getElementById('successBar').style.width = '0%';
        return;
    }

    const completedTasks = tasks.filter(task => task.status === 'completed').length;
    const successRate = Math.round((completedTasks / tasks.length) * 100);

    document.getElementById('successPercentage').textContent = `${successRate}%`;
    document.getElementById('successBar').style.width = `${successRate}%`;
}

// Función de logout
function logout() {
    localStorage.removeItem('token');
}
