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
     var login_button = document.getElementById("login_button");
     var unsub_button = document.getElementById("unsub_btn");

     login_button.onclick = function() {
          window.location.replace("/login");     
     }

     unsub_button.onclick = function() {
          var email = prompt("Enter Your Email", "example@gmail.com")     
          postData("/api/unsubscribe", {"user_email": email})
               .then(function (res) {
                         if (res.status == 403) {
                              alert("Invalid Email, Try Again!");
                         } 
                         if (res.status == 400) {
                              alert("Email Not Registerd!");
                         }
                         if (res.status == 500) {
                              alert("Internal Server Error, Try Again!");
                         }
                         else if (res.status == 200) {
                              alert("Unsubscribed From Waiting List!");
                         }
                    }
          ) 
     }

     email_input.addEventListener("keydown", function(event) {
          if (event.key === "Enter") {
               postData("/api/wait_list", {"user_email": email_input.value})
               .then(function (res) {
                         if (res.status == 403) {
                              alert("Invalid Email, Try Again!");
                         } 
                         if (res.status == 400) {
                              alert("Email Alredy Registerd!");
                         }
                         if (res.status == 500) {
                              alert("Internal Server Error, Try Again!");
                         }
                         else if (res.status == 200) {
                              alert("Added to Waiting List!");
                         }
                    }
               ) 
          }
     });
} 
      
