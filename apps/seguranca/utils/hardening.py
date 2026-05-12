import os


def validar_assinatura_arquivo(arquivo):
    """
    Verifica se o conteúdo do arquivo corresponde à sua extensão (Magic Numbers).
    Implementação manual para evitar dependência do imghdr (removido no Python 3.13).
    """
    if not arquivo:
        return True

    ext = os.path.splitext(arquivo.name)[1].lower()

    # Se for imagem, verifica via Magic Numbers
    if ext in [".jpg", ".jpeg", ".png", ".gif"]:
        # Lê os primeiros bytes
        header = arquivo.read(12)
        arquivo.seek(0)

        # JPEG: FF D8 FF
        if ext in [".jpg", ".jpeg"]:
            return header.startswith(b"\xff\xd8\xff")

        # PNG: 89 50 4E 47 0D 0A 1A 0A
        if ext == ".png":
            return header.startswith(b"\x89PNG\r\n\x1a\n")

        # GIF: GIF87a ou GIF89a
        if ext == ".gif":
            return header.startswith(b"GIF87a") or header.startswith(b"GIF89a")

    return True


def sanitizar_pii(texto):
    """Remove CPFs e emails de strings para logs de segurança."""
    import re

    if not texto:
        return texto

    # Máscara para CPF (XXX.XXX.XXX-XX ou apenas números)
    texto = re.sub(r"\d{3}\.\d{3}\.\d{3}-\d{2}", "[CPF-PROTEGIDO]", texto)
    texto = re.sub(r"\d{11}", "[ID-SENSIVEL]", texto)

    # Máscara para E-mail
    texto = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL-PROTEGIDO]", texto)

    return texto
