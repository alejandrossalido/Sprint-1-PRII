# Proyecto PRII3 - Grupo 17

En este proyecto usamos ROS 2 y turtlesim para que una tortuga dibuje el número 17. Hemos hecho un nodo en Python que controla el movimiento y tres servicios para pausar, continuar y reiniciar el dibujo.

Dejamos dos formas de compilarlo y ejecutarlo: en Ubuntu directamente y con Distrobox, que es como lo tengo preparado en mi ordenador.

## 1. Compilar y ejecutar en Ubuntu

Necesitas tener:

- Ubuntu 22.04 con escritorio, para poder ver la ventana de turtlesim.
- ROS 2 Humble instalado. La opción Desktop incluye las herramientas habituales.
- Python 3, que ya viene con Ubuntu.
- colcon para compilar el paquete y turtlesim para el simulador.

Si todavía no tienes ROS 2, puedes seguir la [guía de instalación de Humble en Ubuntu](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

Una vez instalado ROS y configurados sus repositorios, instala estas herramientas si te faltan. Esto solo hace falta hacerlo una vez:

    sudo apt update
    sudo apt install python3-colcon-common-extensions ros-humble-turtlesim

Abre una terminal dentro de la carpeta g17_PRII3_ws. Es la que contiene src y este README, dentro de Sprint1. Ejecuta los comandos en este orden:

    source /opt/ros/humble/setup.bash
    colcon build --symlink-install --packages-select g17_prii3_turtlesim
    source install/setup.bash
    ros2 launch g17_prii3_turtlesim draw_17.launch.py

El primer comando carga ROS, el segundo compila y el tercero hace que ROS encuentre nuestro paquete. El último abre turtlesim y arranca el nodo que dibuja el 17.

## 2. Compilar y ejecutar con Distrobox en Omarchy

En mi ordenador uso Omarchy. Para trabajar con ROS tengo una caja de Distrobox llamada ros-humble, con Ubuntu 22.04 y ROS 2 Humble instalados dentro.

Para hacerlo de esta forma necesitas:

- Distrobox instalado en el ordenador, junto con Docker o Podman.
- Una caja con Ubuntu 22.04, ROS 2 Humble, Python 3, colcon y turtlesim.
- La carpeta del proyecto accesible desde la caja. En mi instalación está dentro de mi carpeta de usuario y se comparte con Distrobox.

Los siguientes pasos parten de que la caja ya está preparada. Si la acabas de crear, instala ROS dentro siguiendo la guía del apartado de Ubuntu y después instala colcon y turtlesim con los comandos de ese mismo apartado.

Desde una terminal normal del ordenador, entra en la caja:

    distrobox enter --clean-path --name ros-humble

Uso --clean-path para que se utilice el Python de Ubuntu dentro de la caja y no otro que tenga instalado en Omarchy. Si tu caja tiene otro nombre, cambia ros-humble por ese nombre.

Cuando ya estés dentro, ve a la carpeta del proyecto. Esta es la ruta de mi ordenador; en otro ordenador tendrás que poner la tuya:

    cd "/home/alejandrossalido/Projects/01_Universidad/3º_de_Carrera/Proyecto_RII_3/Sprint1/g17_PRII3_ws"

Después compila y arranca el proyecto:

    source /opt/ros/humble/setup.bash
    colcon build --symlink-install --packages-select g17_prii3_turtlesim
    source install/setup.bash
    ros2 launch g17_prii3_turtlesim draw_17.launch.py

Aunque el ordenador use Omarchy, estos comandos se ejecutan dentro del Ubuntu de Distrobox. La ventana de la tortuga aparece en el escritorio del ordenador.

## Pausar, continuar y reiniciar el dibujo

Deja abierta la terminal donde has lanzado el proyecto y abre una segunda. Si usas Distrobox, entra también en la caja desde esa nueva terminal:

    distrobox enter --clean-path --name ros-humble

En Ubuntu directamente puedes saltarte ese paso. En los dos casos, entra en la carpeta del proyecto y carga el entorno. Esta es la ruta de mi ordenador; cámbiala si tienes el proyecto en otra carpeta:

    cd "/home/alejandrossalido/Projects/01_Universidad/3º_de_Carrera/Proyecto_RII_3/Sprint1/g17_PRII3_ws"
    source /opt/ros/humble/setup.bash
    source install/setup.bash

Ahora puedes usar los tres comandos siguientes, uno cada vez, desde esta segunda terminal.

Para parar la tortuga mientras está dibujando:

    ros2 service call /stop_drawing std_srvs/srv/Trigger "{}"

La tortuga se queda quieta y conserva el punto del dibujo. La respuesta debe mostrar success=True y el mensaje "Dibujo pausado".

Para continuar desde donde se quedó:

    ros2 service call /continue_drawing std_srvs/srv/Trigger "{}"

La tortuga vuelve a moverse y sigue el dibujo. La respuesta debe mostrar success=True y "Dibujo reanudado".

Para borrar el dibujo y empezar otra vez:

    ros2 service call /restart_drawing std_srvs/srv/Trigger "{}"

Se borra el lienzo, la tortuga vuelve a la posición inicial y empieza de nuevo. La respuesta debe mostrar success=True y "Reinicio solicitado".

Para enseñarlo en clase, pausa mientras se está moviendo, comprueba que se queda quieta, reanúdala y después reiníciala. Si el dibujo ya terminó, primero usa restart_drawing: continue_drawing solo sirve para continuar un dibujo que todavía no ha acabado.

Para cerrar el proyecto, pulsa Ctrl+C en la primera terminal. El servicio stop_drawing solo pausa la tortuga; mantiene el programa abierto para poder reanudarla.

## Qué archivos usamos

Dentro de src/g17_prii3_turtlesim están los archivos principales:

- g17_prii3_turtlesim/draw_17.py: controla el movimiento, el lápiz y los servicios del dibujo.
- launch/draw_17.launch.py: arranca el simulador y nuestro nodo juntos.
- setup.py y setup.cfg: indican cómo instalar el paquete y ejecutar el nodo.
- package.xml: contiene la información del paquete y sus dependencias.

## Comprobaciones rápidas

Desde la segunda terminal, con el entorno ya cargado, puedes ver los nodos, los topics y los servicios:

    ros2 node list
    ros2 topic list
    ros2 service list

Deberían aparecer los nodos /draw_17 y /turtlesim. Nuestro nodo envía las velocidades por /turtle1/cmd_vel y recibe la posición de la tortuga por /turtle1/pose.

No hace falta abrir turtlesim por separado, porque el launch ya lo inicia. En las siguientes ejecuciones puedes saltarte colcon build si no has cambiado el código, pero sí debes volver a cargar el entorno en cada terminal nueva.
