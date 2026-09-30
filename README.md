# Proyecto RII 3 - Grupo 17

Nodo ROS 2 que controla `turtlesim` para dibujar automáticamente el número 17.

## Requisitos

- Ubuntu 22.04
- ROS 2 Humble
- Python 3

## Compilación

Desde la raíz del workspace:

```bash
colcon build --symlink-install --packages-select g17_prii3_turtlesim
source install/setup.bash
```

## Ejecución

El launch inicia `turtlesim` y el nodo de dibujo en un único comando:

```bash
ros2 launch g17_prii3_turtlesim draw_17.launch.py
```

## Servicios

En otra terminal, carga el mismo workspace antes de llamar a los servicios:

```bash
source install/setup.bash
```

Pausar el dibujo:

```bash
ros2 service call /stop_drawing std_srvs/srv/Trigger "{}"
```

Reanudarlo desde el mismo punto:

```bash
ros2 service call /continue_drawing std_srvs/srv/Trigger "{}"
```

Borrar el lienzo y comenzar de nuevo:

```bash
ros2 service call /restart_drawing std_srvs/srv/Trigger "{}"
```

## Comprobaciones útiles

```bash
ros2 node list
ros2 node info /draw_17
ros2 service list
```
