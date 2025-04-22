import yt_dlp


def baixar_audio_yt_dlp(url, pasta_saida="downloads", file_name="original_ytd"):
    # Configurações do yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Melhor qualidade de áudio
        # 'outtmpl': f'{pasta_saida}/%(title)s.%(ext)s',  # Nome do arquivo de saída
        'outtmpl': f'{pasta_saida}/{file_name}',  # Nome do arquivo de saída
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extrair áudio
            'preferredcodec': 'wav',  # Formato WAV
            'preferredquality': '192',  # Qualidade do áudio
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# Exemplo de uso
url_youtube = "https://www.youtube.com/watch?v=eomrw3DgRmE"
baixar_audio_yt_dlp(url_youtube)
