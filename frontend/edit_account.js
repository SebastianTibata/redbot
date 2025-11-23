// en frontend/edit_account.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const form = document.getElementById('editAccountForm');
    const errorDiv = document.getElementById('editError');
    
    // 1. Obtener el ID de la cuenta desde la URL
    const params = new URLSearchParams(window.location.search);
    const accountId = params.get('id');

    if (!accountId) {
        errorDiv.textContent = "Error: No se proporcionó un ID de cuenta.";
        return;
    }

    // 2. Rellenar el formulario con datos existentes
    async function fetchAccountData() {
        try {
            const res = await fetch(`/api/accounts/${accountId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) {
                if(res.status === 401) window.location.href = 'login.html';
                throw new Error('No se pudieron cargar los datos de la cuenta.');
            }
            const account = await res.json();
            
            // 3. Rellenar los campos
            document.getElementById('handle').value = account.handle;
            document.getElementById('token').value = account.token;
            
        } catch (err) {
            errorDiv.textContent = err.message;
        }
    }
    
    fetchAccountData(); // Llama a la función al cargar la página

    // 4. Manejar el envío del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const handle = document.getElementById('handle').value;
        const tokenValue = document.getElementById('token').value;

        try {
            const res = await fetch(`/api/accounts/${accountId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ handle, token: tokenValue })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Error al guardar los cambios.');
            }
            
            alert('¡Cuenta actualizada con éxito!');
            window.location.href = 'main.html';

        } catch (err) {
            errorDiv.textContent = err.message;
        }
    });
});