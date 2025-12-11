import os
import sys
import subprocess

def create_shortcut():
    # Rutas
    target_script = os.path.abspath("gui_app.py")
    work_dir = os.path.dirname(target_script)
    
    # Intentar usar pythonw.exe para que no se abra la consola negra
    python_exe = sys.executable
    if "python.exe" in python_exe:
        pythonw = python_exe.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw):
            python_exe = pythonw
            
    # Nombre del acceso directo
    shortcut_name = "YouTube Downloader.lnk"
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    shortcut_path = os.path.join(desktop_path, shortcut_name)

    # Script VBS para crear el acceso directo (windows nativo)
    vbs_script = f"""
    Set oWS = WScript.CreateObject("WScript.Shell")
    sLinkFile = "{shortcut_path}"
    Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "{python_exe}"
    oLink.Arguments = "{target_script}"
    oLink.WorkingDirectory = "{work_dir}"
    oLink.Description = "Convertidor YT a MP4"
    ' Usa el icono de python por defecto, o puedes poner una ruta a un .ico
    oLink.IconLocation = "{python_exe},0" 
    oLink.Save
    """

    # Crear archivo temporal VBS
    vbs_file = "create_shortcut_temp.vbs"
    try:
        with open(vbs_file, "w") as file:
            file.write(vbs_script)

        # Ejecutar VBS
        subprocess.run(["cscript", "//nologo", vbs_file], check=True)
        print(f"✅ Acceso directo creado en el Escritorio: {shortcut_path}")
    except Exception as e:
        print(f"❌ Error al crear acceso directo: {e}")
    finally:
        # Limpiar archivo temporal
        if os.path.exists(vbs_file):
            os.remove(vbs_file)

if __name__ == "__main__":
    create_shortcut()
    print("\nPuedes cerrar esta ventana.")
    try:
        input("Presiona Enter para terminar...")
    except:
        pass
