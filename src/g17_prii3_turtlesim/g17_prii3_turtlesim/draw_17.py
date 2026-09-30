"""Nodo ROS 2 que dibuja automáticamente el número 17 en turtlesim."""

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Empty, Trigger
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


class Draw17(Node):
    """Controla la tortuga y expone servicios para pausar y reiniciar."""

    def __init__(self):
        """Inicializa las comunicaciones ROS y la secuencia de dibujo."""
        super().__init__('draw_17')

        # Publisher:
        # Envía velocidades a turtle1
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # Subscriber:
        # Recibe la posición actual de turtle1
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Cliente del servicio set_pen
        # Nos permite levantar y bajar el lápiz
        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        # Cliente para borrar el dibujo y devolver turtlesim a su estado inicial.
        self.reset_client = self.create_client(
            Empty,
            '/reset'
        )

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Esperando al servicio /turtle1/set_pen...'
            )

        while not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio /reset...')

        # Aquí guardaremos la posición actual de la tortuga
        self.pose = None

        # Lista de acciones para dibujar "17"
        self.actions = [
            ('pen', False),       # Levantar lápiz
            ('move', 3.0, 8.0),  # Ir al inicio del 1

            ('pen', True),        # Bajar lápiz
            ('move', 3.0, 3.0),  # Dibujar el 1

            ('pen', False),       # Levantar lápiz
            ('move', 5.0, 8.0),  # Ir al inicio del 7

            ('pen', True),        # Bajar lápiz
            ('move', 8.0, 8.0),  # Parte superior del 7
            ('move', 5.5, 3.0),  # Diagonal del 7

            ('pen', False),       # Levantar lápiz al terminar
        ]

        # Acción que estamos ejecutando
        self.current_action = 0

        # Sirve para saber si estamos esperando
        # a que termine una llamada a set_pen
        self.pen_future = None
        self.reset_future = None

        # El servicio de pausa no pierde la acción que se estaba ejecutando.
        self.paused = False

        # Servicios públicos del nodo.
        self.stop_service = self.create_service(
            Trigger,
            '/stop_drawing',
            self.stop_drawing_callback
        )
        self.continue_service = self.create_service(
            Trigger,
            '/continue_drawing',
            self.continue_drawing_callback
        )
        self.restart_service = self.create_service(
            Trigger,
            '/restart_drawing',
            self.restart_drawing_callback
        )

        # El controlador se ejecutará 10 veces por segundo
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.get_logger().info('Nodo draw_17 iniciado')

    def pose_callback(self, msg):
        """Actualiza la posición actual de turtle1."""
        self.pose = msg

    def set_pen(self, enabled):
        """Activa o desactiva el lápiz de turtle1."""
        request = SetPen.Request()

        # Color del trazo
        request.r = 0
        request.g = 0
        request.b = 255

        # Grosor
        request.width = 5

        # off = 0 -> dibuja
        # off = 1 -> no dibuja
        request.off = 0 if enabled else 1

        self.pen_future = self.pen_client.call_async(request)

    def stop_turtle(self):
        """Publica velocidad cero para detener la tortuga."""
        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.cmd_vel_pub.publish(msg)

    def stop_drawing_callback(self, request, response):
        """Pausa el dibujo manteniendo la acción actual."""
        del request
        self.paused = True
        self.stop_turtle()
        response.success = True
        response.message = 'Dibujo pausado'
        self.get_logger().info(response.message)
        return response

    def continue_drawing_callback(self, request, response):
        """Reanuda el dibujo desde el punto en que se detuvo."""
        del request

        if self.reset_future is not None:
            response.success = False
            response.message = 'El reinicio está en curso'
            return response

        if self.current_action >= len(self.actions):
            response.success = False
            response.message = 'El dibujo ya ha terminado; usa /restart_drawing'
            return response

        self.paused = False
        response.success = True
        response.message = 'Dibujo reanudado'
        self.get_logger().info(response.message)
        return response

    def restart_drawing_callback(self, request, response):
        """Borra turtlesim y vuelve a iniciar la secuencia completa."""
        del request

        if self.reset_future is not None:
            response.success = False
            response.message = 'Ya hay un reinicio en curso'
            return response

        self.paused = True
        self.pen_future = None
        self.stop_turtle()
        self.reset_future = self.reset_client.call_async(Empty.Request())

        response.success = True
        response.message = 'Reinicio solicitado'
        self.get_logger().info(response.message)
        return response

    def move_to(self, target_x, target_y):
        """
        Mueve la tortuga hacia una posición objetivo.

        Devuelve True cuando hemos llegado.
        """
        # Distancia entre la tortuga y el objetivo
        distance = math.sqrt(
            (target_x - self.pose.x) ** 2 +
            (target_y - self.pose.y) ** 2
        )

        # Ángulo que debería tener la tortuga
        target_angle = math.atan2(
            target_y - self.pose.y,
            target_x - self.pose.x
        )

        # Diferencia entre dónde mira y dónde debería mirar
        angle_error = target_angle - self.pose.theta

        # Normalizar el ángulo entre -pi y pi
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )

        # Si estamos suficientemente cerca,
        # consideramos que hemos llegado
        if distance < 0.1:
            self.stop_turtle()
            return True

        msg = Twist()

        # Si todavía estamos mirando muy lejos
        # de la dirección correcta, giramos primero
        if abs(angle_error) > 0.15:
            msg.linear.x = 0.0
            msg.angular.z = 2.0 * angle_error

        # Cuando ya miramos hacia el objetivo,
        # avanzamos mientras corregimos ligeramente
        else:
            msg.linear.x = min(1.5, 1.5 * distance)
            msg.angular.z = 2.0 * angle_error

        self.cmd_vel_pub.publish(msg)

        return False

    def control_loop(self):
        """
        Este es el cerebro principal del programa.

        Se ejecuta cada 0.1 segundos y decide
        qué tiene que hacer la tortuga.
        """
        # Todavía no conocemos la posición
        if self.pose is None:
            return

        # Durante el reinicio no debe enviarse ningún movimiento. Esperamos a
        # que turtlesim haya borrado el lienzo y repuesto la pose inicial.
        if self.reset_future is not None:
            self.stop_turtle()

            if self.reset_future.done():
                try:
                    self.reset_future.result()
                except Exception as error:
                    self.get_logger().error(
                        f'No se pudo reiniciar turtlesim: {error}'
                    )
                    self.paused = True
                else:
                    self.current_action = 0
                    self.paused = False
                    self.get_logger().info('Dibujo reiniciado')

                self.reset_future = None

            return

        # Detener no reinicia la secuencia: simplemente deja de publicar
        # velocidades hasta recibir /continue_drawing.
        if self.paused:
            self.stop_turtle()
            return

        # Hemos terminado todas las acciones
        if self.current_action >= len(self.actions):
            self.stop_turtle()
            return

        # Si hemos llamado a set_pen,
        # esperamos a que termine el servicio
        if self.pen_future is not None:

            self.stop_turtle()

            if self.pen_future.done():
                self.pen_future = None
                self.current_action += 1

            return

        action = self.actions[self.current_action]

        # ------------------------------
        # ACCIÓN: cambiar estado del lápiz
        # ------------------------------

        if action[0] == 'pen':

            enabled = action[1]

            if enabled:
                self.get_logger().info('Bajando lápiz')
            else:
                self.get_logger().info('Levantando lápiz')

            self.set_pen(enabled)

        # ------------------------------
        # ACCIÓN: moverse a un punto
        # ------------------------------

        elif action[0] == 'move':

            target_x = action[1]
            target_y = action[2]

            arrived = self.move_to(
                target_x,
                target_y
            )

            if arrived:
                self.get_logger().info(
                    f'Objetivo alcanzado: ({target_x}, {target_y})'
                )

                self.current_action += 1


def main(args=None):
    """Inicializa y ejecuta el nodo de dibujo."""
    # Inicializar ROS 2
    rclpy.init(args=args)

    # Crear nuestro nodo
    node = Draw17()

    try:
        # Mantener el nodo ejecutándose
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    # Detener la tortuga antes de cerrar
    node.stop_turtle()

    # Destruir el nodo
    node.destroy_node()

    # Cerrar ROS 2
    rclpy.shutdown()


if __name__ == '__main__':
    main()
