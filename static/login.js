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

function checkUppercase(str){
     for (var i=0; i<str.length; i++){
       if (str.charAt(i) == str.charAt(i).toUpperCase() && str.charAt(i).match(/[a-z]/i)){
         return true;
       }
     }
     return false;
};

window.onload = function() {
     var email_input = document.getElementById("email_input");
     var password_input = document.getElementById("password_input");
     var login_button = document.getElementById("login_btn");
     var register_button = document.getElementById("signup_btn");
     var password_button = document.getElementById("pass_btn");

     login_button.onclick = function() {
          var email = email_input.value;
          var password = password_input.value;
          postData("/api/login", {"user_email": email, "user_password": password})
          .then(r =>  r.json().then(data => {
                    if (r.status == 403) {
                         alert("Invalid Email or Password, Try Again!");
                    } 
                    if (r.status == 500 || r.status == 400) {
                         alert("Internal Server Error, Try Again!");
                    }
                    else if (r.status == 200) {
                         encrypted_email = window.btoa(data.email);
                         encrypted_password = window.btoa(data.password);
                         encrypted_license = window.btoa(data.license);
                         encrypted_license_type = window.btoa(data.license_type);
                         encrypted_hwid = window.btoa(data.hwid);
                         encrypted_plan = window.btoa(data.plan_type);
                     
                         var user_data = encrypted_email + "&" + encrypted_password + "&" + encrypted_license + "&" + encrypted_license_type + "&" + encrypted_plan + "&" + encrypted_hwid;
                         document.cookie = `user_data=${user_data}`;
                         window.location.replace("/dash");

                    }
          }
          )) 
     }

     register_button.onclick = function() {
          window.location.replace("/register");
     }

     password_button.onclick = function() {
          var email = prompt("Enter Your Email:", "");
          if (email === null || email === "") {
               return; //break out of the function early
          }
          else {
               postData("/api/forgot_password", {"user_email": email})
               .then(r =>  r.json().then(data => {
                         if (r.status == 404) {
                              alert("Invalid Email, Try Again!");
                         } 
                         if (r.status == 500) {
                              alert("Internal Server Error, Try Again!");
                         }
                         else if (r.status == 200) {
                              alert("Password Reset Email Sent!");
                         }
                    }
               ))}
          }
     }
