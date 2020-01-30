BASE_URL = "http://localhost:8080/"

var defaultPasswordButton = document.querySelector("#generateDefaultButton");
var customPasswordButton = document.querySelector("#generateCustomButton");

defaultPasswordButton.onclick = function (){
    var bodyString;
    var username = document.querySelector("#usernameGenerator");
    var password = document.querySelector("#passwordGenerator");
    var website = document.querySelector("#websiteGenerator");
    var counter = document.querySelector("#counterGenerator");

    var usernameText = username.value
    var passwordText = password.value
    var websiteText = website.value
    var counterText = counter.value

    console.log(username.value)
    
    bodyString = "username=" + encodeURIComponent(usernameText);
    bodyString += "&password=" + encodeURIComponent(passwordText);
    bodyString += "&website=" + encodeURIComponent(websiteText);
    bodyString += "&counter=" + encodeURIComponent(counterText);

    fetch(BASE_URL + 'defaults', {
        //request parameters:
        method: "POST",
        body: bodyString,
        credentials: "include",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function (response){
        //handle the response:
        console.log("Server responded from POST!", response);
        //goGetData();
    });
}

customPasswordButton.onclick = function () {

}

function goGetData(){

}
