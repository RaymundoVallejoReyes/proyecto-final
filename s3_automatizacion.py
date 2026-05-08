import boto3
from datetime import datetime

REGION = "us-east-1"
BUCKET_NAME = "devops-bucket-505331880455"


def crear_archivo_prueba():
    nombre_archivo = "archivo_prueba.txt"

    contenido = (
        "Archivo de prueba para automatizacion S3.\n"
        f"Fecha de creacion: {datetime.now()}\n"
        "Proyecto DevOps AWS.\n"
    )

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    print(f"Archivo local creado: {nombre_archivo}")
    return nombre_archivo


def subir_archivo_s3(s3_client, archivo_local):
    key_s3 = f"pruebas/{archivo_local}"

    s3_client.upload_file(archivo_local, BUCKET_NAME, key_s3)

    print(f"Archivo subido a S3: s3://{BUCKET_NAME}/{key_s3}")


def listar_objetos_s3(s3_client):
    print(f"\nObjetos dentro del bucket: {BUCKET_NAME}")

    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

    if "Contents" not in response:
        print("El bucket no contiene objetos.")
        return

    for objeto in response["Contents"]:
        nombre = objeto["Key"]
        tamano = objeto["Size"]
        fecha = objeto["LastModified"]

        print("-----------------------------------")
        print(f"Nombre: {nombre}")
        print(f"Tamaño: {tamano} bytes")
        print(f"Última modificación: {fecha}")


def main():
    print("Iniciando automatizacion de S3 con boto3...")

    s3_client = boto3.client("s3", region_name=REGION)

    archivo = crear_archivo_prueba()
    subir_archivo_s3(s3_client, archivo)
    listar_objetos_s3(s3_client)

    print("\nProceso S3 finalizado correctamente.")


if __name__ == "__main__":
    main()
