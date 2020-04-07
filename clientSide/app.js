BASE_URL = "http://localhost:8080/"

var defaultPasswordButton = document.querySelector("#generateDefaultButton");
var customPasswordButton = document.querySelector("#generateCustomButton");
var savedSpecificationsButton = document.querySelector("#getSavedSpecifications");

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
            displayPassword(data);
        });
    });
}

function displayPassword(data){
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
    console.log(bodyString);

    fetch(BASE_URL + 'customs', {
        method: "POST",
        body: bodyString,
        credentials: "include",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }).then(function (response){
        console.log("Server responded from custom POST!", response);
        response.json().then(function (data) {
            console.log(data);
            displayPassword(data);
        });
    });
}

savedSpecificationsButton.onclick = function() {
    fetch(BASE_URL + 'specifications', {
        method: "GET",
        credentials: "include",
        headers:{

        }
    }).then(function (response){
        console.log("Server responded from specifications GET", response);
        response.json().then(function (data) {
            console.log(data);
            displaySpecifications(data);
        });
    })
}

function displaySpecifications(data){
    
    var specsDiv = document.querySelector("#displaySavedSpecifications");
    for (var i = 0; i < data.length; i++){
        var entry = document.createElement("h5");
        entry.innerHTML = "Entry no. " + String(i);
        specsDiv.appendChild(entry);
        
        var username = document.createElement("p");
        username.innerHTML = data[i]["username"];

        var website = document.createElement("p");
        website.innerHTML = data[i]["website"];

        var count = document.createElement("p");
        count.innerHTML = data[i]["count"];

        var length = document.createElement("p");
        length.innerHTML = data[i]["length"];

        var symbols = document.createElement("p");
        symbols.innerHTML = data[i]["symbols"];

        var uppercase = document.createElement("p");
        uppercase.innerHTML = data[i]["uppercase"];

        var lowercase = document.createElement("p");
        lowercase.innerHTML = data[i]["lowercase"];

        var numbers = document.createElement("p");
        numbers.innerHTML = data[i]["numbers"];


        specsDiv.appendChild(username);
        specsDiv.appendChild(website);
        specsDiv.appendChild(count);
        specsDiv.appendChild(length);
        specsDiv.appendChild(symbols);
        specsDiv.appendChild(uppercase);
        specsDiv.appendChild(lowercase);
        specsDiv.appendChild(numbers);
    }
}


