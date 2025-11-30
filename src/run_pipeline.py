import subprocess
import sys
import time
import os

def run_step(script_path, description):
    print(f"\n{'='*60}")
    print(f"🚀 INICIANDO: {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    try:
        # Configurar PYTHONPATH para incluir el directorio 'src' raíz
        # Asumimos que este script (run_pipeline.py) está en 'src/'
        src_dir = os.path.dirname(os.path.abspath(__file__))
        env = os.environ.copy()
        env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

        # Ejecutamos el script como un subproceso
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False, # Dejamos que el output salga directo a consola
            text=True,
            env=env
        )
        duration = time.time() - start_time
        print(f"\n✅ ÉXITO: {description} completado en {duration:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: Falló {description}")
        print(f"Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Definimos la secuencia de pasos del pipeline
    steps = [
        {
            "path": os.path.join(base_dir, "testing", "check_setup.py"),
            "desc": "Verificación de Entorno y Dependencias"
        },
        {
            "path": os.path.join(base_dir, "testing", "test_ingestion.py"),
            "desc": "Pruebas de Ingesta de Datos (Download & Load)"
        },
        {
            "path": os.path.join(base_dir, "testing", "test_splitting.py"),
            "desc": "Pruebas de Transformación (Splitting Strategy)"
        },
        {
            "path": os.path.join(base_dir, "pipeline_ingestion.py"),
            "desc": "Ejecución del Pipeline de Ingestión Real (ETL -> VectorDB)"
        },
        {
            "path": os.path.join(base_dir, "testing", "test_retrieval.py"),
            "desc": "Pruebas de Recuperación (Retrieval)"
        },
        {
            "path": os.path.join(base_dir, "testing", "test_reranking.py"),
            "desc": "Pruebas de Reranking (Precision)"
        },
        {
            "path": os.path.join(base_dir, "testing", "test_chat.py"),
            "desc": "Pruebas de Generación (Chatbot E2E)"
        }
    ]

    print("🤖 INICIANDO ORQUESTACIÓN DEL PIPELINE DE MEDIRAG")
    
    for step in steps:
        if not os.path.exists(step["path"]):
            print(f"⚠️ Archivo no encontrado: {step['path']}")
            sys.exit(1)
            
        success = run_step(step["path"], step["desc"])
        if not success:
            print("\n🛑 Deteniendo pipeline por fallo en etapa previa.")
            sys.exit(1)

    print(f"\n{'='*60}")
    print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
