from PyQt6 import QtWidgets, QtGui, QtCore
from src.logica.gestor_passkeeper import PassKeeper

import random
import string

class PassKeeperApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.keeper = PassKeeper()
        self.init_ui()

    def init_ui(self):
        # Configuración de la ventana principal
        self.setWindowTitle("PassKeeper - Gestor de Contraseñas")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #F5F5F5;")

        # Etiqueta del título
        self.title_label = QtWidgets.QLabel("Gestor de Contraseñas - PassKeeper", self)
        self.title_label.setGeometry(0, 10, 800, 50)
        self.title_label.setStyleSheet("color: #2C3E50; font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Tabla de contraseñas
        self.password_table = QtWidgets.QTableWidget(self)
        self.password_table.setGeometry(50, 100, 700, 250)
        self.password_table.setColumnCount(3)
        self.password_table.setHorizontalHeaderLabels(["Servicio", "Usuario", "Contraseña"])
        self.password_table.horizontalHeader().setStretchLastSection(True)

        # Campos de entrada para Servicio, Usuario y Contraseña
        self.service_input = QtWidgets.QLineEdit(self)
        self.service_input.setGeometry(50, 380, 200, 30)
        self.service_input.setPlaceholderText("Servicio")
        self.service_input.setStyleSheet("background-color: white; border: 1px solid #BDC3C7; border-radius: 5px;")

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(300, 380, 200, 30)
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setStyleSheet("background-color: white; border: 1px solid #BDC3C7; border-radius: 5px;")

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(550, 380, 200, 30)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("background-color: white; border: 1px solid #BDC3C7; border-radius: 5px;")

        # Botones para Añadir, Editar y Eliminar
        self.add_button = QtWidgets.QPushButton("Añadir", self)
        self.add_button.setGeometry(150, 470, 150, 40)
        self.add_button.setStyleSheet("background-color: #2C3E50; color: white; font-weight: bold; border-radius: 10px;")
        self.add_button.clicked.connect(self.add_password)

        self.edit_button = QtWidgets.QPushButton("Editar", self)
        self.edit_button.setGeometry(325, 470, 150, 40)
        self.edit_button.setStyleSheet("background-color: #2C3E50; color: white; font-weight: bold; border-radius: 10px;")
        self.edit_button.clicked.connect(self.edit_password)

        self.delete_button = QtWidgets.QPushButton("Eliminar", self)
        self.delete_button.setGeometry(500, 470, 150, 40)
        self.delete_button.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold; border-radius: 10px;")
        self.delete_button.clicked.connect(self.confirm_delete)

        # Actualizar la tabla con datos al inicio
        self.update_password_table()

        # Botón para generar una contraseña aleatoria
        self.generate_button = QtWidgets.QPushButton("Generar Contraseña", self)
        self.generate_button.setGeometry(550, 420, 200, 30)
        self.generate_button.setStyleSheet(
            "background-color: #3498DB; color: white; font-weight: bold; border-radius: 10px;")
        self.generate_button.clicked.connect(self.generate_password)

    def add_password(self):
        """Añade una nueva contraseña, evitando duplicados de servicio y usuario."""
        service = self.service_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if service and username and password:
            # Verificar si el servicio y usuario ya existen
            for row_idx in range(self.password_table.rowCount()):
                existing_service = self.password_table.item(row_idx, 0).text()
                existing_username = self.password_table.item(row_idx, 1).text()
                if service == existing_service and username == existing_username:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Advertencia",
                        f"El servicio '{service}' y el usuario '{username}' ya existen en la fila {row_idx + 1}."
                    )
                    return

            self.keeper.add_password(service, username, password)
            self.update_password_table()
            self.clear_inputs()

    def edit_password(self):
        """Edita los datos seleccionados en la tabla."""
        selected_row = self.password_table.currentRow()
        if selected_row != -1:
            service = self.service_input.text()
            username = self.username_input.text()
            password = self.password_input.text()

            # Validar campos y actualizar
            if service and username and password:
                old_service = self.password_table.item(selected_row, 0).text()
                self.keeper.delete_password(old_service)
                self.keeper.add_password(service, username, password)
                self.update_password_table()
                self.clear_inputs()

    def confirm_delete(self):
        """Muestra una ventana de confirmación antes de eliminar."""
        selected_row = self.password_table.currentRow()
        if selected_row != -1:
            service = self.password_table.item(selected_row, 0).text()

            # Confirmación
            reply = QtWidgets.QMessageBox.question(
                self, "Confirmar Eliminación", f"¿Estás seguro de eliminar la contraseña para {service}?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.delete_password()

    def delete_password(self):
        """Elimina la contraseña seleccionada."""
        selected_row = self.password_table.currentRow()
        if selected_row != -1:
            service = self.password_table.item(selected_row, 0).text()
            self.keeper.delete_password(service)
            self.update_password_table()

    def update_password_table(self):
        """Actualiza la tabla con las contraseñas almacenadas."""
        passwords = self.keeper.view_passwords()
        self.password_table.setRowCount(len(passwords))
        for row_idx, (service, username, password) in enumerate(passwords):
            service_item = QtWidgets.QTableWidgetItem(service)
            username_item = QtWidgets.QTableWidgetItem(username)
            password_item = QtWidgets.QTableWidgetItem(password)

            # Hacer las celdas no editables
            service_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            username_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            password_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)

            self.password_table.setItem(row_idx, 0, service_item)
            self.password_table.setItem(row_idx, 1, username_item)
            self.password_table.setItem(row_idx, 2, password_item)

    def clear_inputs(self):
        """Limpia los campos de entrada."""
        self.service_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def generate_password(self):
        """Genera una contraseña aleatoria y la muestra en el campo de entrada."""
        length = 12
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        generated_password = ''.join(random.choice(characters) for _ in range(length))
        self.password_input.setText(generated_password)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = PassKeeperApp()
    window.show()
    sys.exit(app.exec())
