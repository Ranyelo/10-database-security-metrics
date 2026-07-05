#!/usr/bin/env python3
import os
import sys

def evaluar_respaldos(directorio_respaldos):
    if not os.path.exists(directorio_respaldos):
        print(f"[-] El directorio de respaldos '{directorio_respaldos}' no existe.")
        return
        
    total_rutinas = 0
    exitosos = 0
    
    print(f"[+] Evaluando respaldos en: {directorio_respaldos}")
    for archivo in os.listdir(directorio_respaldos):
        # Asumiendo respaldos con extension .sql o .dump o .tar.gz
        if archivo.endswith(('.sql', '.dump', '.gz', '.zip')):
            total_rutinas += 1
            ruta_completa = os.path.join(directorio_respaldos, archivo)
            tamano = os.path.getsize(ruta_completa)
            
            # Un respaldo vacio o menor a 1KB se considera fallido
            if tamano > 1024:
                exitosos += 1
                print(f"  [OK] {archivo} - {tamano / 1024:.2f} KB")
            else:
                print(f"  [FALLO] {archivo} - Archivo corrupto o vacio ({tamano} bytes)")
                
    if total_rutinas > 0:
        perc = (exitosos / total_rutinas) * 100
    else:
        perc = 0.0
        
    print(f"\n--- Reporte de Indicador PERC ---")
    print(f"Rutinas de respaldo evaluadas: {total_rutinas}")
    print(f"Respaldos exitosos: {exitosos}")
    print(f"Porcentaje de Exito en Respaldos (PERC): {perc:.2f}%")
    
    if perc < 100.0:
        print("[ALERTA] El PERC es inferior al 100%. Se requiere atencion de soporte.")
    else:
        print("[OK] Todos los respaldos se generaron correctamente.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python verificar_respaldos.py <directorio_de_respaldos>")
        sys.exit(1)
        
    dir_respaldos = sys.argv[1]
    evaluar_respaldos(dir_respaldos)

if __name__ == '__main__':
    main()
