async function handleLogin(event) {
    event.preventDefault();
    
    const form = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Redirect based on role
            if (data.role === 'jobseeker') {
                window.location.href = '/jobseeker/dashboard';
            } else if (data.role === 'employer') {
                window.location.href = '/employer/dashboard';
            } else {
                window.location.href = '/';
            }
        } else {
            errorMessage.textContent = data.error || 'Login failed';
            errorMessage.classList.remove('d-none');
        }
    } catch (error) {
        errorMessage.textContent = 'An error occurred. Please try again.';
        errorMessage.classList.remove('d-none');
    }
}