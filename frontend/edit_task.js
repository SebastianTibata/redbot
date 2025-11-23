// en frontend/edit_task.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const form = document.getElementById('editTaskForm');
    const errorDiv = document.getElementById('editError');
    
    // Referencias a los campos del formulario
    const taskTypeSelect = document.getElementById('taskType');
    const accountIdInput = document.getElementById('accountId');
    const configTextarea = document.getElementById('config');

    // 1. Obtener el ID de la tarea desde la URL
    const params = new URLSearchParams(window.location.search);
    const taskId = params.get('id');

    if (!taskId) {
        errorDiv.textContent = "Error: No se proporcionó un ID de tarea.";
        return;
    }

    // 2. Rellenar el formulario con datos existentes
    async function fetchTaskData() {
        try {
            const res = await fetch(`/api/tasks/${taskId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) {
                if(res.status === 401) window.location.href = 'login.html';
                throw new Error('No se pudieron cargar los datos de la tarea.');
            }
            const task = await res.json();
            
            // 3. Rellenar los campos
            taskTypeSelect.value = task.type;
            accountIdInput.value = task.account_id;
            configTextarea.value = JSON.stringify(task.config_json, null, 2); // Formatea el JSON
            
        } catch (err) {
            errorDiv.textContent = err.message;
        }
    }
    
    fetchTaskData(); // Llama a la función al cargar la página

    // 4. Manejar el envío del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        let config;
        try {
            config = JSON.parse(configTextarea.value);
        } catch {
            errorDiv.textContent = 'Configuración JSON inválida';
            return;
        }

        try {
            const res = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ 
                    type: taskTypeSelect.value, 
                    config_json: config 
                    // No enviamos account_id porque no permitimos cambiarlo
                })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Error al guardar los cambios.');
            }
            
            alert('¡Tarea actualizada con éxito!');
            window.location.href = 'main.html';

        } catch (err) {
            errorDiv.textContent = err.message;
        }
    });
});