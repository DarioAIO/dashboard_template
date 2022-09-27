function getCookie(name) {
     const value = `; ${document.cookie}`;
     const parts = value.split(`; ${name}=`);
     if (parts.length === 2) return parts.pop().split(';').shift();
}

function removeCookie(name) {
     document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
   
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

window.onload = async function() {
     var user_data = getCookie("user_data");
     if (user_data == null) {
          window.location.replace("/login");
     }

     if (typeof browser === "undefined") {
          var browser = chrome;
     }
      
     user_email = window.atob(user_data.split("&")[0]);
     user_password = window.atob(user_data.split("&")[1]);
     user_license = window.atob(user_data.split("&")[2]);
     user_license_type = window.atob(user_data.split("&")[3]);
     user_plan_type = window.atob(user_data.split("&")[4]);
     user_hwid = window.atob(user_data.split("&")[5]);


     var download_button = document.getElementById("download_btn");
     var password_button = document.getElementById("change_pass_btn");
     var payment_buton = document.getElementById("manage_payment_btn");
     var logout_button = document.getElementById("logout_btn");
     var license_field = document.getElementById("license_field");
     var hwid_field = document.getElementById("hwid_field");
     var email_field = document.getElementById("email_field");
     var license_type_field = document.getElementById("license_type_field");
     var plan_feild = document.getElementById("plan_field")
     var hwid_field = document.getElementById("hwid_field");
     license_field.textContent = "License: " + user_license;
     email_field.textContent = "Email: " + user_email;
     plan_feild.textContent = "Plan: " + user_plan_type
     license_type_field.textContent = "License Type: " + user_license_type;
     hwid_field.textContent = "Hardware ID: " + user_hwid;

     license_field.onclick = function() {
          var license_cotent = license_field.textContent.toString()
          var license_cotent = license_cotent.replace("License: ", "");
          navigator.clipboard.writeText(license_cotent);
          alert("License Copied to Clipboard!");
     }    

     hwid_field.onclick = function () {
          if (user_hwid == "N/A") {
               alert("You Haven't Binded Your Mechine Yet!")
          } else {
               postData("/api/reset_hwid", {"user_email": user_email, "user_password": user_password})
               .then(r =>  r.json().then(data => {
                    if (r.status == 404) {
                         alert("Invalid Login Details!");
                    } 
                    if (r.status == 500) {
                         alert("Internal Server Error, Try Again!");
                    }
                    else if (r.status == 200) {
                         alert("HWID Reset Successfully!");
                         window.replace("/dash")
                    }
               }
          ))}
          
     }

     download_button.onclick = function() {
          window.location.replace("https://cdn.discordapp.com/attachments/825091990432776252/1005852964835033188/Nitty_AIO_Alpha.zip");
     }

     password_button.onclick = function() {
          var email = user_email
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

     payment_buton.onclick = function() {
          alert("Payments In Development, To Cancel Contact A Staff Member!")
     }

     logout_button.onclick = function() {
          removeCookie("user_data")
          window.location.replace("/login")
     }
}