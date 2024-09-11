from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from pymongo import MongoClient
from bson import ObjectId, json_util
from datetime import datetime, timedelta, time
import os
from dateutil import parser #Correr este comando: pip install python-dateutil

#Instancia de la aplicación
app = Flask(__name__)
app.secret_key = os.urandom(24)


if __name__ == '_main_':
    app.run(debug=True)
#La función app.run() inicia el servidor web de Flask y ejecuta la aplicación.
#El argumento debug=True indica al servidor web que muestre información de depuración en caso de error.


mongo_client = MongoClient('mongodb+srv://Renzo_Chale:mPpnDhO2vgTRG55w@escuela.jfpdawd.mongodb.net/Escuela')
db = mongo_client.Escuela #Qué base de datos estamos usando.
usuarios = db['usuarios']
reservas = db['reservas']
habitaciones = db['habitaciones']
clientes = db['clientes']

from flask import redirect, url_for

def actualizar_habitacion(numero_habitacion, alimento, cargos_cancelacion, alquilar, numero_camas, estado):
    # Actualizar el documento de la habitación en la colección
    habitaciones.update_one(
        {'numero_habitacion': numero_habitacion},
        {'$set': {'alimento': alimento, 'cargos_cancelacion': cargos_cancelacion, 'alquilar': alquilar, 'numero_camas': numero_camas, 'estado': estado}}
    )
    
@app.route('/guardar_cambios_habitacion/<numero_habitacion>', methods=['POST'])
def guardar_cambios_habitacion(numero_habitacion):
    # Obtener los datos del formulario
    alimento = request.form['alimento']
    cargos_cancelacion = request.form['cargos_cancelacion']
    alquilar = request.form['alquilar']
    numero_camas = request.form['numero_camas']  # Obtener el número de camas del formulario
    estado = request.form['status']  # Obtener el estado de la reserva del formulario
    
    # Llamar a la función para actualizar la habitación en la base de datos
    actualizar_habitacion(numero_habitacion, alimento, cargos_cancelacion, alquilar, numero_camas, estado)
    
    # Redirigir de vuelta a la página de la lista de habitaciones después de guardar los cambios
    return redirect(url_for('all_rooms'))



def actualizar_reserva(numero_reserva, llegada, salida, email, telefono, status):
    # Actualizar el documento de la reserva en la colección
    reservas.update_one(
        {'numero_reserva': numero_reserva},
        {'$set': {'llegada': llegada, 'salida': salida, 'email': email, 'telefono': telefono, 'status': status}}
    )

@app.route('/guardar_cambios_reserva/<numero_reserva>', methods=['POST'])
def guardar_cambios_reserva(numero_reserva):
    # Obtener los datos del formulario
    llegada = request.form['llegada']
    salida = request.form['salida']
    email = request.form['email']
    telefono = request.form['telefono']
    status = request.form['status']  # Agregar esta línea para capturar el estado

    # Llamar a la función para actualizar la reserva en la base de datos
    actualizar_reserva(numero_reserva, llegada, salida, email, telefono, status)

    # Redirigir de vuelta a la página de la lista de reservas después de guardar los cambios
    return redirect(url_for('all_booking'))


def actualizar_usuario(id_personal, primer_nombre, apellido, correo_electronico, celular, contraseña, confirmar_contraseña, rol):
    # Actualizar el documento del usuario en la colección
    usuarios.update_one(
        {'_id': id_personal},
        {'$set': {'primer_nombre': primer_nombre, 'apellido': apellido, 'correo_electronico': correo_electronico, 'celular': celular, 'contraseña': contraseña, 'confirmar_contraseña': confirmar_contraseña, 'rol': rol }}
    )


@app.route('/guardar_cambios_employee/<string:_id>', methods=['POST'])
def guardar_cambios(_id):
    # Obtener los datos del formulario
    primer_nombre = request.form['primer_nombre']
    apellido = request.form['apellido']
    correo_electronico = request.form['correo_electronico']
    celular = request.form['celular']
    contraseña = request.form['contraseña']
    confirmar_contraseña = request.form['confirmar_contraseña']
    rol = request.form['rol']
    
    # Llamar a la función para actualizar el usuario en la base de datos
    actualizar_usuario(_id, primer_nombre, apellido, correo_electronico, celular, contraseña, confirmar_contraseña, rol)
    
    # Redirigir de vuelta a la página de la lista de usuarios después de guardar los cambios
    return redirect(url_for('all_staff'))


