document.addEventListener('DOMContentLoaded', () => {
    // Connect to the websocket
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

    socket.on('connect', () => {
        document.getElementById('send-message-button').onclick = () => {
            sendMessage(socket)
        }
    })

    getData('/channels').then(data => {
        data.forEach(channel => {
            const chann = channelListEntry(channel['creator'], channel['name'])
            document.getElementById('channels-section').appendChild(chann)
            handleRoomMessages(socket, channel['creator'], channel['name'])
        })
    })
    const channelInput = document.getElementById('channel-name')
    const createChannelForm = document.getElementById('create-channel-form')

    channelInput.addEventListener('keydown', () => {
        createChannelForm.classList.remove('was-validated')
        channelInput.classList.remove('is-invalid')
    })

    document.getElementById('create-channel-confirm').onclick = (e) => {
        e.preventDefault()
        const goodString = testString(channelInput.value)
        if (createChannelForm.checkValidity() === false) {
            e.stopPropagation()
            // This has to be added if we want the form to post
            createChannelForm.classList.add('was-validated')
        } else {
            if (!goodString) {
                channelInput.classList.add('is-invalid')
                document.getElementById('modal-feedback')
                    .innerText = "Only alphanumeric characters are allowed. No spaces."
            } else {
                postChannel(channelInput.value).then(data => {
                    console.log(JSON.stringify(data))
                    if (!data['success']) {
                        channelInput.classList.add('is-invalid')
                        document.getElementById('modal-feedback').innerText = data['error']
                    } else {
                        channelInput.value = ""
                        $('#create-channel-modal').modal('hide')
                    }
                })
            }
        }
    }

    socket.on('new channel', (data) => {
        const chann = channelListEntry(data['creator'], data['name'])
        document.getElementById('channels-section').appendChild(chann)
        handleRoomMessages(socket, data['creator'], data['name'])
    })
})

const postChannel = async (channelName) => {
    /* ==============================
    [ For posting data without using a form ] */
    const response = await fetch("/api/create_channel", {
        method: "POST",
        body: JSON.stringify({'name': channelName}),
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    return response.json()
}

const testString = channelName => {
    const format = /^[a-zA-Z0-9]*$/
    return format.test(channelName)
}

const getData = async (route) => {
    /* ==============================
    [ Fetch channels as soon as the home page is displayed ] */
    const response = await fetch(`/api/${route}`)
    return response.json()
}

const channelListEntry = (creator, name) => {
    const channelEntry = document.createElement('a')
    channelEntry.classList.add('list-group-item', 'list-group-item-action')
    channelEntry.dataset.toggle = 'list'
    channelEntry.innerText = `${creator}/${name}`
    channelEntry.id = `${creator}-${name}-channel`
    channelEntry.href = `#${creator}-${name}`
    addChannelRoomPane(creator, name)
    return channelEntry
}

const addChannelRoomPane = (creator, name) => {
    /* ==============================
    [ Create the corresponding room for the channel ] */
    const channelRoom = document.createElement('div')
    channelRoom.classList.add('tab-pane', 'fade')
    channelRoom.id = `${creator}-${name}`
    channelRoom.role = 'tabpanel'
    channelRoom.innerText = `welcome to ${channelRoom.id}`
    channelRoom.setAttribute('aria-labelledby', `list-${creator}-${name}-list`)
    document.getElementById('messages-section').appendChild(channelRoom)
    populateMessages(channelRoom.id)
}

const handleRoomMessages = (socket, creator, name) => {
    const channelRoom = document.getElementById(`${creator}-${name}`)
    socket.on(`${creator}-${name}-channel`, (data) => {
        const newMessage = formatMessage(data)
        channelRoom.appendChild(newMessage)
    })
}

const sendMessage = (socket) => {
    const channelName = document.querySelector('.active')
    const message = document.getElementById('message-box').value
    const messageDetails = {
        'channelName': channelName.id,
        'message': message
    }
    socket.emit('handle messages', messageDetails)
}

const populateMessages = room => {
    const roomDiv = document.getElementById(room)
    getData(`/room_messages/${room}`).then(data => {
        data.forEach(message => {
            const entry = formatMessage(message)
            roomDiv.appendChild(entry)
        })
    })
}

const formatMessage = (message) => {
    const messageDiv = document.createElement('div')
    messageDiv.innerText = `${message['author']} said: ${message['message']}`
    const username = document.getElementById('username').innerText
    if (message['author'] === username) {
        messageDiv.classList.add('author-message')
    }
    messageDiv.classList.add('list-group-item')
    return messageDiv
}