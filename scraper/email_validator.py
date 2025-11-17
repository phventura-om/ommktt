import dns.resolver
import smtplib

def validar_email(email):
    try:
        dominio = email.split("@")[1]

        # Verifica MX
        registros_mx = dns.resolver.resolve(dominio, 'MX')
        if not registros_mx:
            return {"email_valido": False, "motivo": "Sem MX"}

        servidor_mx = str(registros_mx[0].exchange)

        # Teste SMTP (VRFY)
        server = smtplib.SMTP(timeout=5)
        server.connect(servidor_mx)
        code, message = server.helo()

        if code != 250:
            return {"email_valido": False, "motivo": "HELO falhou"}

        server.quit()
        return {"email_valido": True, "motivo": "MX + SMTP OK"}

    except Exception as e:
        return {"email_valido": False, "motivo": str(e)}
