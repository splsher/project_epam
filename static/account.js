const change_url = 'http://localhost:6996/user/1';

async function change(id) {
    const inputs = document.getElementById(id).elements;
    var surname = inputs['Surname'].value;
    var name = inputs['Name'].value;
    var password = inputs['Password'].value;
    var accessusers = inputs['Accessusers'].value;
    if (password != password) {
        alert("wrong password");
        return 0;
    }
    var data = {
        "name": name,
        "surname": surname,
        "password": password,
        "accessusers": accessusers
    }
    var url = change_url;
    await fetch(url, {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(async (response) => {
        var res = await response.json();
        if (response.status == 200) {
            var token = res.access_token
            localStorage.setItem('token', token);
        }
        else {
            alert("try again");
        }
    });
}
