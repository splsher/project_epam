function log(){
    username =  document.getElementById("username").value;
    password = document.getElementById("password").value;
    data =
        { "username":username, "password":password};
        console.log(data)
    fetch("http://127.0.0.1:5000/login",
        {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Accept': '*/*'
                    },
        body:JSON.stringify(data)}).then(res=>{
            if(res.ok){
                return res.json()
            }else{
                debugger
                alert("something is wrong")
            }
        }).then(jsonResponse=>{
            createCookie('token',jsonResponse,7);
            createCookie('username',username,7);
            location.replace("index.html")
            }
        ).catch((err) => {
            console.error(err)
            createCookie('token','0',7);
        }
        );
};
