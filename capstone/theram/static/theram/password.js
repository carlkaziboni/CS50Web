document.addEventListener("DOMContentLoaded", ()=>{
    const password = document.getElementById("id_password");
    const password_confirm = document.getElementById("id_confirm_password");
    const submit_button = document.getElementById("submit-id-submit");
    submit_button.disabled = true;
    password.addEventListener("change", ()=>{
        if ((password.value == password_confirm.value) && (password.value.length > 0)){
            submit_button.disabled = false;
        }
        else{
            submit_button.disabled = true;
        }
    });
    password_confirm.addEventListener("change", ()=>{
        if ((password.value == password_confirm.value) && (password.value.length > 0)){
            submit_button.disabled = false;
        }
        else{
            submit_button.disabled = true;
        }
    });
});