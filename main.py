"""
站点访问管理工具
简易的站点地址和端口配置管理器
"""
import sys
import json
import webbrowser
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QDialog, QLabel,
    QLineEdit, QComboBox, QMessageBox, QGroupBox, QSplitter,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QDateTimeEdit, QFrame, QMenu, QInputDialog
)
from PySide6.QtCore import Qt, QSize, QDateTime
from PySide6.QtGui import QIcon, QColor


MODERN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: "Microsoft YaHei UI", "Segoe UI", Arial;
    font-size: 10pt;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
}

QLineEdit, QComboBox, QTextEdit {
    border: 2px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px;
    background-color: white;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
    border: 2px solid #2196F3;
}

QListWidget, QTableWidget {
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
    outline: none;
}

QListWidget::item {
    padding: 10px;
    border-radius: 4px;
    margin: 2px;
}

QListWidget::item:selected {
    background-color: #2196F3;
    color: white;
}

QListWidget::item:hover {
    background-color: #E3F2FD;
}

QTableWidget {
    gridline-color: #E0E0E0;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #2196F3;
    color: white;
}

QHeaderView::section {
    background-color: #FAFAFA;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #E0E0E0;
    font-weight: 600;
}

QGroupBox {
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    background-color: white;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 8px;
    color: #424242;
}

QTabWidget::pane {
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
    top: -2px;
}

QTabBar::tab {
    background-color: #FAFAFA;
    border: 2px solid #E0E0E0;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 20px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 2px solid white;
}

QTabBar::tab:hover {
    background-color: #E3F2FD;
}

QLabel {
    color: #424242;
}

