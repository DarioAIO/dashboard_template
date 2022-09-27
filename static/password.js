async function postData(url = '', data = {}) {
     const response = await fetch(url, {
          method: 'POST',
          mode: 'cors', 
          cache: 'no-cache', 
          credentials: 'same-origin', 
          headers: {
          'Content-Type': 'application/json'
          },
          redirect: 'follow', 
          referrerPolicy: 'no-referrer', 
          body: JSON.stringify(data) 
     });

     return response; 

}

function removeCookie(name) {
     document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

window.onload = function() {
     var email_input = document.getElementById("email_input")
     var password_input = document.getElementById("password_input");
     var password_2_input = document.getElementById("password_input_2");    
     var login_btn = document.getElementById("login_btn");
     var password_btn = document.getElementById("pass_btn");

     const params = new Proxy(new URLSearchParams(window.location.search), {
          get: (searchParams, prop) => searchParams.get(prop),
     });
     
     password_btn.onclick = function() {
          if (password_input.value == password_2_input.value) {
               postData("/api/update_password", {"reset_token": params.code, "user_email": email_input.value, "new_password": password_input.value})
               .then(r =>  r.json().then(data => {
                    if (r.status == 405) {
                         alert("METHOD_NOT_ALLOWED");
                    }
                    else if (r.status == 401) {
                         alert("Password Must Contain 1 Capital And 1 Special Character!")
                    }
                    else if (r.status == 403) {
                         alert("Invalid Email, Try Again!");
                    }
                    else if (r.status == 200) {
                         alert("Password Change Successfully!");
                         removeCookie("user_data")
                         location.replace("/login")
                    }
                    else {
                         alert("Unknown Error, Try Again!");
                    }
               })  
          )}
          else {
               alert("Passwords Do Not Match")
          }
     }

     login_btn.onclick = function() {
          location.replace("/login")
     }

}    