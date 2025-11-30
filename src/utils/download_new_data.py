import os
import urllib.request
import time

def download_covid_papers():
    # Directorio de destino
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista de papers (Arxiv es Open Access y estable para descargas)
    papers = [
        {
            "url": "https://arxiv.org/pdf/2106.05388", 
            "filename": "neurological_covid19.pdf",
            "title": "Neurological Consequences of COVID-19 Infection"
        },
        {
            "url": "https://arxiv.org/pdf/2105.15094", 
            "filename": "generalization_covid19_ct.pdf",
            "title": "Systematic investigation into generalization of COVID-19 CT deep learning models"
        }
    ]
    
    # Configurar headers para evitar bloqueo 403
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
    urllib.request.install_opener(opener)

    print("⬇️ Iniciando descarga de literatura médica sobre COVID-19...\n")

    for paper in papers:
        filepath = os.path.join(output_dir, paper["filename"])
        
        # Solo descargar si no existe
        if not os.path.exists(filepath):
            print(f"📥 Descargando: {paper['title']}...")
            try:
                urllib.request.urlretrieve(paper["url"], filepath)
                print(f"   ✅ Guardado en: {filepath}")
                time.sleep(1) # Pausa cortés para no saturar el servidor
            except Exception as e:
                print(f"   ❌ Error descargando {paper['filename']}: {e}")
        else:
            print(f"   ℹ️ El archivo {paper['filename']} ya existe.")

    print("\n✅ Descarga completada. Archivos listos en data/raw/")

if __name__ == "__main__":
    download_covid_papers()