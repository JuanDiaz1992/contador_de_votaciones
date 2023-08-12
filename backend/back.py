from actions.insertBD import DatabaseInsert
from actions.BdQuery import DatabaseQuery
from actions.BdModify import DatabaseModify
from actions.BdDelete import DatabaseDelete
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import cgi
import pandas as pd
import os
import re
import shutil



from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

database_host = 'localhost'
database_user = 'root'
database_password = '3118514322s'
database_name = 'voting'

connectorConsultas = DatabaseQuery(database_host, database_user, database_password, database_name)
connectorInsert = DatabaseInsert(database_host, database_user, database_password, database_name)
conecctorModify = DatabaseModify(database_host, database_user, database_password, database_name)
conectorDelete = DatabaseDelete(database_host, database_user, database_password, database_name)



class RequestHandler(BaseHTTPRequestHandler):
    

    def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")
      
    def do_OPTIONS(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

    def do_POST(self):

#**************************INICIO DE SESION**********************************
        if self.path == '/ruta1':
            # Leer los datos del cuerpo de la solicitud
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            # Decodificar el JSON recibido
            dataJson = json.loads(body)
            # Acceder a los datos del JSON
            name = dataJson['usuario']
            passwordFront = dataJson['password']

            usuarioExist = connectorConsultas.get_coordinator_by_password_and_name(passwordFront,name)
            if usuarioExist:
                print("SI")
                consultaUsuario = connectorConsultas.get_session_by_id(usuarioExist[0])
                if consultaUsuario:
                    cambiarEstadoLogin = conectorDelete.delete_session(usuarioExist[0])
                    token = random.randint(4,2000)
                    loggin = connectorInsert.insert_session(usuarioExist[0], True,token)
                    
                else:
                    token = random.randint(4,2000)
                    loggin = connectorInsert.insert_session(usuarioExist[0], True,token)

                data = {
                    "token":token,
                    "message": "Inicio de sesión exitoso",
                    "is_logged_in":True,
                    
                }
                
            else:
                print("NO")
                data = {
                    "message": "Credenciales inválidas",
                    "is_logged_in":False,
                }
            # Convertir la respuesta a formato JSON
            response_json = json.dumps(data)
            self.send_response(200)  # Código de respuesta HTTP
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
                    
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))
            

#***********************************Validar Sesión Activa****************************
        elif self.path == '/ruta2':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            dataJson = json.loads(body)
            token = dataJson['token']
            sessionExist = connectorConsultas.get_session_active_by_token(token)
            if sessionExist:
                coordinator = connectorConsultas.get_coordinator_by_id(sessionExist[0])
                data = {
                    "coordinator":coordinator[1],
                    "message": "Session activa",
                    "is_logged_in":True,
                    
                }
                
            else:
                data = {
                    "message": "No hay una session activa",
                    "is_logged_in":False,
                }
            # Convertir la respuesta a formato JSON
            response_json = json.dumps(data)
            self.send_response(200)  # Código de respuesta HTTP
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))




#***********************************Ingreso Formulario****************************                
        elif self.path == '/ingresoForm':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            dataJson = json.loads(body)
            token = dataJson['token']
            sessionExist = connectorConsultas.get_session_active_by_token(token)
            coordinator = connectorConsultas.get_coordinator_by_id(sessionExist[0])
            if coordinator[2] == dataJson['document'] and coordinator[3] == dataJson['email']:
                try:
                    print("ok")
                    data={
                        "data_saved":True
                        }
                    connectorInsert.insert_election_from_form(dataJson['year'], dataJson['vote_count'], dataJson['political_party'],  dataJson['county'], coordinator[0])
                except:
                    print("error")
                    data={
                        "message":"Error registering the data, validate and try again",
                        "data_saved":False
                        }
            else:
                print("else")
                data={  "message":"Wrong document or email",
                        "data_saved":False
                        }

            response_json = json.dumps(data)
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))

