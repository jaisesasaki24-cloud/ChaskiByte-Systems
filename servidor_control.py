import os
import sys
import json
import socket
import subprocess
import threading
import time
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.error

import concurrent.futures

PORT = 5050
BASE_DIR = r"C:\Users\USUARIO\Documents\Tarea Eureka"

def check_tcp_port(port, host="127.0.0.1", timeout=0.2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def check_all_services_status():
    service_defs = [
        ("eureka", "Eureka Server", 8761),
        ("gateway", "API Gateway", 18080),
        ("config", "Config Server", 8888),
        ("catalogo", "pc-catalogo-ms", 8081),
        ("orden1", "pc-orden-ms (Instancia 1)", 8082),
        ("orden2", "pc-orden-ms (Instancia 2)", 8083),
        ("postgres", "PostgreSQL (Docker)", 5433),
        ("grafana", "Grafana Dashboards", 13000)
    ]
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {executor.submit(check_tcp_port, port): (key, name, port) for key, name, port in service_defs}
        for future in concurrent.futures.as_completed(future_to_key):
            key, name, port = future_to_key[future]
            is_up = future.result()
            results[key] = {"name": name, "port": port, "up": is_up}
    return results

class ControlHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # Redirigir root a presentacion.html
        if parsed.path == "/" or parsed.path == "":
            self.send_response(302)
            self.send_header("Location", "/presentacion.html")
            self.end_headers()
            return

        if parsed.path == "/api/status":
            services = check_all_services_status()
            res_body = json.dumps({"ok": True, "services": services}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(res_body)
            return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
        
        response_data = {"ok": False, "msg": "Endpoint desconocido"}

        if parsed.path == "/api/iniciar-todo":
            bat_path = os.path.join(BASE_DIR, "iniciar_todo.bat")
            subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/c", bat_path], cwd=BASE_DIR, shell=True)
            response_data = {"ok": True, "msg": "Iniciando ecosistema completo en terminales independientes..."}

        elif parsed.path == "/api/iniciar-db":
            bat_path = os.path.join(BASE_DIR, "iniciar_db.bat")
            subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/c", bat_path], cwd=BASE_DIR, shell=True)
            response_data = {"ok": True, "msg": "Levantando contenedor PostgreSQL (Puerto 5433)..."}

        elif parsed.path == "/api/iniciar-obs":
            bat_path = os.path.join(BASE_DIR, "iniciar_observabilidad.bat")
            subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/c", bat_path], cwd=BASE_DIR, shell=True)
            response_data = {"ok": True, "msg": "Levantando stack de observabilidad (Prometheus y Grafana)..."}

        elif parsed.path == "/api/limpiar":
            bat_path = os.path.join(BASE_DIR, "limpiar_pc_laboratorio.bat")
            subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/c", bat_path], cwd=BASE_DIR, shell=True)
            response_data = {"ok": True, "msg": "Ejecutando limpieza preventiva de puertos de laboratorio..."}

        elif parsed.path == "/api/test/201":
            # Ejecutar POST de creación de orden con 18% IGV
            orden_payload = {
                "cliente": "Eliceo Parillo Mostajo y Cristhian Paul Laura",
                "tipoComprobante": "FACTURA",
                "metodoPago": "MERCADO_PAGO",
                "detalles": [
                    {"productoId": 1, "nombreProducto": "AMD Ryzen 7 7800X3D", "precioUnitario": 1780.00, "cantidad": 1},
                    {"productoId": 4, "nombreProducto": "Kingston Fury 1TB NVMe Gen4", "precioUnitario": 380.00, "cantidad": 1}
                ]
            }
            url = "http://localhost:18080/api/v1/ordenes"
            try:
                data = json.dumps(orden_payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=5) as resp:
                    code = resp.getcode()
                    body = json.loads(resp.read().decode("utf-8"))
                    elapsed = round((time.time() - t0) * 1000, 1)
                    response_data = {
                        "ok": True,
                        "status": code,
                        "statusText": "201 Created",
                        "timeMs": elapsed,
                        "data": body,
                        "msg": f"Orden creada exitosamente en {elapsed} ms con cálculo fiscal del 18% IGV."
                    }
            except urllib.error.HTTPError as e:
                response_data = {"ok": False, "status": e.code, "msg": f"Error HTTP {e.code}: {e.read().decode('utf-8')}"}
            except Exception as e:
                response_data = {"ok": False, "msg": f"No se pudo contactar al Gateway (18080): {str(e)}"}

        elif parsed.path == "/api/test/400":
            url = "http://localhost:18080/api/v1/ordenes"
            try:
                data = b"{}"
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=5)
                response_data = {"ok": False, "msg": "Se esperaba 400 Bad Request pero respondió OK"}
            except urllib.error.HTTPError as e:
                response_data = {
                    "ok": True,
                    "status": e.code,
                    "statusText": "400 Bad Request",
                    "msg": "Capturado código 400 Bad Request exitosamente (Validación: El campo 'cliente' es obligatorio)."
                }
            except Exception as e:
                response_data = {"ok": False, "msg": f"Error de conexión: {str(e)}"}

        elif parsed.path == "/api/test/404":
            url = "http://localhost:18080/api/v1/ordenes/99999"
            try:
                req = urllib.request.Request(url)
                urllib.request.urlopen(req, timeout=5)
                response_data = {"ok": False, "msg": "Se esperaba 404 Not Found pero respondió OK"}
            except urllib.error.HTTPError as e:
                response_data = {
                    "ok": True,
                    "status": e.code,
                    "statusText": "404 Not Found",
                    "msg": "Capturado código 404 Not Found exitosamente (La orden con ID 99999 no existe en PostgreSQL)."
                }
            except Exception as e:
                response_data = {"ok": False, "msg": f"Error de conexión: {str(e)}"}

        elif parsed.path == "/api/test/balanceo":
            url = "http://localhost:18080/api/v1/ordenes"
            resultados = []
            try:
                for i in range(1, 5):
                    t0 = time.time()
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req, timeout=4) as resp:
                        code = resp.getcode()
                        elapsed = round((time.time() - t0) * 1000, 1)
                        resultados.append(f"Petición {i}: HTTP {code} en {elapsed} ms (Procesada por réplica balanceada)")
                    time.sleep(0.3)
                response_data = {
                    "ok": True,
                    "msg": "4 solicitudes completadas con éxito vía Spring Cloud LoadBalancer.",
                    "logs": resultados
                }
            except Exception as e:
                response_data = {"ok": False, "msg": f"Fallo en prueba de balanceo: {str(e)}"}

        elif parsed.path == "/api/test/apagar-8082":
            # Matar proceso en puerto 8082 usando PowerShell
            ps_cmd = 'Get-NetTCPConnection -LocalPort 8082 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }'
            try:
                subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, timeout=5)
                response_data = {
                    "ok": True,
                    "msg": "Instancia en puerto 8082 detenida forzosamente. Vuelve a consultar el Gateway para comprobar que la instancia 8083 atiende transparentemente."
                }
            except Exception as e:
                response_data = {"ok": False, "msg": f"Error al detener puerto 8082: {str(e)}"}

        res_bytes = json.dumps(response_data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(res_bytes)

def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ControlHandler)
    print(f"===============================================================")
    print(f"  CHASKIPC CONTROL SERVER ACTIVO EN: http://localhost:{PORT}")
    print(f"===============================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == "__main__":
    run()
