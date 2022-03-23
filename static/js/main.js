
    // get profiles and projects search forms and page links
    let searchForm = document.getElementById('searchForm')
    let pageLinks = document.getElementsByClassName('page-link')

    //ensure search form exists
    if(searchForm) {
        for (let i = 0; i < pageLinks.length; i++) {
            pageLinks[i].addEventListener('click', function(e) {
                // stops default action from occurring when
                e.preventDefault();
                // get the data attribute, this = button clicked on
                let page = this.dataset.page;
                console.log('PAGE: ' + page);
                // add hidden search input to form, add html content/add in another input field to <form>
                searchForm.innerHTML += `<input value=${page} name="page" hidden/>`;
                // submit form
                searchForm.submit();
                });
        }
    }