@app.route("/all-staff.html")
def all_staff():
    usuarios = db.usuarios.find()
    return render_template("all-staff.html", usuarios=usuarios)


@app.route("/eliminar_cliente/<string:cliente_id>", methods=['POST'])
def eliminar_clientes(cliente_id):
    # Convertir el ID del cliente al formato ObjectId de MongoDB
    cliente_oid = ObjectId(cliente_id)
    # Eliminar el cliente de la base de datos
    result = clientes.delete_one({'_id': cliente_oid})
    
    if result.deleted_count == 1:
        return jsonify({"message": "Cliente eliminado correctamente"}), 200
    else:
        return jsonify({"message": "Cliente no encontrado"}), 404

@app.route("/eliminar_habitacion/<string:numero_habitacion>", methods=['POST'])
def eliminar_habitacion(numero_habitacion):
    # Eliminar la reserva de la base de datos
    habitaciones.delete_one({'numero_habitacion': numero_habitacion})
    return redirect(url_for('all_rooms'))

@app.route("/eliminar_reserva/<string:reserva_id>", methods=['POST'])
def eliminar_reserva(reserva_id):
    # Eliminar la reserva de la base de datos
    reservas.delete_one({'numero_reserva': reserva_id})
    return redirect(url_for('all_booking'))


@app.route("/eliminar_usuario/<string:usuario_id>", methods=['POST'])
def eliminar_usuario(usuario_id):
    # Convertir el _id a ObjectId
    usuario_id = ObjectId(usuario_id)
    # Eliminar al usuario de la base de datos
    usuarios.delete_one({'_id': usuario_id})
    return redirect(url_for('all_staff'))



@app.route('/', methods=['GET', 'POST']) #Verifica datos del formulario con la BdD
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    
        user_data = db.usuarios.find_one({'nombre_usuario': username, 'contraseña': password})
        
        if user_data:
            return render_template('index.html')
        
        else:
             return render_template('login.html')


    return render_template('login.html')
@app.route("/activities.html")
def activities():
    return render_template("activities.html")

@app.route("/add-asset.html")
def add_asset():
    return render_template("add-asset.html")

@app.route("/add-blog.html")
def add_blog():
    return render_template("add-blog.html")

hora_estandar = time(15,0) 
                        