QDialog {
    background-color: #f5f5f5;
}
"""


class DeploymentDialog(QDialog):
    """部署记录添加对话框"""

    def __init__(self, parent=None, deployment_data=None):
        super().__init__(parent)
        self.deployment_data = deployment_data or {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("添加部署记录")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # 部署类型
        type_label = QLabel("部署类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["前端", "后端", "进程服务", "数据库", "其他"])
        current_type = self.deployment_data.get("type", "前端")
        self.type_combo.setCurrentText(current_type)
        layout.addWidget(type_label)
        layout.addWidget(self.type_combo)

        # 站点名称
        site_label = QLabel("站点名称:")
        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("例如: 工厂监控系统")
        self.site_input.setText(self.deployment_data.get("site_name", ""))
        layout.addWidget(site_label)
        layout.addWidget(self.site_input)

        # 版本号
        version_label = QLabel("版本号:")
        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("例如: v1.2.3")
        self.version_input.setText(self.deployment_data.get("version", ""))
        layout.addWidget(version_label)
        layout.addWidget(self.version_input)

        # 部署环境
        env_label = QLabel("部署环境:")
        self.env_combo = QComboBox()
        self.env_combo.addItems(["开发环境", "测试环境", "预发布环境", "生产环境"])
        current_env = self.deployment_data.get("environment", "开发环境")
        self.env_combo.setCurrentText(current_env)
        layout.addWidget(env_label)
        layout.addWidget(self.env_combo)

        # 部署状态
        status_label = QLabel("部署状态:")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["成功", "失败", "进行中", "回滚"])
        current_status = self.deployment_data.get("status", "成功")
        self.status_combo.setCurrentText(current_status)
        layout.addWidget(status_label)
        layout.addWidget(self.status_combo)

        # 部署时间
        time_label = QLabel("部署时间:")
        self.time_edit = QDateTimeEdit()
        self.time_edit.setCalendarPopup(True)
        self.time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        if "deploy_time" in self.deployment_data:
            dt = QDateTime.fromString(self.deployment_data["deploy_time"], "yyyy-MM-dd HH:mm:ss")
            self.time_edit.setDateTime(dt)
        else:
            self.time_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(time_label)
        layout.addWidget(self.time_edit)

        # 部署人员
        deployer_label = QLabel("部署人员:")
        self.deployer_input = QLineEdit()
        self.deployer_input.setPlaceholderText("例如: 张三")
        self.deployer_input.setText(self.deployment_data.get("deployer", ""))
        layout.addWidget(deployer_label)
        layout.addWidget(self.deployer_input)

        # 备注
        notes_label = QLabel("备注:")
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("部署说明、变更内容等...")
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setText(self.deployment_data.get("notes", ""))
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_input)

        # 按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_deployment_data(self):
        """获取部署数据"""
        return {
            "type": self.type_combo.currentText(),
            "site_name": self.site_input.text().strip(),
            "version": self.version_input.text().strip(),
            "environment": self.env_combo.currentText(),
            "status": self.status_combo.currentText(),
            "deploy_time": self.time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            "deployer": self.deployer_input.text().strip(),
            "notes": self.notes_input.toPlainText().strip()
        }


class SiteDialog(QDialog):
    """站点添加/编辑对话框"""

    def __init__(self, parent=None, site_data=None, groups=None):
        super().__init__(parent)
        self.site_data = site_data or {}
        self.groups = groups or ["默认分组"]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("添加/编辑站点")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # 站点名称
        name_label = QLabel("站点名称:")
        self.name_input = QLineEdit()
        self.name_input.setText(self.site_data.get("name", ""))
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        # 地址
        host_label = QLabel("地址:")
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("例如: localhost 或 192.168.1.100")
        self.host_input.setText(self.site_data.get("host", ""))
        layout.addWidget(host_label)
        layout.addWidget(self.host_input)

        # 端口
        port_label = QLabel("端口:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("例如: 8080")
        self.port_input.setText(str(self.site_data.get("port", "")))
        layout.addWidget(port_label)
        layout.addWidget(self.port_input)

        # 协议
        protocol_label = QLabel("协议:")
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["http", "https"])
        current_protocol = self.site_data.get("protocol", "http")
        self.protocol_combo.setCurrentText(current_protocol)
        layout.addWidget(protocol_label)
        layout.addWidget(self.protocol_combo)

        # 路径（可选）
        path_label = QLabel("路径（可选）:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("例如: /api/v1")
        self.path_input.setText(self.site_data.get("path", ""))
        layout.addWidget(path_label)
        layout.addWidget(self.path_input)

        # 分组
        group_label = QLabel("分组:")
        self.group_combo = QComboBox()
        self.group_combo.setEditable(True)
        self.group_combo.addItems(self.groups)
        current_group = self.site_data.get("group", "默认分组")
        self.group_combo.setCurrentText(current_group)
        layout.addWidget(group_label)
        layout.addWidget(self.group_combo)

        # 用户名（可选）
        username_label = QLabel("用户名（可选）:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("登录用户名")
        self.username_input.setText(self.site_data.get("username", ""))
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        # 密码（可选）
        password_label = QLabel("密码（可选）:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("登录密码")
        self.password_input.setText(self.site_data.get("password", ""))
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # 按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_site_data(self):
        """获取站点数据"""
        return {
            "name": self.name_input.text().strip(),
            "host": self.host_input.text().strip(),
            "port": self.port_input.text().strip(),
            "protocol": self.protocol_combo.currentText(),
            "path": self.path_input.text().strip(),
            "group": self.group_combo.currentText().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip()
        }


class SiteManager(QMainWindow):
    """站点管理主窗口"""

    VERSION = "v2.0.2"

    def __init__(self):
        super().__init__()
        self.config_file = Path("sites_config.json")
        self.deployment_file = Path("deployments.json")
        self.sites = []
        self.deployments = []
        self.load_config()
        self.load_deployments()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"站点访问管理器 {self.VERSION}")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(MODERN_STYLE)

        # 设置窗口图标
        icon_path = Path(__file__).parent / "asww.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_sites_tab(), "站点管理")
        self.tab_widget.addTab(self.create_deployments_tab(), "部署记录")
        self.tab_widget.addTab(self.create_about_tab(), "关于")
        main_layout.addWidget(self.tab_widget)

    def create_sites_tab(self):
        """创建站点管理标签页"""
        sites_widget = QWidget()
        sites_layout = QHBoxLayout(sites_widget)
        sites_layout.setContentsMargins(10, 10, 10, 10)

        # 左侧：分组列表
        left_panel = QGroupBox("分组")
        left_layout = QVBoxLayout()
        self.group_list = QListWidget()
        self.group_list.itemClicked.connect(self.on_group_selected)
        self.group_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.group_list.customContextMenuRequested.connect(self.show_group_context_menu)
        left_layout.addWidget(self.group_list)
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(220)

        # 右侧：站点列表和操作按钮
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # 站点列表标题
        title_label = QLabel("站点列表（双击打开）")
        title_label.setStyleSheet("font-size: 12pt; font-weight: 600; color: #424242; margin-bottom: 5px;")
        right_layout.addWidget(title_label)

        # 站点列表
        self.site_list = QListWidget()
        self.site_list.itemDoubleClicked.connect(self.open_site)
        right_layout.addWidget(self.site_list)

        # 操作按钮
        button_layout = QHBoxLayout()
        add_btn = QPushButton("➕ 添加站点")
        edit_btn = QPushButton("✏️ 编辑站点")
        delete_btn = QPushButton("🗑️ 删除站点")
        open_btn = QPushButton("🌐 打开站点")

        add_btn.clicked.connect(self.add_site)
        edit_btn.clicked.connect(self.edit_site)
        delete_btn.clicked.connect(self.delete_site)
        open_btn.clicked.connect(self.open_site)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(open_btn)
        right_layout.addLayout(button_layout)

        right_panel.setLayout(right_layout)

        # 添加到主布局
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 1)
        sites_layout.addWidget(splitter)

        self.refresh_groups()
        self.refresh_sites()

        return sites_widget

    def create_deployments_tab(self):
        """创建部署记录标签页"""
        deployments_widget = QWidget()
        deployments_layout = QVBoxLayout(deployments_widget)
        deployments_layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel("部署历史记录")
        title_label.setStyleSheet("font-size: 12pt; font-weight: 600; color: #424242; margin-bottom: 5px;")
        deployments_layout.addWidget(title_label)

        # 部署记录表格
        self.deployment_table = QTableWidget()
        self.deployment_table.setColumnCount(8)
        self.deployment_table.setHorizontalHeaderLabels([
            "部署时间", "类型", "站点名称", "版本", "环境", "状态", "部署人员", "备注"
        ])
        self.deployment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.deployment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.deployment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.deployment_table.setAlternatingRowColors(True)
        deployments_layout.addWidget(self.deployment_table)

        # 操作按钮
        button_layout = QHBoxLayout()
        add_deployment_btn = QPushButton("➕ 添加记录")
        edit_deployment_btn = QPushButton("✏️ 编辑记录")
        delete_deployment_btn = QPushButton("🗑️ 删除记录")
        refresh_btn = QPushButton("🔄 刷新")

        add_deployment_btn.clicked.connect(self.add_deployment)
        edit_deployment_btn.clicked.connect(self.edit_deployment)
        delete_deployment_btn.clicked.connect(self.delete_deployment)
        refresh_btn.clicked.connect(self.refresh_deployments)

        button_layout.addWidget(add_deployment_btn)
        button_layout.addWidget(edit_deployment_btn)
        button_layout.addWidget(delete_deployment_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        deployments_layout.addLayout(button_layout)

        self.refresh_deployments()

        return deployments_widget

    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.sites = json.load(f)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"加载配置失败: {str(e)}")
                self.sites = []
        else:
            self.sites = []

    def load_deployments(self):
        """加载部署记录"""
        if self.deployment_file.exists():
            try:
                with open(self.deployment_file, 'r', encoding='utf-8') as f:
                    self.deployments = json.load(f)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"加载部署记录失败: {str(e)}")
                self.deployments = []
        else:
            self.deployments = []

    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.sites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存配置失败: {str(e)}")

    def save_deployments(self):
        """保存部署记录"""
        try:
            with open(self.deployment_file, 'w', encoding='utf-8') as f:
                json.dump(self.deployments, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存部署记录失败: {str(e)}")

    def get_groups(self):
        """获取所有分组"""
        groups = set()
        for site in self.sites:
            groups.add(site.get("group", "默认分组"))
        return sorted(list(groups)) if groups else ["默认分组"]

    def refresh_groups(self):
        """刷新分组列表"""
        self.group_list.clear()
        all_item = QListWidgetItem("全部站点")
        self.group_list.addItem(all_item)
        for group in self.get_groups():
            item = QListWidgetItem(group)
            self.group_list.addItem(item)
        self.group_list.setCurrentRow(0)

    def refresh_sites(self, filter_group=None):
        """刷新站点列表"""
        self.site_list.clear()
        for site in self.sites:
            if filter_group and filter_group != "全部站点":
                if site.get("group", "默认分组") != filter_group:
                    continue
            url = self.build_url(site)
            display_text = f"{site['name']} - {url}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, site)
            self.site_list.addItem(item)

    def build_url(self, site):
        """构建完整URL"""
        protocol = site.get("protocol", "http")
        host = site.get("host", "")
        port = site.get("port", "")
        path = site.get("path", "")

        if port:
            url = f"{protocol}://{host}:{port}"
        else:
            url = f"{protocol}://{host}"

        if path:
            if not path.startswith("/"):
                path = "/" + path
            url += path

        return url

    def on_group_selected(self, item):
        """分组选择事件"""
        group_name = item.text()
        self.refresh_sites(group_name)

    def show_group_context_menu(self, position):
        """显示分组右键菜单"""
        item = self.group_list.itemAt(position)
        if not item:
            return

        group_name = item.text()
        # "全部站点"不允许重命名
        if group_name == "全部站点":
            return

        menu = QMenu()
        rename_action = menu.addAction("重命名分组")

        action = menu.exec(self.group_list.mapToGlobal(position))
        if action == rename_action:
            self.rename_group(group_name)

    def rename_group(self, old_name):
        """重命名分组"""
        new_name, ok = QInputDialog.getText(
            self,
            "重命名分组",
            f"请输入新的分组名称（当前: {old_name}）:",
            text=old_name
        )

        if not ok or not new_name.strip():
            return

        new_name = new_name.strip()

        # 检查新名称是否已存在
        if new_name in self.get_groups() and new_name != old_name:
            QMessageBox.warning(self, "警告", f"分组 '{new_name}' 已存在！")
            return

        # 检查是否为保留名称
        if new_name == "全部站点":
            QMessageBox.warning(self, "警告", "不能使用保留名称 '全部站点'！")
            return

        # 更新所有使用该分组的站点
        updated_count = 0
        for site in self.sites:
            if site.get("group", "默认分组") == old_name:
                site["group"] = new_name
                updated_count += 1

        if updated_count > 0:
            self.save_config()
            self.refresh_groups()
            self.refresh_sites()
            QMessageBox.information(self, "成功", f"已将 {updated_count} 个站点的分组从 '{old_name}' 更新为 '{new_name}'")
        else:
            QMessageBox.information(self, "提示", f"分组 '{old_name}' 下没有站点")


    def add_site(self):
        """添加站点"""
        dialog = SiteDialog(self, groups=self.get_groups())
        if dialog.exec():
            site_data = dialog.get_site_data()
            if not site_data["name"] or not site_data["host"]:
                QMessageBox.warning(self, "警告", "站点名称和地址不能为空！")
                return
            self.sites.append(site_data)
            self.save_config()
            self.refresh_groups()
            self.refresh_sites()

    def edit_site(self):
        """编辑站点"""
        current_item = self.site_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要编辑的站点！")
            return

        site_data = current_item.data(Qt.UserRole)
        dialog = SiteDialog(self, site_data=site_data, groups=self.get_groups())
        if dialog.exec():
            new_data = dialog.get_site_data()
            if not new_data["name"] or not new_data["host"]:
                QMessageBox.warning(self, "警告", "站点名称和地址不能为空！")
                return

            # 更新站点数据
            index = self.sites.index(site_data)
            self.sites[index] = new_data
            self.save_config()
            self.refresh_groups()
            self.refresh_sites()

    def delete_site(self):
        """删除站点"""
        current_item = self.site_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要删除的站点！")
            return

        site_data = current_item.data(Qt.UserRole)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除站点 '{site_data['name']}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.sites.remove(site_data)
            self.save_config()
            self.refresh_groups()
            self.refresh_sites()

    def open_site(self, item=None):
        """在浏览器中打开站点"""
        if item is None:
            item = self.site_list.currentItem()

        if not item:
            QMessageBox.warning(self, "警告", "请先选择要打开的站点！")
            return

        site_data = item.data(Qt.UserRole)
        url = self.build_url(site_data)

        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开浏览器失败: {str(e)}")

    def add_deployment(self):
        """添加部署记录"""
        dialog = DeploymentDialog(self)
        if dialog.exec():
            deployment_data = dialog.get_deployment_data()
            if not deployment_data["site_name"]:
                QMessageBox.warning(self, "警告", "站点名称不能为空！")
                return
            self.deployments.append(deployment_data)
            self.save_deployments()
            self.refresh_deployments()

    def edit_deployment(self):
        """编辑部署记录"""
        current_row = self.deployment_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要编辑的记录！")
            return

        # 从第一列获取存储的部署数据
        time_item = self.deployment_table.item(current_row, 0)
        if not time_item:
            return

        deployment_data = time_item.data(Qt.UserRole)
        if not deployment_data:
            return

        dialog = DeploymentDialog(self, deployment_data=deployment_data)
        if dialog.exec():
            new_data = dialog.get_deployment_data()
            if not new_data["site_name"]:
                QMessageBox.warning(self, "警告", "站点名称不能为空！")
                return

            # 在原始列表中找到并更新数据
            for i, dep in enumerate(self.deployments):
                if dep == deployment_data:
                    self.deployments[i] = new_data
                    break

            self.save_deployments()
            self.refresh_deployments()

    def delete_deployment(self):
        """删除部署记录"""
        current_row = self.deployment_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要删除的记录！")
            return

        # 从第一列获取存储的部署数据
        time_item = self.deployment_table.item(current_row, 0)
        if not time_item:
            return

        deployment_data = time_item.data(Qt.UserRole)
        if not deployment_data:
            return

        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除站点 '{deployment_data.get('site_name', '')}' 的部署记录吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 在原始列表中找到并删除数据
            for i, dep in enumerate(self.deployments):
                if dep == deployment_data:
                    del self.deployments[i]
                    break

            self.save_deployments()
            self.refresh_deployments()

    def refresh_deployments(self):
        """刷新部署记录表格"""
        self.deployment_table.setRowCount(0)

        # 按时间倒序排列
        sorted_deployments = sorted(
            self.deployments,
            key=lambda x: x.get("deploy_time", ""),
            reverse=True
        )

        for deployment in sorted_deployments:
            row = self.deployment_table.rowCount()
            self.deployment_table.insertRow(row)

            # 设置单元格内容
            time_item = QTableWidgetItem(deployment.get("deploy_time", ""))
            time_item.setData(Qt.UserRole, deployment)  # 存储部署数据引用
            self.deployment_table.setItem(row, 0, time_item)

            self.deployment_table.setItem(row, 1, QTableWidgetItem(deployment.get("type", "")))
            self.deployment_table.setItem(row, 2, QTableWidgetItem(deployment.get("site_name", "")))
            self.deployment_table.setItem(row, 3, QTableWidgetItem(deployment.get("version", "")))
            self.deployment_table.setItem(row, 4, QTableWidgetItem(deployment.get("environment", "")))

            # 状态单元格添加颜色
            status_item = QTableWidgetItem(deployment.get("status", ""))
            status = deployment.get("status", "")
            if status == "成功":
                status_item.setForeground(QColor("#4CAF50"))
            elif status == "失败":
                status_item.setForeground(QColor("#F44336"))
            elif status == "进行中":
                status_item.setForeground(QColor("#FF9800"))
            elif status == "回滚":
                status_item.setForeground(QColor("#9C27B0"))
            self.deployment_table.setItem(row, 5, status_item)

            self.deployment_table.setItem(row, 6, QTableWidgetItem(deployment.get("deployer", "")))
            self.deployment_table.setItem(row, 7, QTableWidgetItem(deployment.get("notes", "")))

    def create_about_tab(self):
        """创建关于标签页"""
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        about_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel(f"站点访问管理器 {self.VERSION}")
        title_label.setStyleSheet("font-size: 18pt; font-weight: 700; color: #2196F3; margin-bottom: 10px;")
        about_layout.addWidget(title_label)

        # 描述
        desc_label = QLabel("简易的站点地址和端口配置管理器")
        desc_label.setStyleSheet("font-size: 11pt; color: #757575; margin-bottom: 20px;")
        about_layout.addWidget(desc_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        about_layout.addWidget(line)

        # 更新记录标题
        changelog_title = QLabel("更新记录")
        changelog_title.setStyleSheet("font-size: 14pt; font-weight: 600; color: #424242; margin-top: 15px; margin-bottom: 10px;")
        about_layout.addWidget(changelog_title)

        # 更新记录内容
        changelog_text = QTextEdit()
        changelog_text.setReadOnly(True)
        changelog_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                background-color: #FAFAFA;
                padding: 15px;
                font-family: "Consolas", "Monaco", monospace;
                font-size: 9pt;
            }
        """)

        # 读取CHANGELOG.md文件
        changelog_file = Path(__file__).parent / "CHANGELOG.md"
        if changelog_file.exists():
            try:
                with open(changelog_file, 'r', encoding='utf-8') as f:
                    changelog_content = f.read()
                changelog_text.setPlainText(changelog_content)
            except Exception as e:
                changelog_text.setPlainText(f"无法读取更新记录: {str(e)}")
        else:
            changelog_text.setPlainText("更新记录文件不存在")

        about_layout.addWidget(changelog_text)

        return about_widget


def main():
    app = QApplication(sys.argv)
    window = SiteManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
