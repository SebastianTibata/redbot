// en frontend/add_task.js

document.addEventListener('DOMContentLoaded', () => {

    // --- Referencias a todos los elementos ---
    const generateBtn = document.getElementById('generate-ai-task-btn');
    const aiPromptInput = document.getElementById('ai-prompt');
    const addTaskForm = document.getElementById('addTaskForm');
    const addTaskError = document.getElementById('addTaskError');
    
    // Campos del formulario
    const taskTypeSelect = document.getElementById('taskType');
    const configTextarea = document.getElementById('config');
    const accountIdInput = document.getElementById('accountId');
    
    // Campos de Moderación
    const modOptionsDiv = document.getElementById('mod-options');
    const modPostUrl = document.getElementById('mod-post-url');
    const modForbiddenWords = document.getElementById('mod-forbidden-words');
    const modSpamPatterns = document.getElementById('mod-spam-patterns');
    const modCapsPercent = document.getElementById('mod-caps-percent');

    // Token de autenticación
    const token = localStorage.getItem('token');

    // --- 1. Lógica para mostrar/ocultar campos de moderación ---
    if (taskTypeSelect) {
        taskTypeSelect.addEventListener('change', () => {
            if (taskTypeSelect.value === 'moderar') {
                modOptionsDiv.style.display = 'block'; // Mostrar
                configTextarea.style.display = 'none'; // Ocultar
                configTextarea.required = false; // <-- ¡CORRECCIÓN!
            } else {
                modOptionsDiv.style.display = 'none'; // Ocultar
                configTextarea.style.display = 'block'; // Mostrar
                configTextarea.required = true; // <-- ¡CORRECCIÓN!
            }
        });
    }

    // --- 2. Lógica para el botón "Generar tarea" (IA) ---
    if (generateBtn) {
        generateBtn.addEventListener('click', async () => {
            const prompt = aiPromptInput.value;
            if (!prompt) {
                alert('Por favor, describe la tarea en el campo de IA.');
                return;
            }

            generateBtn.textContent = 'Generando...';
            generateBtn.disabled = true;

            try {
                const response = await fetch('/api/tasks/generate-from-prompt', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ prompt: prompt })
                });

                if (!response.ok) {
                    const err = await response.json(); 
                    throw new Error(err.detail || `Error del servidor: ${response.statusText}`);
                }

                const taskData = await response.json(); 
                
                // Rellena el formulario
                taskTypeSelect.value = taskData.task_type;
                
                // Dispara el evento 'change' para mostrar/ocultar los campos correctos
                taskTypeSelect.dispatchEvent(new Event('change'));

                if (taskData.task_type === 'moderar') {
                    // Rellena los campos de moderación
                    const filters = taskData.config.filters || {};
                    modPostUrl.value = taskData.config.post_url || '';
                    modForbiddenWords.value = (filters.forbidden_words || []).join(', ');
                    modSpamPatterns.value = (filters.spam_patterns || []).join(', ');
                    modCapsPercent.value = filters.max_caps_percent || 100;
                } else {
                    // Rellena el JSON normal
                    configTextarea.value = JSON.stringify(taskData.config, null, 2);
                }
                
                accountIdInput.value = "1"; // Ponemos un 'default'
                accountIdInput.focus(); 
                
                alert('¡Tarea generada! Por favor, confirma el "ID de la cuenta" y haz clic en "Crear tarea".');

            } catch (error) {
                console.error('Error al generar tarea con IA:', error);
                addTaskError.textContent = `Error al generar tarea: ${error.message}`;
            } finally {
                generateBtn.textContent = 'Generar tarea';
                generateBtn.disabled = false;
            }
        });
    }

    // --- 3. Lógica para el formulario "Crear tarea" (Submit) ---
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', async function(e) {
            
            e.preventDefault(); 
            
            const type = taskTypeSelect.value;
            const accountId = accountIdInput.value;
            let config;

            try {
                if (type === 'moderar') {
                    // Construye el JSON de moderación desde los campos
                    config = {
                        post_url: modPostUrl.value,
                        action: "remove",
                        filters: {
                            forbidden_words: modForbiddenWords.value.split(',').map(s => s.trim()).filter(Boolean),
                            spam_patterns: modSpamPatterns.value.split(',').map(s => s.trim()).filter(Boolean),
                            max_caps_percent: parseInt(modCapsPercent.value, 10) || 100
                        }
                    };
                    if (!config.post_url) {
                        throw new Error('La URL del post es obligatoria para moderar.');
                    }
                } else {
                    // Lógica antigua para otras tareas
                    config = JSON.parse(configTextarea.value);
                }
            } catch (err) {
                addTaskError.textContent = `Error en la configuración: ${err.message}`;
                return;
            }

            try {
                const res = await fetch('/api/tasks/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ type, account_id: accountId, config_json: config })
                });
                
                if (res.ok) {
                    window.location.href = 'main.html';
                } else {
                    const err = await res.json();
                    addTaskError.textContent = `Error al agregar la tarea: ${err.detail || 'Error desconocido'}`;
                }
            } catch (err) {
                addTaskError.textContent = 'Error de conexión';
            }
        });
    }
});