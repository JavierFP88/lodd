import json
import requests
import time
from pathlib import Path

# Configuración
SERVICE_URL = "http://10.2.3.133:3000/enviar-correo"
BCC_EMAIL = "cggis@coralgables.com,itsdnotification@coralgables.com"  # Email para copia oculta (opcional)

# Template del email en HTML para LODD Training
EMAIL_TEMPLATE = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #f9f9f9; padding: 30px; border-radius: 8px; border-left: 5px solid #0078d4;">
        
        <p><strong>Dear Departmental POC,</strong></p>
        
        <p>This is the second of three informational emails you will receive regarding the upcoming <strong>Multi-Agency Line of Duty Death (LODD) – South Florida Best Practices training</strong>.</p>
        
        <p>Please ensure that the number of personnel reserved for your department is accurately reflected on the final roster and matches your original request as seats are limited. The attached email contains the registration link — kindly forward it to your assigned personnel so they can register in our system and receive credit for attendance.</p>
        
        <p>If any cancellations occur, please reply to the original message thread so that we can promptly open those seats for other agencies currently on the waiting list.</p>
        
        <p style="text-align: center; margin: 25px 0;">
            <a href="https://arcg.is/1P5WOT2" 
               style="background-color: #0078d4; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; font-size: 16px;">
                👉 Click here to register for the training
            </a>
        </p>
        
        <p>Please review the following important details to help your personnel plan accordingly:</p>
        
        <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0; border: 1px solid #ddd;">
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>Arrival Time:</strong> Check-in begins at 7:30 AM, and the opening ceremony will start promptly at 8:00 AM.</li>
                <li><strong>Traffic Advisory:</strong> Coral Gables experiences heavy morning traffic and limited parking. Allow extra time for travel and parking.</li>
                <li><strong>Lunch:</strong> A hot lunch will be provided to all attendees, courtesy of Veterans Last Call.</li>
                <li><strong>Dress Code:</strong> Business casual or agency uniform is recommended.</li>
            </ul>
        </div>
        
        <h3 style="color: #0078d4; border-bottom: 2px solid #0078d4; padding-bottom: 5px;">Training Outline</h3>
        
        <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; margin: 20px 0; border: 1px solid #ddd;">
            <ul style="margin: 0; padding-left: 20px; list-style-type: none;">
                <li style="margin-bottom: 8px;">📅 <strong>8:00 AM</strong> – Opening Ceremony</li>
                <li style="margin-bottom: 8px;">🎤 <strong>Morning Session</strong> – Guest Speakers and Presentations</li>
                <li style="margin-bottom: 8px;">🍽️ <strong>12:00 PM</strong> – Lunch (Hot Meal Provided)</li>
                <li style="margin-bottom: 8px;">💼 <strong>Afternoon Session</strong> – South Florida Best Practices and Collaborative Planning</li>
                <li style="margin-bottom: 8px;">❓ <strong>Closing Remarks and Q&A</strong></li>
            </ul>
        </div>
        
        <p>At the conclusion of the training, attendees will receive access to a QR code that will provide:</p>
        
        <div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #0078d4;">
            <ul style="margin: 0; padding-left: 20px;">
                <li>A post-event survey</li>
                <li>Their certificate of completion</li>
                <li>All training materials covered during instruction</li>
            </ul>
        </div>
        
        <p>We appreciate your cooperation and attention in ensuring your department's participants are properly registered and accounted for. This event represents an important opportunity to strengthen inter-agency coordination and uphold the highest standards of professionalism in handling Line of Duty Death events.</p>
        
        <p style="margin-top: 30px;">
            <strong>Respectfully,</strong><br>
            <span style="color: #0078d4; font-weight: bold;">Marcos De Rosa</span><br>
            <span style="color: #0078d4; font-weight: bold;">Police Officer</span><br>
            <span style="color: #0078d4; font-weight: bold;">Coral Gables Police Department</span>
        </p>
        
    </div>
