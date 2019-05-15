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

chatSocket.onopen = function(e) {
    fetchMessages();
}

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

chatSocket.onclose = function(e) {
    console.error('Why do websockets hate me?');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        sendMessage();
    }
};

$("#chat-message-input").keypress(function(){
    chatSocket.send(JSON.stringify({
        'command': 'typing',
        'from': username,
    }));
});

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

function fetchMessages() {
    chatSocket.send(JSON.stringify({
        'command': 'fetch_messages',
        'room_name': roomName, // TODO (brian): this should be room id
    }));
}

function displayMessage(data){
    if (doWeAppendBoss(data)){
        appendToPrevious(data);
    } else {
        displayNewMessage(data);
    }
}

function doWeAppendBoss(data){
    if (data["author"] == $(".author:last").find("b").html()){
        // check timestamp of last group of messages
        var prev_message_timestamp = $(".message:last").attr("timestamp");
        return (data["timestamp"] - prev_message_timestamp < 600);
    } else {
        return false;
    }
}

function appendToPrevious(data){
    var prev_message = $(".message:last");
    var content = data["content"];
    if (pictureOrNah(content)){
        content = generatePictureHtml(content);
    }
    prev_message.append("<br>" + content);

    // scroll to bottom every time a new message is added to bottom
    var chatLog = document.getElementById("chat-log-v2");
    chatLog.scrollTo(0, chatLog.scrollHeight);
}

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

    document.getElementById("chat-log-v2").appendChild(newChatElement);
    pictureOrNah(data["content"]);

    // scroll to bottom every time a new message is added to bottom
    chatLog.scrollTo(0, chatLog.scrollHeight);
}

/**
* Determines if message content is a picture
*/
function pictureOrNah(content){
    var ext = content.split(".").pop();
    return (["png", "gif", "jpg", "jpeg"].indexOf(content.split(".").pop()) >= 0 &&
        ["http", "https"].indexOf(content.split("://").shift()) >= 0);
}

/**
* generates html for picture messages
*/
function generatePictureHtml(content){
    return "<a href=\"" + content + "\" target=\"_blank\">" + content + "</l>" +
           "<br>" +
           "<img src=\"" + content + "\" target=\"_blank\">";
}
