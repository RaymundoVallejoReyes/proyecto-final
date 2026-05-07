import boto3
from datetime import datetime, timedelta, timezone


REGION = "us-east-1"


def listar_instancias_ec2():
    print("\n========== INSTANCIAS EC2 ==========")

    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        response = ec2.describe_instances()
        instancias_encontradas = False

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instancias_encontradas = True
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                state = instance["State"]["Name"]

                print(f"ID: {instance_id}")
                print(f"Tipo: {instance_type}")
                print(f"Estado: {state}")
                print("-----------------------------------")

        if not instancias_encontradas:
            print("No se encontraron instancias EC2.")

    except Exception as e:
        print(f"Error al listar instancias EC2: {e}")


def obtener_instancias_en_ejecucion():
    ec2 = boto3.client("ec2", region_name=REGION)
    instancias = []

    try:
        response = ec2.describe_instances(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": ["running"]
                }
            ]
        )

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instancias.append(instance["InstanceId"])

    except Exception as e:
        print(f"Error al obtener instancias en ejecución: {e}")

    return instancias


def reporte_cpu_cloudwatch():
    print("\n========== REPORTE CPU CLOUDWATCH ==========")

    cloudwatch = boto3.client("cloudwatch", region_name=REGION)
    instancias = obtener_instancias_en_ejecucion()

    if not instancias:
        print("No hay instancias EC2 en ejecución para consultar métricas de CPU.")
        return

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)

    for instance_id in instancias:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[
                    {
                        "Name": "InstanceId",
                        "Value": instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=["Average", "Maximum"],
                Unit="Percent"
            )

            datapoints = response["Datapoints"]

            print(f"\nInstancia: {instance_id}")

            if not datapoints:
                print("No hay métricas de CPU disponibles en las últimas 24 horas.")
            else:
                datapoints_ordenados = sorted(datapoints, key=lambda x: x["Timestamp"])

                for point in datapoints_ordenados:
                    timestamp = point["Timestamp"]
                    average = point.get("Average", 0)
                    maximum = point.get("Maximum", 0)

                    print(f"Fecha: {timestamp}")
                    print(f"CPU Promedio: {average:.2f}%")
                    print(f"CPU Máxima: {maximum:.2f}%")
                    print("-----------------------------------")

        except Exception as e:
            print(f"Error al obtener métricas de CPU para {instance_id}: {e}")


def listar_buckets_s3():
    print("\n========== BUCKETS S3 ==========")

    s3 = boto3.client("s3")

    try:
        response = s3.list_buckets()
        buckets = response.get("Buckets", [])

        if not buckets:
            print("No se encontraron buckets S3.")
            return

        for bucket in buckets:
            bucket_name = bucket["Name"]
            print(f"\nBucket: {bucket_name}")

            try:
                objetos = s3.list_objects_v2(Bucket=bucket_name)

                if "Contents" not in objetos:
                    print("Este bucket no tiene objetos.")
                else:
                    print("Objetos:")
                    for obj in objetos["Contents"]:
                        print(f"- {obj['Key']} | Tamaño: {obj['Size']} bytes")

            except Exception as e:
                print(f"No se pudieron listar objetos del bucket {bucket_name}: {e}")

    except Exception as e:
        print(f"Error al listar buckets S3: {e}")


def listar_auto_scaling_groups():
    print("\n========== AUTO SCALING GROUPS ==========")

    autoscaling = boto3.client("autoscaling", region_name=REGION)

    try:
        response = autoscaling.describe_auto_scaling_groups()
        grupos = response.get("AutoScalingGroups", [])

        if not grupos:
            print("No se encontraron grupos de Auto Scaling.")
            return

        for grupo in grupos:
            print(f"Nombre: {grupo['AutoScalingGroupName']}")
            print(f"Capacidad mínima: {grupo['MinSize']}")
            print(f"Capacidad máxima: {grupo['MaxSize']}")
            print(f"Capacidad deseada: {grupo['DesiredCapacity']}")
            print("-----------------------------------")

    except Exception as e:
        print(f"Error al listar grupos de Auto Scaling: {e}")


def main():
    print("Iniciando script de automatización con boto3...")
    print(f"Región configurada: {REGION}")

    listar_instancias_ec2()
    reporte_cpu_cloudwatch()
    listar_buckets_s3()
    listar_auto_scaling_groups()

    print("\nScript finalizado correctamente.")


if __name__ == "__main__":
    main()
