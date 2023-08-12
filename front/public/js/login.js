function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}






let urlLogin = 'http://localhost:8000/'; // URL del servidor HTTP

const varlidarSesion = () => {
    const token = getCookie("token")
    if (token){
        fetch(`${urlLogin}ruta2`, {
            method: 'POST',
            body: JSON.stringify({"token":token}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                
            }
        })
        .then((resp) => resp.json())
        .then(data => {
            console.log("Logueado")
            if(data.is_logged_in){
                console.log("Logueado")
                window.location.href = "index.html"
    
            }
            else{
                console.log("No logueado")
 
            }
        })
        .catch(error => {
            if (error.status === 401) {
                console.error('Error al obtener el estado del usuario:', error);
        }});
    }
    else{
        console.log("No Existe")
    }
        

};

(function() {
    varlidarSesion()
})();



/************************Loguearse*******************************/

let userStatusElement = document.getElementById("user-status")
let sesionOn = document.querySelector(".sesionOn")
let sesionOff = document.querySelector(".sesionOff")
let form = document.getElementById('formLogin');



  if(form){
    form.addEventListener('submit', function(e){   
        e.preventDefault();
        let botonIniciar = document.getElementById('formLoginButtom')
        botonIniciar.removeAttribute("type")
        botonIniciar.classList.add("buttonInactive")
        botonIniciar.innerText = "Validating..."
        let usuario = document.getElementById("username").value;
        let password =  document.getElementById("password").value;
        let data = {
            "usuario":usuario,
            "password":password
        }
    
        fetch(`${urlLogin}ruta1`, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                        
                    }
                })
        .then((resp) => resp.json())
        .then(data =>{
            console.log(data)
            if (data.is_logged_in) {
                contenido = JSON.stringify(data);
                const fechaExpiracion = new Date();
                fechaExpiracion.setTime(fechaExpiracion.getTime() + 120 * 60 * 1000); // 30 minutos
                document.cookie = `token=${data.token}; expires=${fechaExpiracion.toUTCString()}; path=/`;
                Swal.fire({
                    title: "Bienvenido",
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'Aceptar',
                    willClose: function() {
                        redireccionar();
                      }
                })
                function redireccionar(){
                    window.location.href = "index.html"
                }
                setTimeout(redireccionar, 2000)
            }
            else{

                Swal.fire({
                    title: "Error al iniciar sesión",
                    text: data.message,
                    icon: 'error',
                    confirmButtonText: 'Aceptar',
                    willClose: function() {
                        location.reload();
                      }
                })
            }

        })
        .catch(error => {
            console.error('Error al obtener el estado del usuario:', error);
        });
    });
    
}