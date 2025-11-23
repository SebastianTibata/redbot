function showRegister() {
  document.getElementById('registerSection').style.display = 'block';
}

document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  try {
  const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      window.location.href = 'main.html';
    } else {
      document.getElementById('loginError').textContent = 'Usuario o contraseña incorrectos';
    }
  } catch (err) {
    document.getElementById('loginError').textContent = 'Error de conexión';
  }
});

document.getElementById('registerForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const username = document.getElementById('regUsername').value;
  const password = document.getElementById('regPassword').value;
  try {
  const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      document.getElementById('registerError').textContent = 'Cuenta creada, ahora puedes iniciar sesión.';
      document.getElementById('registerSection').style.display = 'none';
    } else {
      document.getElementById('registerError').textContent = 'No se pudo crear la cuenta.';
    }
  } catch (err) {
    document.getElementById('registerError').textContent = 'Error de conexión.';
  }
});


