# Usa un'immagine ufficiale di Python basata su Linux Debian minimale
FROM python:3.11-slim

# Imposta la cartella principale di lavoro dentro il container
WORKDIR /app

# Copia il file delle dipendenze e le installa senza mantenere cache inutili
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del codice della cartella corrente dentro il container
COPY . .

# Espone la porta 5000 su cui ascolta il server Flask
EXPOSE 5000

# Comando di avvio per eseguire l'applicazione Flask accessibile dall'esterno
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5000"]