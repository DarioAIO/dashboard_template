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

window.onload = function() {
     var email_input = document.getElementById("email_input");
     var password_input = document.getElementById("password_input");
     var invite_code_input = document.getElementById("invitecode_input");
     var register_button = document.getElementById("register_btn");
     var login_btn = document.getElementById("login_btn")

     register_button.onclick = function() {
          postData("/api/register", {"user_email": email_input.value, "user_password": password_input.value, "user_invite_code": invite_code_input.value})
          .then(function (res) {
               if (res.status == 403) {
                    alert("Invalid Email, Try Again!");
               } 
               if (res.status == 401) {
                    alert("Password Must Contain 1 Capital And 1 Special Character!")
               }
               if (res.status == 400) {
                    alert("Email already registered, Try Again!");
               }
               if (res.status == 404) {
                    alert("Invalid Invite Code, Try Again!");
               }
               if (res.status == 500) {
                    alert("Internal Server Error, Try Again!");
               }
               else if (res.status == 200) {
                    alert("Registration Successful!");
                    window.location.replace("/login");

               }
          }
     )}

     login_btn.onclick = function() {
          location.replace("/login")
     }
}     