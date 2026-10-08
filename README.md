# Sprint 1 PRII3 - Grupo 17

Usamos ROS 2 y turtlesim para dibujar el número 17. El dibujo se puede parar, reanudar y reiniciar.

## Descargar el proyecto

Comprueba que tienes Git:

    git --version

Si no lo tienes, en Ubuntu puedes instalarlo con:

    sudo apt update
    sudo apt install git

Para descargarlo en tu carpeta Projects:

    mkdir -p ~/Projects
    cd ~/Projects
    git clone https://github.com/alejandrossalido/Sprint-1-PRII.git
    cd Sprint-1-PRII

Sprint-1-PRII es el workspace y ya contiene src y este README. En mi copia original se llama g17_PRII3_ws. Si usas Distrobox, puedes descargarlo antes de entrar en la caja.

Para actualizar una copia que ya tienes:

    cd ~/Projects/Sprint-1-PRII
    git pull --ff-only

## 1. Compilar y ejecutar en Ubuntu

Necesitas tener:

- Ubuntu 22.04 con escritorio.
- ROS 2 Humble y Python 3.
- colcon y turtlesim.

Para instalar ROS, sigue la [guía de Humble en Ubuntu](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

Con ROS instalado y sus repositorios configurados, instala las herramientas que falten:

    sudo apt update
    sudo apt install python3-colcon-common-extensions ros-humble-turtlesim

Entra en la carpeta descargada:

    cd ~/Projects/Sprint-1-PRII

Compila y arranca el proyecto:

    source /opt/ros/humble/setup.bash
    colcon build --symlink-install --packages-select g17_prii3_turtlesim
    source install/setup.bash
    ros2 launch g17_prii3_turtlesim draw_17.launch.py

El launch abre el simulador y nuestro nodo juntos.

## 2. Compilar y ejecutar con Distrobox en Omarchy

En mi ordenador uso Omarchy con Distrobox y una caja llamada ros-humble. Necesitas Distrobox con Docker o Podman, y la caja con Ubuntu 22.04 y las herramientas del apartado anterior instaladas.

Desde la terminal normal, entra en la caja:

    distrobox enter --clean-path --name ros-humble

--clean-path hace que use el Python de la caja. Cambia ros-humble si tu caja tiene otro nombre.

Dentro de la caja, entra en la copia descargada:

    cd ~/Projects/Sprint-1-PRII

O en mi copia original. Usa solo uno de los dos comandos cd:

    cd "/home/alejandrossalido/Projects/01_Universidad/3º_de_Carrera/Proyecto_RII_3/Sprint1/g17_PRII3_ws"

Después compila y arranca el proyecto:

    source /opt/ros/humble/setup.bash
    colcon build --symlink-install --packages-select g17_prii3_turtlesim
    source install/setup.bash
    ros2 launch g17_prii3_turtlesim draw_17.launch.py

## Pausar, continuar y reiniciar el dibujo

Deja el proyecto abierto y abre otra terminal. Si usas Distrobox, entra también en la caja:

    distrobox enter --clean-path --name ros-humble

En Ubuntu directamente, sáltate ese paso. Entra en la carpeta del proyecto y carga el entorno:

    cd ~/Projects/Sprint-1-PRII
    source /opt/ros/humble/setup.bash
    source install/setup.bash

Si usas mi copia original, cambia el cd por la ruta del apartado de Distrobox. Ejecuta cada servicio por separado.

Parar:

    ros2 service call /stop_drawing std_srvs/srv/Trigger "{}"

Reanudar desde donde se quedó:

    ros2 service call /continue_drawing std_srvs/srv/Trigger "{}"

Borrar y empezar de nuevo:

    ros2 service call /restart_drawing std_srvs/srv/Trigger "{}"

La respuesta debe mostrar success=True. Si el dibujo ya terminó, usa restart_drawing. Para cerrar el programa, pulsa Ctrl+C en la primera terminal.

## Qué archivos usamos

Dentro de src/g17_prii3_turtlesim:

- g17_prii3_turtlesim/draw_17.py: movimiento, lápiz y servicios.
- launch/draw_17.launch.py: arranca el simulador y el nodo.
- setup.py y setup.cfg: instalación del paquete.
- package.xml: información y dependencias.

## Comprobaciones rápidas

Desde la segunda terminal, con el entorno cargado:

    ros2 node list
    ros2 topic list
    ros2 service list

Deberían aparecer /draw_17 y /turtlesim. Las velocidades se envían por /turtle1/cmd_vel y la posición se recibe por /turtle1/pose.

Si no has cambiado el código, puedes saltarte colcon build. Los comandos source se repiten en cada terminal nueva.
