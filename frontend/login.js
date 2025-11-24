function showRegister() {
  document.getElementById('registerSection').style.display = 'block';
}

// Función para mostrar configuración de seguridad (opcional)
function showSecuritySetup() {
  const securitySection = document.getElementById('securitySection');
  if (securitySection) {
    securitySection.style.display = securitySection.style.display === 'none' ? 'block' : 'none';
  }
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

      // Guardar configuración de seguridad si se proporcionó
      const authType = document.getElementById('securityAuthType')?.value || 'disabled';

      if (authType === 'symmetric') {
        const masterKey = document.getElementById('securityMasterKey')?.value;
        if (masterKey) {
          localStorage.setItem('securityAuthType', 'symmetric');
          localStorage.setItem('masterKey', masterKey);
        }
      } else if (authType === 'asymmetric') {
        const accessToken = document.getElementById('securityAccessToken')?.value;
        const accessSignature = document.getElementById('securityAccessSignature')?.value;
        if (accessToken && accessSignature) {
          localStorage.setItem('securityAuthType', 'asymmetric');
          localStorage.setItem('accessToken', accessToken);
          localStorage.setItem('accessSignature', accessSignature);
        }
      } else {
        localStorage.setItem('securityAuthType', 'disabled');
      }

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


