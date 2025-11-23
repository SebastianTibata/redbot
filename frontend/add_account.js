document.getElementById('addAccountForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const platform = document.getElementById('platform').value;
  // Corregido: El valor del input se asigna a 'handle' en lugar de 'name'.
  const handle = document.getElementById('accountName').value; 
  const token = document.getElementById('token').value;
  const userToken = localStorage.getItem('token');

  try {
    const res = await fetch('/api/accounts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userToken}`
      },
      // Cuerpo corregido para que coincida con el esquema de Pydantic
      body: JSON.stringify({
        platform: platform,
        handle: handle, // Se envía 'handle' en lugar de 'name'
        token: token,
        user_id: 0      // Se añade user_id con un valor temporal (el backend lo reemplazará)
      })
    });
    if (res.ok) {
      window.location.href = 'main.html';
    } else {
      // Opcional: Mostrar un error más detallado del servidor si está disponible
      const errorData = await res.json();
      document.getElementById('addAccountError').textContent = `Error: ${errorData.detail || 'No se pudo agregar la cuenta'}`;
    }
  } catch (err) {
    document.getElementById('addAccountError').textContent = 'Error de conexión';
  }
});