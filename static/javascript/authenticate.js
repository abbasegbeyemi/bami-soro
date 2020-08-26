document.addEventListener('DOMContentLoaded', () => {
    /* ==============================
    [ On init we load the sign in form ] */
    loadForm('login', 'Sign In')
})

window.onpopstate = e => {
    const data = e.state
    clearForm(data.formTitle)
    activateForm(data.text, data.formType)
}

const loadForm = (type, title) => {
    /* ==============================
    [ Load a form depending on the type of form provided, and the title of the form ] */
    clearForm(title)    // Clear the from and put the right title in

    /* ==============================
    [ Get the required form from the server ] */
    getForm(type).then(data => {
        activateForm(data, type)    // With the form html gotten, i.e no error, we activate the form
        // Push info about the form to the browser state
        history.pushState({'text': data, 'formTitle': title, 'formType': type}, title, type)
    })
}

const activateForm = (data, type) => {
    /* ==============================
    [ This is where we activate the form. First we put it in its container ] */
    const formContainer = document.getElementById('form-container')
    formContainer.innerHTML = data
    // Then we activate the alternative links
    alternativeLinks(type)
    // We then add the event listener to the form we just received
    const form = document.getElementById('form')
    form.addEventListener('submit', (e) => submitEvent(e, form, type))
}

const alternativeLinks = (type) => {
    /* ==============================
    [ Define the alternative link depending on the type of form ] */
    type === 'login' ? document.getElementById('alternative').onclick = () => {
            loadForm('register', 'Register')
            return false
        } :
        document.getElementById('alternative').onclick = () => {
            loadForm('login', 'Sign In')
            return false
        }
}

const clearForm = (title) => {
    /* ==============================
    [ Clear error list and put a proper title on the form ] */
    document.getElementById(`error-list`).innerHTML = ""
    document.getElementById('form-title').innerText = title
    document.title = `bamisoro - ${title}`
}

const submitEvent = (e, form, type) => {
    /* ==============================
    [ The event that is fired when the submit button is clicked on the form. Post the forn data ] */
    e.preventDefault()
    // We clear the error list
    document.getElementById(`error-list`).innerHTML = ""
    // Prevent form from even doing anything if all the fields have not been filled
    if (form.checkValidity() === false) {
        e.stopPropagation()
    } else {
        // Post the form if all the fields have been filled
        postForm(type, form).then(data => {
            // Server returns false for success if there are errors after server validation
            if (!data.success) {
                Object.keys(data['errors']).forEach((key) => {
                    const errorList = document.getElementById(`error-list`)
                    errorList.innerHTML += `<li>${data['errors'][key][0]}</li>`
                })
            }
            else if (data.success) {
                window.location.href = data['nextpage']
            }
        })
    }
    // This has to be added if we want the form to post
    form.classList.add('was-validated')
}

const getForm = async (type) => {
    /* ==============================
    [ The get request to get the form everytime we want to load ] */
    const response = await fetch(`/api/${type}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'text/html'
            }
        })
    return response.text()
}

const postForm = async (type, form) => {
    /* ==============================
    [ Initialise the form properly for postage and get the JSON response ] */
    const response = await fetch(`/api/${type}`,
        {
            method: 'POST',
            body: new URLSearchParams(new FormData(form))
        })
    return response.json()
}
