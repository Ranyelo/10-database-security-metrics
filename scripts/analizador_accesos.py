#!/usr/bin/env python3
import sys
import re

# Formato aproximado de log de conexiones de PostgreSQL
# 2026-07-04 23:10:05 UTC [12345] postgres@db connection failed: password authentication failed for user "ecommerce_user"
# 2026-07-04 23:10:10 UTC [12346] postgres@db connection authorized: user=ecommerce_user database=db
LOG_PATTERN = re.compile(
    r'.*?connection (?P<status>failed|authorized):.*?'
)

def analizar_log_conexiones(ruta_log):
    intentos_totales = 0
    intentos_fallidos = 0
    
    with open(ruta_log, 'r', encoding='utf-8') as f:
        for linea in f:
            match = LOG_PATTERN.match(linea)
            if match:
                intentos_totales += 1
                status = match.group('status')
                if status == 'failed':
                    intentos_fallidos += 1
                    
    return intentos_totales, intentos_fallidos

def main():
    if len(sys.argv) < 2:
        print("Uso: python analizador_accesos.py <archivo_postgresql.log>")
        sys.exit(1)
        
    ruta_log = sys.argv[1]
    try:
        totales, fallidos = analizar_log_conexiones(ruta_log)
        if totales > 0:
            tiaf = (fallidos / totales) * 100
        else:
            tiaf = 0.0
            
        print(f"--- Reporte Metricas de Acceso (TIAF) ---")
        print(f"Total de intentos de conexion: {totales}")
        print(f"Intentos fallidos de conexion: {fallidos}")
        print(f"Tasa de Intentos de Acceso Fallidos (TIAF): {tiaf:.2f}%")
        
        if tiaf > 3.0:
            print("[ALERTA] La tasa TIAF supera el limite insatisfactorio (>3%). Posible ataque de fuerza bruta.")
        else:
            print("[INFO] Tasa TIAF dentro de los limites aceptables.")
            
    except FileNotFoundError:
        print(f"[-] Error: No se pudo abrir el archivo {ruta_log}")
    except Exception as e:
        print(f"[-] Ocurrio un error inesperado: {e}")

if __name__ == '__main__':
    main()
