// en frontend/main.js

document.addEventListener('DOMContentLoaded', () => {
    fetchAccounts();
    fetchTasks();
});

const token = localStorage.getItem('token');

// --- Cargar Cuentas ---
async function fetchAccounts() {
    const list = document.getElementById('accounts-list');
    const errorDiv = document.getElementById('accountsError');
    if (!list) return;

    try {
        const res = await fetch('/api/accounts', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.status === 401) {
            window.location.href = 'login.html';
            return;
        }
        if (res.status === 502) {
            errorDiv.textContent = 'Error: 502 Bad Gateway (El servicio de cuentas está caído)';
            return;
        }
        if (!res.ok) {
            throw new Error('Error al cargar las cuentas');
        }

        const accounts = await res.json();
        list.innerHTML = ''; // Limpiar lista
        accounts.forEach(acc => {
            const li = document.createElement('li');
            // Esta parte ya estaba correcta
            li.innerHTML = `
                ID: ${acc.id} - ${acc.handle} (${acc.platform})
                
                <a href="edit_account.html?id=${acc.id}" class="edit-btn">Editar</a>
                
                <button class="delete-btn" data-id="${acc.id}" data-type="account">X</button>
            `;
            list.appendChild(li);
        });
    } catch (err) {
        errorDiv.textContent = err.message;
    }
}

// --- Cargar Tareas ---
async function fetchTasks() {
    const list = document.getElementById('tasks-list');
    const errorDiv = document.getElementById('tasksError');
    if (!list) return;

    try {
        const res = await fetch('/api/tasks/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.status === 401) {
            window.location.href = 'login.html';
            return;
        }
        if (res.status === 502) {
            errorDiv.textContent = 'Error: 502 Bad Gateway (El servicio de tareas está caído)';
            return;
        }
        if (!res.ok) {
            throw new Error('Error al cargar las tareas');
        }
        const tasks = await res.json();
        list.innerHTML = ''; // Limpiar lista
        tasks.forEach(task => {
            const li = document.createElement('li');
            
            // ▼▼▼ BLOQUE CORREGIDO ▼▼▼
            // Añadimos el enlace "Editar" junto al botón "Eliminar"
            li.innerHTML = `
                ${task.type} - ${task.status}
                
                <a href="edit_task.html?id=${task.id}" class="edit-btn">Editar</a>
                
                <button class="delete-btn" data-id="${task.id}" data-type="task">X</button>
            `;
            // ^^^ BLOQUE CORREGIDO ^^^
            
            if (task.status === 'failed') {
                li.style.color = 'red';
            }
            if (task.status === 'completed') {
                li.style.color = 'green';
            }
            list.appendChild(li);
        });
    } catch (err) {
        errorDiv.textContent = err.message;
    }
}

// --- Manejador de Clics para Borrar ---
document.addEventListener('click', function(e) {
    // Revisa si el clic fue en un botón con la clase 'delete-btn'
    if (e.target.classList.contains('delete-btn')) {
        const id = e.target.dataset.id;
        const type = e.target.dataset.type;
        
        if (confirm(`¿Estás seguro de que quieres eliminar ${type} con ID ${id}?`)) {
            handleDeleteClick(id, type);
        }
    }
    // No necesitamos un manejador para 'edit-btn' porque es un enlace <a>
});

async function handleDeleteClick(id, type) {
    let url = '';
    if (type === 'account') {
        url = `/api/accounts/${id}`;
    } else if (type === 'task') {
        url = `/api/tasks/${id}`;
    } else {
        return;
    }

    try {
        const res = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Error al eliminar');
        }

        alert(`${type} eliminado exitosamente.`);
        
        // Recargar las listas
        if (type === 'account') {
            fetchAccounts();
        } else if (type === 'task') {
            fetchTasks();
        }

    } catch (err) {
        alert(`Error: ${err.message}`);
    }
}

// --- Función de Salir (Logout) ---
function logout() {
    localStorage.removeItem('token');
}