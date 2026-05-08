import time
import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
TABLE_NAME = "devops-tabla"


def crear_tabla(dynamodb):
    print(f"Creando tabla DynamoDB: {TABLE_NAME}")

    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        print("Esperando a que la tabla esté activa...")
        table.wait_until_exists()
        print("Tabla creada correctamente.")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ResourceInUseException":
            print("La tabla ya existe. Continuando con las operaciones...")
            table = dynamodb.Table(TABLE_NAME)
        else:
            print(f"Error al crear la tabla: {e}")
            raise

    return dynamodb.Table(TABLE_NAME)


def insertar_registro(table):
    print("Insertando registro...")

    table.put_item(
        Item={
            "id": "1",
            "nombre": "registro-devops",
            "status": "creado"
        }
    )

    print("Registro insertado correctamente.")


def actualizar_registro(table):
    print("Actualizando registro...")

    table.update_item(
        Key={
            "id": "1"
        },
        UpdateExpression="SET #st = :nuevo_status",
        ExpressionAttributeNames={
            "#st": "status"
        },
        ExpressionAttributeValues={
            ":nuevo_status": "actualizado"
        }
    )

    print("Registro actualizado correctamente.")


def eliminar_registro(table):
    print("Eliminando registro...")

    table.delete_item(
        Key={
            "id": "1"
        }
    )

    print("Registro eliminado correctamente.")


def main():
    print("Iniciando operaciones con DynamoDB usando boto3...")

    dynamodb = boto3.resource("dynamodb", region_name=REGION)

    table = crear_tabla(dynamodb)

    insertar_registro(table)
    actualizar_registro(table)
    eliminar_registro(table)

    print("Operaciones DynamoDB finalizadas correctamente.")


if __name__ == "__main__":
    main()