@app.route("/add-booking.html", methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        
        numero_reserva = request.form['numero_reserva']
        nombre = request.form['nombre']
        tipo_habitacion = request.form['tipo_habitacion']
        num_clientes = request.form['num_clientes']
        fecha = request.form['fecha']
        hora = request.form['hora']
        llegada = parser.parse(request.form['llegada'])  # Convertir string a objeto de datetime
        salida = parser.parse(request.form['salida'])  # Convertir string a objeto de datetime
        email = request.form['email']
        telefono = request.form['telefono']
        numero_habitacion = request.form['numero_habitacion']
        nota = request.form['nota']
        status = request.form['status']

        # Combinar fecha y hora de llegada para llegar a un objeto datetime completo
        llegada_datetime = datetime.combine(llegada, parser.parse(hora).time())

        # Combinar fecha de salida con hora estándar (3:00 PM) para formar un objeto datetime completo
        salida_datetime = datetime.combine(salida, hora_estandar)

        data = {
            'numero_reserva': numero_reserva,
            'nombre': nombre,
            'tipo_habitacion': tipo_habitacion,
            'num_clientes': num_clientes,
            'fecha': fecha,
            'hora': hora,
            'llegada': llegada_datetime,
            'salida': salida_datetime,
            'email': email,
            'telefono': telefono,
            'numero_habitacion': numero_habitacion,
            'nota': nota,
            'status': status
        }

        db.reservas.insert_one(data)

        return render_template("add-booking.html")
    
    return render_template("add-booking.html")

@app.route('/add-customer.html', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo_electronico']
        numero_celular = request.form['numero_celular']

        customer_data = {
            'nombre': nombre,
            'apellido': apellido,
            'correo_electronico': correo_electronico,
            'numero_celular': numero_celular
        }

        db.clientes.insert_one(customer_data)

        return render_template("add-customer.html")

    return render_template("add-customer.html")

@app.route("/add-employee.html")
def add_employee():
    return render_template("add-employee.html")

@app.route("/add-expense.html")
def add_expense():
    return render_template("add-expense.html")

@app.route("/add-holiday.html")
def add_holiday():
    return render_template("add-holiday.html")

@app.route("/add-leave-type.html")
def add_leave_type():
    return render_template("add-leave-type.html")

@app.route("/add-leave.html")
def add_leave():
    return render_template("add-leave.html")

@app.route("/add-pricing.html")
def add_pricing():
    return render_template("add-pricing.html")

@app.route("/add-provident-fund.html")
def add_provident_fund():
    return render_template("add-provident-fund.html")

@app.route("/add-role.html")
def add_role():
    return render_template("add-role.html")

@app.route('/add-room.html', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        numero_habitacion = request.form['numero_habitacion']
        existing_room = db.habitaciones.find_one({'numero_habitacion': numero_habitacion})
        if existing_room:
            flash('La habitación ya existe. Por favor, elige otro número de habitación.', 'error')
            return redirect(url_for('add_room'))
        else:
            tipo_habitacion = request.form['tipo_habitacion']
            no_ac = request.form['no_ac']
            alimento = request.form['alimento']
            num_camas = request.form['num_camas']
            cargos_cancelacion = request.form['cargos_cancelacion']
            alquilar = request.form['alquilar']
            mensaje = request.form['mensaje']
            
            # Agregar el estado "Disponible"
            estado = "Disponible"
            
            room_data = {
                'numero_habitacion': numero_habitacion,
                'tipo_habitacion': tipo_habitacion,
                'no_ac': no_ac,
                'alimento': alimento,
                'num_camas': num_camas,
                'cargos_cancelacion': cargos_cancelacion,
                'alquilar': alquilar,
                'mensaje': mensaje,
                'estado': estado  # Agregar el estado aquí
            }

            db.habitaciones.insert_one(room_data)

            return redirect(url_for('add_room'))  # Redirige a la misma página después de guardar

    return render_template("add-room.html")

@app.route('/check-room', methods=['POST'])
def check_room():
    numero_habitacion = request.form['numero_habitacion']
    existing_room = db.habitaciones.find_one({'numero_habitacion': numero_habitacion})
    if existing_room:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})


@app.route("/add-salary.html")
def add_salary():
    return render_template("add-salary.html")

@app.route("/add-staff.html", methods=['GET', 'POST'])
def add_staff():
    if request.method == "POST":
        data = {
            'primer_nombre': request.form['primer_nombre'],
            'apellido': request.form['apellido'],
            'nombre_usuario': request.form['nombre_usuario'],
            'correo_electronico': request.form['correo_electronico'],
            'contraseña': request.form['contraseña'],
            'confirmar_contraseña': request.form['confirmar_contraseña'],
            'dia_ingreso': request.form['dia_ingreso'],
            'celular': request.form['celular'],  
            'rol': request.form['rol'],
            'estado': request.form['status']
        }
        db.usuarios.insert_one(data)
        return render_template("add-staff.html")
    return render_template("add-staff.html")


@app.route("/add-tax.html")
def add_tax():
    return render_template("add-tax.html")

@app.route("/all-booking.html")
def all_booking():
    # Recuperar todas las reservas de la base de datos
    reservas = db.reservas.find()

    # Recuperar todas las habitaciones de la base de datos
    habitaciones = db.habitaciones.find()
    
    # Contar el total de habitaciones
    total_habitaciones = db.habitaciones.count_documents({})

    # Pasar las reservas y las habitaciones a la plantilla "all-booking.html"
    return render_template("all-booking.html", reservas=reservas, habitaciones=habitaciones, total_habitaciones=total_habitaciones)

@app.route("/all-customers.html")
def all_customers():
    # Recuperar todos los clientes de la base de datos
    clientes = db.clientes.find()
    
    # Pasar los clientes a la plantilla "all-customers.html"
    return render_template("all-customers.html", clientes=clientes)


@app.route("/all-rooms.html")
def all_rooms():
    
    habitaciones = db.habitaciones.find()
    
    return render_template("all-rooms.html", habitaciones=habitaciones)





@app.route('/buscar', methods=['POST'])
def buscar_usuarios():
    # Obtener los parámetros de búsqueda del cuerpo de la solicitud
    id_personal = request.form.get('id_personal')
    nombre_personal = request.form.get('nombre_personal')
    rol = request.form.get('rol')

    # Realizar la búsqueda en tu base de datos MongoDB
    # Aquí debes adaptar la consulta según la estructura de tu colección de usuarios en MongoDB
    resultados = usuarios.find({
        'id_personal': id_personal,
        'primer_nombre': {'$regex': '.*' + nombre_personal + '.*', '$options': 'i'},
        'rol': rol
    })

    # Convertir los resultados a una lista de diccionarios
    resultados_lista = [json_util.dumps(usuario, default=str) for usuario in resultados]

    # Devolver los resultados como JSON
    return jsonify(resultados_lista)


@app.route("/assets1.html")
def assets1():
    return render_template("assets1.html")

@app.route("/attendance.html")
def attendance():
    return render_template("attendance.html")

@app.route("/blank-page.html")
def blank_page():
    return render_template("blank-page.html")

@app.route("/blog-details.html")
def blog_details():
    return render_template("blog_details.html")

@app.route("/blog.html")
def blog():
    return render_template("blog.html")

@app.route("/calendar.html")
def calendar():
    return render_template("calendar.html")

@app.route("/change-password.html")
def change_password():
    return render_template("change-password.html")

@app.route("/change-password2.html")
def change_password2():
    return render_template("change-password2.html")

@app.route("/chart-apex.html")
def chart_apex():
    return render_template("chart-apex.html")

@app.route("/chart-c3.html")
def chart_c3():
    return render_template("chart-c3.html")

@app.route("/chart-flot.html")
def chart_flot():
    return render_template("chart-flot.html")

@app.route("/chart-js.html")
def chart_js():
    return render_template("chart-js.html")

@app.route("/chart-morris.html")
def chart_morris():
    return render_template("chart-morris.html")

@app.route("/chart-peity.html")
def chart_peity():
    return render_template("chart-peity.html")

@app.route("/chat-2.html")
def chat_2():
    return render_template("chat-2.html")

@app.route("/chat.html")
def chat():
    return render_template("chat.html")

@app.route("/client-profile.html")
def client_profile():
    return render_template("client-profile.html")

@app.route("/clipboard.html")
def clipboard():
    return render_template("clipboard.html")

@app.route("/compose.html")
def compose():
    return render_template("compose.html")

@app.route("/counter.html")
def counter():
    return render_template("counter.html")

@app.route("/create-invoice.html")
def create_invoice():
    return render_template("create-invoice.html")

@app.route("/drag-drop.html")
def drag_drop():
    return render_template("drag-drop.html")

@app.route("/edit-asset.html")
def edit_asset():
    return render_template("edit-asset.html")

@app.route("/edit-blog.html")
def edit_blog():
    return render_template("edit-blog.html")

@app.route("/edit-booking.html")
def edit_booking():
    return render_template("edit-booking.html")

@app.route("/edit-customer.html")
def edit_customer():
    return render_template("edit-customer.html")

@app.route("/edit-employee.html")
def edit_employee():
    return render_template("edit-employee.html")

@app.route("/edit-expense.html")
def edit_expense():
    return render_template("edit_expense.html")

@app.route("/edit-holiday.html")
def edit_holiday():
    return render_template("edit-holiday.html")

@app.route("/edit-invoice.html")
def edit_invoice():
    return render_template("edit-invoice.html")

@app.route("/edit-leave-type.html")
def edit_leave_type():
    return render_template("edit-leave-type.html")

@app.route("/edit-leave.html")
def edit_leave():
    return render_template("edit-leave.html")

@app.route("/edit-pricing.html")
def edit_pricing():
    return render_template("edit-princing.html")

@app.route("/edit-profile-customer.html")
def edit_profile_customer():
    return render_template("edit-profile-customer.html")

@app.route("/edit-profile.html")
def edit_profile():
    return render_template("edit-profile.html")

@app.route("/edit-provident-fund.html")
def edit_provident_fund():
    return render_template("edit-provident-fund.html")

@app.route("/edit-role.html")
def edit_role():
    return render_template("edit-role.html")

@app.route("/edit-room.html")
def edit_room():
    return render_template("edit-room.html")

@app.route("/edit-salary.html")
def edit_salary():
    return render_template("edit-salary.html")

@app.route("/edit-staff.html")
def edit_staff():
    return render_template("edit-staff.html")

@app.route("/edit-tax.html")
def edit_tax():
    return render_template("edit-tax.html")

@app.route("/email-settings.html")
def email_settings():
    return render_template("email-settings.html")

@app.route("/employees.html")
def employees():
    return render_template("employees.html")

@app.route("/error-404.html")
def error_404():
    return render_template("error-404.html")

@app.route("/error-500.html")
def error_500():
    return render_template("error-500.html")

@app.route("/expense-reports.html")
def expense_reports():
    return render_template("expense-reports.html")

@app.route("/expenses.html")
def expenses():
    return render_template("expenses.html")

@app.route("/forgot-password.html")
def forgot_password():
    return render_template("forgot-password.html")

@app.route("/form-basic-inputs.html")
def form_basic_inputs():
    return render_template("form-basic-inputs.html")

@app.route("/from-fileupload.html")
def from_fileupload():
    return render_template("from-fileupload.html")

@app.route("/from-horizontal.html")
def from_horizontal():
    return render_template("from-horizontal.html")

@app.route("/from-input-groups.html")
def from_input_groups():
    return render_template("from-input-groups.html")

@app.route("/form-mask.html")
def form_mask():
    return render_template("form-mask.html")

@app.route("/form-select2.html")
def form_select2():
    return render_template("form-select2.html") 

@app.route("/form-validation.html")
def form_validation():
    return render_template("form-validation.html")

@app.route("/form-vertical.html")
def form_vertical():
    return render_template("form-vertical.html")

@app.route("/form-wizard.html")
def form_wizard():
    return render_template("form-wizard.html")

@app.route("/gallery.html")
def gallery():
    return render_template("gallery.html")

@app.route("/holidays - copia.html")
def holidays_copia():
    return render_template("holidays - copia.html")

@app.route("/holidays.html")
def holidays():
    return render_template("holidays.html")

@app.route("/horizontal-timeline.html")
def horizontal_timeline():
    return render_template("horizontal-timeline.html")

@app.route("/icon-feather.html")
def icon_feather():
    return render_template("icon-feather.html")

@app.route("/icon-flag.html")
def icon_flag():
    return render_template("icon-flag.html")

@app.route("/icon-fontawesome.html")
def icon_fontawesome():
    return render_template("icon-fontawesome.html")

@app.route("/icon-ionic.html")
def icon_ionic():
    return render_template("icon-ionic.html")

@app.route("/icon-material.html")
def icon_material():
    return render_template("icon-material.html")

@app.route("/icon-pe7.html")
def icon_pe7():
    return render_template("icon-pe7.html")

@app.route("/icon-simpleline.html")
def icon_simpleline():
    return render_template("icon-simpleline.html")

@app.route("/icon-themify.html")
def icon_themify():
    return render_template("icon-themify.html")

@app.route("/icon-typicon.html")
def icon_typicon():
    return render_template("icon-typico .html")

@app.route("/icon-weather.html")
def icon_weather():
    return render_template("icon-weather.html")

@app.route("/inbox.html")
def inbox():
    return render_template("inbox.html")

@app.route("/index.html", methods=['GET', 'POST'])
def index():
    # Obtener todas las reservas de la base de datos
    reservas = db.reservas.find()
    
    # Obtener todas las habitaciones de la base de datos
    habitaciones = db.habitaciones.find()

    total_reservas = db.reservas.count_documents({})

    total_habitaciones = db.habitaciones.count_documents({})

    # Renderizar la plantilla index.html y pasar las reservas y habitaciones como contexto
    return render_template("index.html", reservas=reservas, habitaciones=habitaciones,total_reservas=total_reservas,total_habitaciones=total_habitaciones)


@app.route("/invoice-reports.html")
def invoice_reports():
    return render_template("invoice-reports.html")

@app.route("/invoice-settings.html")
def invoice_settings():
    return render_template("invoice-settings.html")

@app.route("/invoice-view.html")
def invoice_view():
    return render_template("invoice-view.html")

@app.route("/invoices.html")
def invoices():
    return render_template("invoices.html")

@app.route("/leave-type.html")
def leave_type():
    return render_template("leave-type.html")

@app.route("/leaves.html")
def leaves():
    return render_template("leaves.html")

@app.route("/lightbox.html")
def lightbox():
    return render_template("lightbox.html")

@app.route("/localization.html")
def localization():
    return render_template("localization.html")

@app.route("/lock-screen.html")
def lock_screen():
    return render_template("lock-screen.html")

@app.route("/login.html")
def loginpage():
    return render_template("login.html")

@app.route("/mail-view.html")
def mail_view():
    return render_template("mail-view.html")

@app.route("/notification.html")
def notification():
    return render_template("notification.html")

@app.route("/notifications-settings.html")
def notifications_settings():
    return render_template("notifications-settings.html")

@app.route("/payments.html")
def payments():
    return render_template("payments.html")

@app.route("/popover.html")
def popover():
    return render_template("popover.html")

@app.route("/pricing.html")
def pricing():
    return render_template("pricing.html")

@app.route("/profile.html")
def profile():
    return render_template("profile.html")

@app.route("/provident-fund.html")
def provident_fund():
    return render_template("provident-fund.html")

@app.route("/rangeslider.html")
def rangeslider():
    return render_template("rangeslider.html")

@app.route("/rating.html")
def rating():
    return render_template("rating.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/ribbon.html")
def ribbon():
    return render_template("riboon.html")

@app.route("/roles-permissions.html")
def roles_permissions():
    return render_template("roles-permissions.html")

@app.route("/salary-settings.html")
def salary_settings():
    return render_template("salary-settings.html")

@app.route("/salary-view.html")
def salary_view():
    return render_template("salary-view.html")

@app.route("/salary.html")
def salary():
    return render_template("salary.html")

@app.route("/scrollbar.html")
def scrollbar():
    return render_template("scrollbar.html")

@app.route("/settings.html")
def settings():
    return render_template("settings.html")

@app.route("/spinner.html")
def spinner():
    return render_template("spinner.html")

@app.route("/stickynote.html")
def stickynote():
    return render_template("stickynote.html")

@app.route("/sweetalerts.html")
def sweetalerts():
    return render_template("sweetalerts.html")

@app.route("/tables-basic.html")
def tables_basic():
    return render_template("tables-basic.html")

@app.route("/tables-datatables.html")
def tables_datatables():
    return render_template("tables-datatables.html")

@app.route("/tabs.html")
def tabs():
    return render_template("tabs.html")

@app.route("/taxes.html")
def taxes():
    return render_template("taxes.html")

@app.route("/text-editor.html")
def text_editor():
    return render_template("text-editor.html")

@app.route("/theme-settings.html")
def theme_settings():
    return render_template("theme-settings.html")

@app.route("/timeline.html")
def timeline():
    return render_template("timeline.html")

@app.route("/toastr.html")
def toastr():
    return render_template("toastr.html")

@app.route("/tooltip.html")
def tooltip():
    return render_template("tooltip.html")

@app.route("/typography.html")
def typography():
    return render_template("typography.html")

@app.route("/uikit.html")
def uikit():
    return render_template("uikit.html")

@app.route("/video-call.html")
def video_call():
    return render_template("video-call.html")

@app.route("/voice-call.html")
def voice_call():
    return render_template("voice-call.html")

if __name__ == "__main__":
    app.run()

