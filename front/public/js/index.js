/************************Gestión de cookies*******************************/

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

function deleteAllCookies() {
    var cookies = document.cookie.split(";");
  
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var eqPos = cookie.indexOf("=");
      var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }
  }
  
  // Llamada a la función para eliminar todas las cookies

  

let url = 'http://localhost:8000/'; // URL del servidor HTTP


/************************Validar session activa*******************************/

const validarSession=()=>{
    const token = getCookie("token")
    if (token){
        fetch(`${url}ruta2`, {
            method: 'POST',
            body: JSON.stringify({"token":token}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                
            }
        })
        .then((resp) => resp.json())
        .then(data => {
    
            if(data.is_logged_in){
                console.log("Logueado")
                let userNav = document.getElementById("user")
                userNav.innerText = data.coordinator
            }
            else{
                console.log("No logueado")
                window.location.href = "login.html"
            }
        })
        .catch(error => {
            if (error.status === 401) {
                console.error('Error al obtener el estado del usuario:', error);
        }});
    }
    else{
        console.log("No Existe Un TOKEN")
        window.location.href = "login.html"
    }
}




/************************Desloguear el sistema******************************/


const buttomCloseSesion = document.getElementById("closeSession")
buttomCloseSesion.addEventListener("click",function(){
    const token = getCookie("token")
    fetch(`${url}rutaCerrarSesion`,{
        method: 'POST',
        mode: 'cors',
        body: JSON.stringify({"token":token}),
        headers: {
            'Content-Type': 'application/json',
        }
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        Swal.fire({
            title: "Haz finalizado la sesión",
            icon: 'info',
            confirmButtonText: 'Aceptar',
            willClose: function() {
                window.location.href = "login.html"
              }})
        deleteAllCookies();
        
      })
      .catch(error => {
        console.error('Error al desloguear:', error);
      });
})


/************************OBTENER TODOS LOS COUNTYS******************************/
const selectCounty = document.getElementById("select_county");

if(selectCounty){
    (function() {
            const token = getCookie("token")
            fetch(`${url}getCountys`, {
                method: "POST",
                body: JSON.stringify({"token":token}),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    
                }
            })
            .then((resp) => resp.json())
            .then(data => {
                if (data.datosExist) {
                const countys = data.countys;
                countys.sort((a, b) => a[2].localeCompare(b[2]));
                selectCounty.innerHTML = "";
                const defaultOption = document.createElement("option");
                defaultOption.value = "";
                defaultOption.textContent = "Choose an option";
                selectCounty.appendChild(defaultOption);
                countys.forEach(county => {
                    const option = document.createElement("option");
                    option.value = county[0];
                    option.textContent = `${county[2]} ${county[1]}`;
                    selectCounty.appendChild(option);
                });
        
                }
                else {
                selectCounty.innerHTML = "";
                const defaultOption = document.createElement("option");
                defaultOption.value = "";
                defaultOption.textContent = "Choose an option";
                selectCounty.appendChild(defaultOption);
                }
            
            })
    })();
}




/************************Envío de formulario******************************/



let formElection = document.getElementById("form_elecition")
if(formElection){
    formElection.addEventListener("submit",function(e){
        e.preventDefault();


        const token = getCookie("token")
        let document_user = document.getElementById("document_user")
        let email_user = document.getElementById("email_user")
        let year = document.getElementById("year")
        let political_party = document.getElementById("select_party")
        let vote_count = document.getElementById("vote_count")


        let botonIniciar = document.getElementById('button_form_election')
        botonIniciar.removeAttribute("Type")
        botonIniciar.classList.add("buttonInactive")
        botonIniciar.innerText = "Sending..."

        county = selectCounty.value
 
        data = {
            "document":document_user.value,
            "email":email_user.value,
            "year":year.value,
            "political_party":political_party.value,
            "county":county,
            "vote_count":vote_count.value,
            "token":token
        }
        fetch(`${url}ingresoForm`,{
            method: "POST",
            mode: "cors",
            body: JSON.stringify(data),
            headers:{
                'Content-Type': 'application/json',
            }
        })
        .then((resp)=>resp.json())
        .then(data=>{
            if(data.data_saved){
                console.log(data.data_saved)
                formElection.reset();
                botonIniciar.classList.remove("buttonInactive")
                botonIniciar.innerText = "Submit"
                getCountys()
                Swal.fire({
                    title: "Regitro ok",
                    icon: 'info',
                    confirmButtonText: 'Aceptar',
                })
                
            }
            else{
                Swal.fire({
                    title: data.message,
                    icon: 'error',
                    confirmButtonText: 'Aceptar',
                })
                botonIniciar.classList.remove("buttonInactive")
                botonIniciar.innerText = "Submit"
            }
        })
        
        
    })
}

/************************Cargar Excel******************************/

let formExcel = document.getElementById("formExcel")
if (formExcel) {
    formExcel.addEventListener('submit', function(e){
        e.preventDefault();
        let botonIniciar = document.getElementById('buttonformLoadExcel')
        botonIniciar.classList.add("buttonInactive")
        botonIniciar.innerText = "Sending EXCEL..."
        let excelArchve = document.getElementById("file_excel")
        let selectedFile = excelArchve.files[0];
        let formData = new FormData();
        formData.append('excelFile', selectedFile);
        fetch(`${url}uploadExcel`, {
            method: 'POST',
            body: formData,
            mode: "cors",
        })
            .then((resp) => resp.json())
            .then(data => {
                if(data.data_saved){
                    Swal.fire({
                        title: "Regitro ok",
                        icon: 'success',
                        confirmButtonText: 'Aceptar',
                        willClose: function() {
                            window.location.href = "index.html"
                          }
                    })

                }
                else{
                    Swal.fire({
                        title: data.message,
                        icon: 'error',
                        confirmButtonText: 'Aceptar',
                    })

                }
                botonIniciar.classList.remove("buttonInactive")
                botonIniciar.innerText = "Load"
                formExcel.reset();



            })
            .catch(error => {
            // Manejar el error
            botonIniciar.classList.remove("buttonInactive")
            botonIniciar.innerText = "Load"
            formExcel.reset();
            });

    })
}


/************************Cargar JSON******************************/
let formJson = document.getElementById("formJson")
if(formJson){
    formJson.addEventListener("submit",function(e){
        e.preventDefault()
        const token = getCookie("token")
        let botonIniciar = document.getElementById('buttonformLoadJson')
        botonIniciar.classList.add("buttonInactive")
        botonIniciar.innerText = "Sending JSON..."
        let jsonArchve = document.getElementById("file_Json")
        let selectedFile = jsonArchve.files[0];
        let formData = new FormData();
        formData.append('jsonlFile', selectedFile);
        formData.append('token', token);
        fetch(`${url}uploadJson`, {
            method: 'POST',
            body: formData,
            mode: "cors",
        })
            .then((resp) => resp.json())
            .then(data => {
                if(data.data_saved){
                    Swal.fire({
                        title: "Regitro ok",
                        icon: 'success',
                        confirmButtonText: 'Aceptar',
                        willClose: function() {
                            window.location.href = "index.html"
                          }
                    })

                }
                else{
                    Swal.fire({
                        title: data.message,
                        icon: 'error',
                        confirmButtonText: 'Aceptar',
                    })

                }
                botonIniciar.classList.remove("buttonInactive")
                botonIniciar.innerText = "Load"
                formExcel.reset();



            })
            .catch(error => {
            // Manejar el error
            botonIniciar.classList.remove("buttonInactive")
            botonIniciar.innerText = "Load"
            formExcel.reset();
            });

    })

}



(function() {
    validarSession()
})();

