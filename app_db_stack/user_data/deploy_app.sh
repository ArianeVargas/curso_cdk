#!/bin/bash -xe

# Actualiza los paquetes del sistema
sudo yum update -y

# Instala Apache HTTP Server, PHP y cliente MySQL
sudo yum install -y httpd php mysql

# Habilita Apache para iniciar automáticamente en el arranque
sudo systemctl enable httpd

# Inicia el servicio Apache
sudo systemctl start httpd

# Instala cliente MySQL (versión 5.7) y curl
sudo yum install -y mysql57 curl

# Verifica conectividad a GitHub (usado como prueba de red)
curl "https://github.com/ArianeVargas"

# Comentario: Instrucción para conectar a una base de datos RDS manualmente:
# mysql -u {User_name} -p -h {RDS_End_Point} {DB_NAME}
