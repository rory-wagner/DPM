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

    console.log(uppercaseBool);
    console.log(lowercaseBool);
    console.log(numbersBool);
    
    bodyString = "username=" + encodeURIComponent(usernameText);
    bodyString += "&password=" + encodeURIComponent(passwordText);
    bodyString += "&website=" + encodeURIComponent(websiteText);
    bodyString += "&counter=" + encodeURIComponent(counterText);
    
    //allow for empty length and symbol fields
    if (encodeURIComponent(lengthText) == "") {
        bodyString += "&length=default";
    }
    else{
        bodyString += "&length=" + encodeURIComponent(lengthText);
    }
    if (encodeURIComponent(symbolsText) == "") {
        bodyString += "&symbols=default";
    }
    else {
        bodyString += "&symbols=" + encodeURIComponent(symbolsText);
    }
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
    
    var specsDiv = document.querySelector("#specsDisplayDiv");
    specsDiv.innerHTML = "";
    for (var i = 0; i < data.length; i++){
        var entry = document.createElement("h5");
        entry.innerHTML = "Entry no. " + String(i + 1);
        specsDiv.appendChild(entry);
        
        var username = document.createElement("p");
        username.innerHTML = "Username: " + data[i]["username"];

        var website = document.createElement("p");
        website.innerHTML = "Website: " + data[i]["website"];

        var count = document.createElement("p");
        count.innerHTML = "Count: " + data[i]["count"];

        var length = document.createElement("p");
        if (data[i]["length"] == -1){
            length.innerHTML = "Length: " + "N/A";
        }
        else{
            length.innerHTML = "Length: " + String(data[i]["length"]);
        }

        var symbols = document.createElement("p");
        if (data[i]["symbols"] == ""){
            symbols.innerHTML = "Symbols: " + "N/A";
        }
        else{
            symbols.innerHTML = "Symbols: " + data[i]["symbols"];
        }

        var uppercase = document.createElement("p");
        if (data[i]["uppercase"] == 1){
            uppercase.innerHTML = "Uppercase: True";
        }
        else {
            uppercase.innerHTML = "Uppercase: False";
        }
        

        var lowercase = document.createElement("p");
        if (data[i]["lowercase"] == 1){
            lowercase.innerHTML = "Lowercase: True";
        }
        else {
            lowercase.innerHTML = "Lowercase: False";
        }

        var numbers = document.createElement("p");
        if (data[i]["numbers"] == 1){
            numbers.innerHTML = "Numbers: True";
        }
        else {
            numbers.innerHTML = "Numbers: False";
        }


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


