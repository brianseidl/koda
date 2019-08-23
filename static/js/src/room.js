/* This contains logic of connecting to the chat room via websockets */
var clearInterval = 900; //0.9s
var clearTimerId;
var typingUsers = [];
var hostname = window.location.origin;
var bell = document.getElementById('not-discord-bell');

if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
} else {
    var ws_scheme = "ws://";
}

var chatSocket = new ReconnectingWebSocket(
    ws_scheme + window.location.host +
    '/ws/room/' + room_id + '/');

/**
Fetch all previous messages on the chat when the websocket opens.

Precondition:
    Websocket connect to server.

Postcondition:
    Calls function fetchMessages.
*/
chatSocket.onopen = function(e) {
    fetchMessages();
}

/**
Websocket recieves an event from the server
 
Precondition:
    Server sends data to the client

Postcondition:
    The data is handled and process according to the correct command
*/
chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    if (data['command'] === 'messages') {
        for (let i=0; i<data['messages'].length; i++) {
            displayMessage(data['messages'][i]);
        }
    } else if (data['command'] === 'new_message'){
        displayMessage(data['message']);
        if (data["message"]["author"] != username){
            bell.play();
        }
    } else if (data['command'] === 'typing'){
        displayTyping(data['username']);
    }
};

/**
Websocket connection closed :(
*/
chatSocket.onclose = function(e) {
    console.error('Why do websockets hate me?');
};

/**
event lister for when user sends message
*/
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        sendMessage();
    }
};

/**
JQuery to listen to keypress for input

Precondition:
    User starts to type.

Postcondition:
    Client sends typing event to the server.
*/
$("#chat-message-input").keypress(function(){
    chatSocket.send(JSON.stringify({
        'command': 'typing',
        'from': username,
    }));
});

/**
display gif and message showing who is typing

Precondition:
    Message handler event calls displayTyping

Postcondition:
    Gif and message are displayed below the input bar
*/
function displayTyping(typerName){
    if (typerName != username){
        if (typingUsers.indexOf(typerName) >= 0){
            // typerName is in typing users
        } else {
            // typerName is not in typing users
            // add typerName to typing users
            typingUsers.push(typerName);
        }

        if (typingUsers.length > 1){
            $("#typing").html("<img src=\"" + hostname + "/static/images/dots.gif\" style=\"padding-right:5px\">multiple people are typing");
        } else {
            $("#typing").html("<img src=\"" + hostname + "/static/images/dots.gif\" style=\"padding-right:5px\">" + typerName + " is typing");
        }

        // restart timeout timer
        clearTimeout(clearTimerId);
        clearTimerId = setTimeout(function (){
            // clear user is typing message
            $("#typing").html("");
            typingUsers.pop(typerName);
        }, clearInterval);
    }
}

/**
Sends users message to the server.

Precondition:
    function called by input listener

Postcondition:
    new message is sent to the server
*/
function sendMessage() {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    if (message != "") {
        chatSocket.send(JSON.stringify({
            'message': message,
            'command': 'new_message',
            'from': username,
            'room_name': roomName
        }));
        messageInputDom.value = '';
    }
};

/**
Send request to server to request all messages.

Precondition:
    Helper function called by chatSocket.onopen

Postcondition:
    Actually sends request to server.
*/
function fetchMessages() {
    chatSocket.send(JSON.stringify({
        'command': 'fetch_messages',
        'room_name': roomName, // TODO (brian): this should be room id
    }));
}

/**
Helper function called by event handler.
Determine which type of display should be used
and calls that function.

Precondition:
    Function called by event handler.

Postcondition:
    Calls correct display function.
*/
function displayMessage(data){
    if (doWeAppendBoss(data)){
        appendToPrevious(data);
    } else {
        displayNewMessage(data);
    }
}

/**
Helper function called by displayMessage.

Precondition:
    Function called by displayMessage.

Postcondition:
    determines if the message should be appended
    or displayed as a new message.
*/
function doWeAppendBoss(data){
    if (data["author"] == $(".author:last").find("b").html()){
        // check timestamp of last group of messages
        var prev_message_timestamp = $(".message:last").attr("timestamp");
        return (data["timestamp"] - prev_message_timestamp < 600);
    } else {
        return false;
    }
}

/**
Appends new message to previous message

Precondition:
    Called by displayMessage.

Poscondition:
    New message is displayed to the previous message.
*/
function appendToPrevious(data){
    var prev_message = $(".message:last");
    var content = data["content"];
    if (pictureOrNah(content)){
        content = generatePictureHtml(content);
    }
    prev_message.append("<br>" + content);

    // scroll to bottom every time a new message is added to bottom
    var chatLog = document.getElementById("chat-log-v2");
    chatLog.scrollTo(0, chatLog.scrollHeight)
    // scroll to bottom every time a new message is added to bottom
    $('#chat-log-v2').imagesLoaded(function() {
        var chatLog = document.getElementById("chat-log-v2");
        chatLog.scrollTo(0, chatLog.scrollHeight);
    });
}

/**
Displays a message as a new message.

Precondition:
    Called by displayMessage.

Postcondition:
    Message is displayed as a new message.
*/
function displayNewMessage(data) {
    var content = data["content"];
    if (pictureOrNah(content)){
        content = generatePictureHtml(content);
    }
    var chatLog = document.getElementById("chat-log-v2");
    var newChatElement = document.createElement("div");
    newChatElement.setAttribute("class", "whole-message");
    newChatElement.innerHTML = "<div class=\"w3-show-inline-block author\"><b>" + data["author"] + "</b></div>" +
        "<div class=\"w3-container w3-show-inline-block w3-text-dark-gray time\">" + data["time"] + "</div>" +
        "<div class=\"w3-container w3-leftbar message\" timestamp=\"" + data["timestamp"] + "\">" + content + "</div>";

    chatLog.appendChild(newChatElement);
    pictureOrNah(data["content"]);

    // scroll to bottom every time a new message is added to bottom
    $('#chat-log-v2').imagesLoaded(function() {
        var chatLog = document.getElementById("chat-log-v2");
        chatLog.scrollTo(0, chatLog.scrollHeight);
    });
}

/**
Determines if message content is a picture.

Precontition:
    Message is in process of being displayed.

Postcondition:
    Return true if is photo, else false.
*/
function pictureOrNah(content){
    var ext = content.split(".").pop();
    return (["png", "gif", "jpg", "jpeg"].indexOf(content.split(".").pop()) >= 0 &&
        ["http", "https"].indexOf(content.split("://").shift()) >= 0);
}

/**
Generates html for picture messages.

Precondition:
    Message is confirmed a photo.

Postcondition:
    Photo htnml template is returned.
*/
function generatePictureHtml(content){
    return "<a href=\"" + content + "\" target=\"_blank\">" + content + "</l>" +
           "<br>" +
           "<img class=\"chat-photo\" src=\"" + content + "\" target=\"_blank\">";
}