</body>
</html>
"""

def load_recipients(json_file_path):
    """Carga la lista de destinatarios desde el archivo JSON LODD"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Combinar todas las categorías en una sola lista
        all_recipients = []
        
        # Procesar Speakers
        if 'Speakers' in data:
            for speaker in data['Speakers']:
                if 'email' in speaker and speaker['email']:  # Solo si tiene email
                    all_recipients.append({
                        'name': speaker['name'],
                        'email': speaker['email'],
                        'title': speaker.get('title', ''),
                        'agency': speaker.get('agency', ''),
                        'category': 'Speaker'
                    })
        
        # Procesar Participants_Police
        if 'Participants_Police' in data:
            for participant in data['Participants_Police']:
                if 'email' in participant and participant['email']:  # Solo si tiene email
                    all_recipients.append({
                        'name': participant['name'],
                        'email': participant['email'],
                        'title': participant.get('title', ''),
                        'agency': participant.get('agency', ''),
                        'category': 'Police Participant'
                    })
        
        # Procesar Participants_Fire
        if 'Participants_Fire' in data:
            for participant in data['Participants_Fire']:
                if 'email' in participant and participant['email']:  # Solo si tiene email
                    all_recipients.append({
                        'name': participant['name'],
                        'email': participant['email'],
                        'title': participant.get('title', ''),
                        'agency': participant.get('agency', ''),
                        'category': 'Fire Participant'
                    })
        
        print(f"✅ Cargados {len(all_recipients)} destinatarios con email del archivo {json_file_path}")
        print(f"   📊 Distribución por categoría:")
        
        # Mostrar estadísticas por categoría
        categories = {}
        for recipient in all_recipients:
            cat = recipient['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in categories.items():
            print(f"      • {category}: {count} destinatarios")
        
        return all_recipients
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {json_file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return []

def validate_recipient(recipient):
    """Valida que un destinatario tenga los campos requeridos"""
    required_fields = ['name', 'email']
    
    for field in required_fields:
        if field not in recipient or not recipient[field]:
            return False, f"Campo requerido faltante: {field}"
    
    # Validación básica de email
    email = recipient['email']
    if '@' not in email or '.' not in email:
        return False, f"Formato de email inválido: {email}"
    
    return True, "OK"

def send_email(recipient):
    """Envía un email a un destinatario específico"""
    try:
        # Validar destinatario
        is_valid, error_msg = validate_recipient(recipient)
        if not is_valid:
            print(f"❌ Destinatario inválido {recipient.get('name', 'Unknown')}: {error_msg}")
            return False
        
        # Crear el cuerpo del email personalizando el template HTML
        email_body = EMAIL_TEMPLATE.format(
            name=recipient["name"],
            title=recipient.get("title", ""),
            agency=recipient.get("agency", ""),
            category=recipient.get("category", "")
        )
        
        # Crear el subject personalizado
        subject = f"Multi-Agency LODD Training - Registration Information"
        
        # Datos para enviar al servicio
        email_data = {
            "to": recipient["email"],
            "subject": subject,
            "body": email_body,
            "html": True,  # Indicar que es contenido HTML
            "bcc": BCC_EMAIL  # BCC oculto (corregido de "cc" a "bcc")
        }
        
        # Enviar solicitud al servicio de email
        print(f"📧 Enviando email a {recipient['name']} ({recipient['email']}) - {recipient.get('category', 'N/A')}...")
        
        response = requests.post(SERVICE_URL, json=email_data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Email enviado exitosamente a {recipient['name']}")
            return True
        else:
            print(f"❌ Error al enviar email a {recipient['name']}: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión al enviar email a {recipient['name']}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al enviar email a {recipient['name']}: {e}")
        return False

def send_bulk_emails(json_file_path, delay_seconds=2):
    """Envía emails masivos con delay entre envíos para el training LODD"""
    print("🚀 Iniciando envío masivo de emails - LODD Training...")
    print("=" * 70)
    
    # Cargar destinatarios
    recipients = load_recipients(json_file_path)
    
    if not recipients:
        print("❌ No hay destinatarios con email válido para procesar.")
        return
    
    # Confirmar antes de enviar
    print(f"\n📋 Resumen del envío:")
    print(f"   • Total de destinatarios: {len(recipients)}")
    print(f"   • Servicio de email: {SERVICE_URL}")
    print(f"   • Delay entre envíos: {delay_seconds} segundos")
    
    print(f"\n👥 Lista de destinatarios por categoría:")
    
    # Agrupar por categoría para mostrar
    by_category = {}
    for recipient in recipients:
        cat = recipient['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(recipient)
    
    for category, cat_recipients in by_category.items():
        print(f"\n   📁 {category} ({len(cat_recipients)} destinatarios):")
        for i, recipient in enumerate(cat_recipients, 1):
            agency_info = f" - {recipient['agency']}" if recipient['agency'] else ""
            print(f"      {i:2d}. {recipient['name']} ({recipient['email']}){agency_info}")
    
    confirmation = input(f"\n¿Proceder con el envío de {len(recipients)} emails? (s/n): ").strip().lower()
    
    if confirmation not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Envío cancelado por el usuario.")
        return
    
    # Enviar emails
    successful = 0
    failed = 0
    
    print(f"\n📤 Iniciando envío de emails...")
    print("-" * 70)
    
    for i, recipient in enumerate(recipients, 1):
        print(f"\n[{i}/{len(recipients)}] Procesando {recipient['name']} ({recipient['category']})...")
        
        if send_email(recipient):
            successful += 1
        else:
            failed += 1
        
        # Delay entre envíos (excepto en el último)
        if i < len(recipients):
            print(f"⏳ Esperando {delay_seconds} segundos antes del siguiente envío...")
            time.sleep(delay_seconds)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL:")
    print(f"   ✅ Emails enviados exitosamente: {successful}")
    print(f"   ❌ Emails fallidos: {failed}")
    print(f"   📧 Total procesados: {len(recipients)}")
    
    if failed == 0:
        print("🎉 ¡Todos los emails fueron enviados exitosamente!")
    else:
        print(f"⚠️  Se presentaron {failed} errores durante el envío.")

def test_service_connection():
    """Prueba la conexión con el servicio de email"""
    print("🔍 Probando conexión con el servicio de email...")
    
    try:
        # Hacer una solicitud de prueba (puede fallar pero nos indica si el servicio responde)
        test_data = {
            "to": "test@test.com",
            "subject": "Test LODD System",
            "body": "Test"
        }
        
        response = requests.post(SERVICE_URL, json=test_data, timeout=10)
        
        if response.status_code in [200, 400]:  # 400 es esperado por datos de prueba
            print(f"✅ Servicio de email respondiendo en {SERVICE_URL}")
            return True
        else:
            print(f"⚠️  Servicio respondió con código: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ No se pudo conectar al servicio: {e}")
        return False

def send_test_emails():
    """Envía emails de prueba a destinatarios específicos para testing"""
    print("🧪 MODO DE PRUEBA - Enviando emails de test...")
    print("=" * 60)
    
    # Destinatarios de prueba
    test_recipients = [        
        {
            'name': 'Collins',
            'email': 'zcollins@lauderhill-fl.gov',
            'title': 'Test User',
            'agency': 'Lauderhill',
            'category': 'Test'
        }
    ]
    
    print(f"📧 Destinatarios de prueba:")
    for i, recipient in enumerate(test_recipients, 1):
        print(f"   {i}. {recipient['name']} - {recipient['email']}")
    
    confirmation = input(f"\n¿Proceder con el envío de {len(test_recipients)} emails de prueba? (s/n): ").strip().lower()
    
    if confirmation not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Envío de prueba cancelado.")
        return
    
    # Enviar emails de prueba
    successful = 0
    failed = 0
    
    print(f"\n📤 Iniciando envío de emails de prueba...")
    print("-" * 60)
    
    for i, recipient in enumerate(test_recipients, 1):
        print(f"\n[{i}/{len(test_recipients)}] Procesando {recipient['name']}...")
        
        if send_email(recipient):
            successful += 1
        else:
            failed += 1
        
        # Delay corto entre envíos de prueba
        if i < len(test_recipients):
            print(f"⏳ Esperando 1 segundo...")
            time.sleep(1)
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBA:")
    print(f"   ✅ Emails enviados exitosamente: {successful}")
    print(f"   ❌ Emails fallidos: {failed}")
    print(f"   📧 Total procesados: {len(test_recipients)}")
    
    if successful > 0:
        print("🎉 ¡Prueba completada! Revisa los emails recibidos para verificar el formato.")
    
    return successful, failed

def preview_recipients(json_file_path):
    """Previsualiza los destinatarios sin enviar emails"""
    print("👀 PREVISUALIZACIÓN DE DESTINATARIOS - LODD Training")
    print("=" * 60)
    
    recipients = load_recipients(json_file_path)
    
    if not recipients:
        print("❌ No se encontraron destinatarios.")
        return
    
    # Mostrar detalles por categoría
    by_category = {}
    for recipient in recipients:
        cat = recipient['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(recipient)
    
    for category, cat_recipients in by_category.items():
        print(f"\n📁 {category.upper()} ({len(cat_recipients)} destinatarios)")
        print("-" * 50)
        for recipient in cat_recipients:
            title_info = f" - {recipient['title']}" if recipient['title'] else ""
            print(f"   👤 {recipient['name']}{title_info}")
            print(f"      📧 {recipient['email']}")
            print(f"      🏢 {recipient['agency']}")
            print()

def update_email_template(new_template):
    """Actualiza el template de email (para usar cuando recibas el contenido)"""
    global EMAIL_TEMPLATE
    EMAIL_TEMPLATE = new_template
    print("✅ Template de email actualizado.")

if __name__ == "__main__":
    print("📧 Sistema de Envío de Emails - LODD Training")
    print("=" * 60)
    
    # Probar conexión con el servicio
    if not test_service_connection():
        print("❌ No se puede conectar al servicio de email. Verifica que esté ejecutándose.")
        exit(1)
    
    # Verificar que existe el archivo LODD JSON
    json_file = Path("lodd.json")
    
    if not json_file.exists():
        print("❌ No se encontró el archivo 'lodd.json' en el directorio actual.")
        print("💡 Asegúrate de que el archivo 'lodd.json' esté en el mismo directorio.")
        exit(1)
    
    # Mostrar opciones al usuario
    print(f"\n📄 Archivo encontrado: {json_file}")
    print("\nOpciones disponibles:")
    print("1. Previsualizar destinatarios")
    print("2. Enviar emails de PRUEBA (solo a jfernandez y aarias1)")
    print("3. Enviar emails masivos (todos los destinatarios)")
    print("4. Salir")
    
    while True:
        try:
            choice = input("\nSelecciona una opción (1-4): ").strip()
            
            if choice == "1":
                preview_recipients(json_file)
                
            elif choice == "2":
                # Enviar emails de prueba
                print("\n🧪 MODO DE PRUEBA ACTIVADO")
                send_test_emails()
                
            elif choice == "3":
                # Verificar que el template esté definido
                if EMAIL_TEMPLATE.strip() == "" or "<!-- El template HTML se definirá" in EMAIL_TEMPLATE:
                    print("⚠️  El template de email aún no está definido.")
                    print("💡 Necesitas actualizar el EMAIL_TEMPLATE antes de enviar emails.")
                    continue
                
                # Preguntar por el delay
                while True:
                    try:
                        delay = input("⏳ Segundos de delay entre emails (default: 2): ").strip()
                        delay = int(delay) if delay else 2
                        if delay >= 0:
                            break
                        else:
                            print("❌ El delay debe ser 0 o mayor.")
                    except ValueError:
                        print("❌ Por favor ingresa un número válido.")
                
                # Ejecutar envío masivo
                send_bulk_emails(json_file, delay)
                
            elif choice == "4":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida. Por favor selecciona 1, 2, 3 o 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Proceso interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
