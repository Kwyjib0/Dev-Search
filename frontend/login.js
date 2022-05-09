let form = document.getElementById('login-form');
// listen for login form submitted
form.addEventListener('submit', (e) => {
    // prevent the default action of the form,
    // keeps page from refreshing so can perform other actions
    e.preventDefault();
    
    
    let formData = {
        'username':form.username.value,
        'password':form.password.value
    }
    // above data sent to url as POST
    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // pass data into body
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('DATA:', data.access)
        // check if got token
        if(data.access) {
            localStorage.setItem('token', data.access)
            // redirect back to projects page
            window.location = 'file:///C:/Users/calin/Desktop/GitHub%20Repos/Django%20Repos/DevSearch/Dev-Search/frontend/projects-list.html'
        } else {
            alert('Username OR password did not work')
        }
    })
})