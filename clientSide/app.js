BASE_URL = "http://localhost:8080/"

var defaultPasswordButton = document.querySelector("#generateDefaultButton");
var customPasswordButton = document.querySelector("#generateCustomButton");

defaultPasswordButton.onclick = function (){
    var bodyString;
    var username = document.querySelector("#usernameGenerator");
    var password = document.querySelector("#passwordGenerator");
    var website = document.querySelector("#websiteGenerator");
    var counter = document.querySelector("#counterGenerator");

    var usernameText = username.value;
    var passwordText = password.value;
    var websiteText = website.value;
    var counterText = counter.value;

    console.log(username.value);
    
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
        console.log("Server responded from default POST!", response);
        response.json().then(function (data) {
            console.log(data);
            displayData();
        });
    });
}

function displayData(){
    var passwordToUse = document.querySelector("#finalPassword");
    passwordToUse.textContent = data["encryptedPassword"];
    var passwordDiv = document.querySelector("#displayPassword");
    passwordDiv.style.display = "block";
}

customPasswordButton.onclick = function () {
    var bodyString;
    var username = document.querySelector("#usernameGenerator");
    var password = document.querySelector("#passwordGenerator");
    var website = document.querySelector("#websiteGenerator");
    var counter = document.querySelector("#counterGenerator");

    var length = document.querySelector("#length");
    var symbols = document.querySelector("#symbols");

    var uppercase = document.querySelector("#uppercase");
    var lowercase = document.querySelector("#lowercase");
    var numbers = document.querySelector("#numbers");

    var usernameText = username.value;
    var passwordText = password.value;
    var websiteText = website.value;
    var counterText = counter.value;

    var lengthText = length.value;
    var symbolsText = symbols.value;

    var uppercaseBool = uppercase.checked;
    var lowercaseBool = lowercase.checked;
    var numbersBool = numbers.checked;

    console.log(username.value);
    
    bodyString = "username=" + encodeURIComponent(usernameText);
    bodyString += "&password=" + encodeURIComponent(passwordText);
    bodyString += "&website=" + encodeURIComponent(websiteText);
    bodyString += "&counter=" + encodeURIComponent(counterText);
    bodyString += "&length=" + encodeURIComponent(lengthText);
    bodyString += "&symbols=" + encodeURIComponent(symbolsText);
    bodyString += "&uppercase=" + encodeURIComponent(uppercaseBool);
    bodyString += "&lowercase=" + encodeURIComponent(lowercaseBool);
    bodyString += "&numbers=" + encodeURIComponent(numbersBool);

    fetch(BASE_URL + 'customs', {
        //request parameters:
        method: "POST",
        body: bodyString,
        credentials: "include",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function (response){
        //handle the response:
        console.log("Server responded from custom POST!", response);
        //goGetData();
    });
}

function goGetData(){

}