#***********************************Subir excel****************************                
        elif self.path == '/uploadExcel':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            uploads_folder = os.path.join(os.path.dirname(__file__), 'uploads')
            if not os.path.exists(uploads_folder):
                os.makedirs(uploads_folder)
            excel_file = form['excelFile']
            file_path = os.path.join(uploads_folder, excel_file.filename)
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(excel_file.file, file)
            temp_filepath = file_path
            dataframe = pd.read_excel(temp_filepath, na_values='')
            # conectorDelete.delete_all_countys()
            try:
                for index, row in dataframe.iterrows():
                    codecounty = int(row['codecounty'])
                    county = re.sub(r'[^a-zA-Z0-9]', '', str(row['county']))
                    population = row['population']
                    area = row['area']
                    if pd.isna(codecounty) or pd.isna(county) or pd.isna(population) or pd.isna(area):
                        continue  # Omitir la fila si alguna columna está vacía
                    # Verificar si el condado ya existe en el diccionario

                    print(f'Cargando: {index}')

                    connectorInsert.insert_county(codecounty, county, population, area)
                    print(f'Guardando: {county}')

                data = {
                    "message": "File uploaded successfully",
                    "data_saved": True
                }
            except:
                data = {
                    "message": "There is an error in the file, validate it in try again",
                    "data_saved": False
                }


            response_json = json.dumps(data)
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))

#***********************************Subir JSON****************************        
        elif self.path == '/uploadJson':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            uploads_folder = os.path.join(os.path.dirname(__file__), 'uploads')
            if not os.path.exists(uploads_folder):
                os.makedirs(uploads_folder)
            json_file = form['jsonlFile']

            
            file_path = os.path.join(uploads_folder, json_file.filename)
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(json_file.file, file)

            with open(file_path) as json_data:
                data = json.load(json_data)
            token = form.getvalue('token')
            coordinator = connectorConsultas.get_session_active_by_token(token)
            # conectorDelete.delete_all_election()
            for item in data:
                year = item['year']
                count_democrat = item['democrat']
                count_republic = item['republic']
                count_other = item['other']
                id_codecounty = int(item['codecounty'])
                # if item['year'] == '' and item['democrat'] == '' and item['republic'] == '' and item['other'] == '' and item['codecounty'] == '':
                #     continue 
                connectorInsert.insert_election(year,count_democrat,"Democrat",id_codecounty,coordinator[0])
                connectorInsert.insert_election(year,count_republic,"Republic",id_codecounty,coordinator[0])
                connectorInsert.insert_election(year,count_other,"Other",id_codecounty,coordinator[0])
                print(item)
                
            data = {
                "message": "File uploaded successfully",
                "data_saved": True
            }


            response_json = json.dumps(data)
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))




#***********************************Cerrar session****************************            
        elif self.path == '/rutaCerrarSesion':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            dataJson = json.loads(body)
            token = dataJson['token']
            conectorDelete.delete_session_by_token(token)
            data={
                "is_logged_in":False
                }
            response_json = json.dumps(data)
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))
               



#***********************************Validar countys****************************

        elif self.path == '/getCountys':
            countys = connectorConsultas.get_all_countys()
            if countys:
                data={
                    "countys":countys,
                    "datosExist":True
                }
            else:
                data={
                    "datosExist":False
                }
            response_json = json.dumps(data)
            self.send_response(200)  # Código de respuesta HTTP
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
                    
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))

        else:
            # Ruta no encontrada
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Ruta no encontrada')


    def do_GET(self):

#***********************************Obtener conteo de votos****************************

        if self.path == '/getCount':
            count = connectorConsultas.get_all_election()
            countys = connectorConsultas.get_all_countys()
            if count:
                data = {
                    "count":count,
                    "countys":countys,
                    "data":True
                }
            else:
                data = {
                    "data":False
                }
            response_json = json.dumps(data)
            self.send_response(200)  # Código de respuesta HTTP
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
                    
            # Enviar la respuesta
            self.wfile.write(response_json.encode(encoding='utf_8'))

        else:
            # Ruta no encontrada
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Ruta no encontrada')


def realizar_cambio_en_bd():
    # Borrar todas las sesiones activas
    conectorDelete.closeAllSesiones()
    

# Crea una instancia del planificador
scheduler = BackgroundScheduler()

# Programa la tarea para que se ejecute después de 2 horas utilizando un disparador de intervalo
trigger = IntervalTrigger(hours=2)
scheduler.add_job(realizar_cambio_en_bd, trigger)

# Inicia el planificador
scheduler.start()
            

def run_server():
    host = 'localhost'
    port = 8000
    server_address = (host, port)
    


    # Iniciar el servidor HTTP dentro del bloque try-except
    try:
        with HTTPServer(server_address, RequestHandler) as httpd:
            print(f'Servidor iniciado en {host}:{port}')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('Servidor detenido')

if __name__ == '__main__':
    # Iniciar el servidor
    run_server()