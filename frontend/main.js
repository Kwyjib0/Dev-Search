let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')
// if logged in only see logout button
if (token) {
    loginBtn.remove();
    // if logged out only see login button
} else {
    logoutBtn.remove();
}
// if logout button is clicked, token is deleted
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    // redirect back to login page
    window.location = 'file:///C:/Users/calin/Desktop/GitHub%20Repos/Django%20Repos/DevSearch/Dev-Search/frontend/login.html'
})
// set url, domain / endpoint to getting projects
let projectsUrl = 'http://127.0.0.1:8000/api/projects/'

let getProjects = () => {
    // fetch api, makes api request to GET data
    fetch(projectsUrl)
        // promise, convert returned json data 
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildProjects(data)
        })

}

// build out projects list
let buildProjects = (projects) => {
    // get html element
    let projectsWrapper = document.getElementById('projects-wrapper')
    // clear projectsWrapper for each iteration so there are no duplicates
    projectsWrapper.innerHTML = '';
    
    for (let i = 0; i < projects.length; i++) {
        let project = projects[i];
        
        let projectCard = `
                <div class="project--card">
                    <img src="http://127.0.0.1:8000${project.featured_image}" />
                    <div>
                        <div class="card--header">
                            <h3>${project.title}</h3>                                            
                            <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                            <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>                            
                        </div>
                        <i>${project.vote_ratio}% Positive feedback </i>
                        <p>${project.description.substring(0, 150)}</p>
                    </div>
                </div>
        `

        projectsWrapper.innerHTML += projectCard
    }
    // add event listeners
    addVoteEvents();

}

// function for adding event listeners to each vote
let addVoteEvents = () => {
    let voteBtns = document.getElementsByClassName('vote--option');

    for (let i = 0; i < voteBtns.length; i++) {
        // listen for click event and run function when voteBtn is clicked
        voteBtns[i].addEventListener('click', (e) => {
            // get token from local storage
            let token = localStorage.getItem('token');
            console.log('token: ', token);

            let vote = e.target.dataset.vote
            let project = e.target.dataset.project

            // fetch api, makes api request to POST data            
            fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ 'value': vote })
            })
            // promise, turns response into json data
            .then(response => response.json())
            .then(data => {
                console.log('Success: ', data);
                getProjects();
            })
        })
    }
}

getProjects();