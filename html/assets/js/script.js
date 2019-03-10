function validationSignUp(){
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;
    // var agreement = document.getElementById("agreement").value;

    if (username == ""){
        alert("username tidak boleh kosong");
        return false;
    }
    
    if (email == ""){
        alert("email tidak boleh kosong");
        return false;
    }

    if (password == "" || confirmPassword == ""){
        alert("password tidak boleh kosong");
        return false;
    }
  
    if (password !== confirmPassword){
        alert("password tidak sesuai, coba ulangi")
        return false
    }

    // if (agreement=0){
    //     alert("Setujui")
    //     return false
    // }
  
    return true;
}

function validationLogin(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username == ""){
        alert("username tidak boleh kosong");
        return false;
    }

    if (password == ""){
        alert("password tidak boleh kosong");
        return false;
    }

    return true;
}

function Delete(){
    var deleteAccount = document.getElementById("delete-account").value;

    if (deleteAccount == true){
        alert("Apakah Anda yakin hendak menghapus akun Anda?");
        return true;
    }
}