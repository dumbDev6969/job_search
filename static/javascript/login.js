async function handleLogin(event) {
    event.preventDefault();
    
    const form = document.getElementById('loginForm');
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

        // Check if response is a redirect
        if (response.redirected) {
            window.location.href = response.url;
            return;
        }
        
        // Try to parse JSON response
        let data;
        try {
            data = await response.json();
        } catch (e) {
            // If response is not JSON, might be a redirect or other response
            if (response.ok) {
                window.location.reload();
                return;
            }
            throw new Error('Invalid response format');
        }
    
        if (response.ok) {
            // Redirect based on role
            if (data.role === 'jobseeker') {
                window.location.href = '/jobseeker/find-jobs';
            } else if (data.role === 'employer') {
                window.location.href = '/employer/dashboard';
            } else {
              if (data.error){
                  Swal.fire({
                      icon: 'error',
                      title: 'Login Failed',
                      text: data.error || 'Invalid credentials',
                      confirmButtonColor: '#3085d6'
                  });}
              
            }
        } else {
            // Handle error responses including 401
            Swal.fire({
                icon: 'error',
                title: 'Login Failed',
                text: data.error || 'Invalid credentials',
                confirmButtonColor: '#3085d6'
            });
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'An error occurred. Please try again.',
            confirmButtonColor: '#3085d6'
        });
    }
}