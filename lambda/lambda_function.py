import json
import random


def lambda_handler(event, context):
    mensajes = [
        "Pipeline DevOps ejecutado correctamente.",
        "Microservicio activo en AWS Lambda.",
        "Automatización aplicada en la infraestructura.",
        "Monitoreo y despliegue integrados en AWS.",
        "Soluciones Tecnológicas del Futuro mejora su entrega continua."
    ]

    respuesta = {
        "mensaje": random.choice(mensajes),
        "servicio": "microservicio-devops"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(respuesta)
    }
