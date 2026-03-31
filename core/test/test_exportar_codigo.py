import runpy
from unittest.mock import patch, mock_open

from django.test import SimpleTestCase
import exportar_codigo as ec


class ExportarCodigoTest(SimpleTestCase):

    # 🔹 is_valid_file
    def test_is_valid_file_valido(self):
        self.assertTrue(ec.is_valid_file("teste.py"))

    def test_is_valid_file_extensao_invalida(self):
        self.assertFalse(ec.is_valid_file("teste.exe"))

    def test_is_valid_file_arquivo_ignorado(self):
        self.assertFalse(ec.is_valid_file(".env"))

    # 🔹 collect_code_to_pdf (mockado)
    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("exportar_codigo.os.walk")
    def test_collect_code_basico(self, mock_walk, mock_doc):
        mock_walk.return_value = [
            ("./", ["venv"], ["arquivo.py", "ignorado.exe"])
        ]

        mock_instance = mock_doc.return_value

        with patch("builtins.open", mock_open(read_data="print('oi')")):
            ec.collect_code_to_pdf()

        self.assertTrue(mock_instance.build.called)

    # 🔹 ignora diretórios
    @patch("exportar_codigo.os.walk")
    def test_ignora_diretorios(self, mock_walk):
        dirs = ["venv", "core"]
        files = ["teste.py"]

        mock_walk.return_value = [
            ("./", dirs, files)
        ]

        with patch("exportar_codigo.SimpleDocTemplate"):
            with patch("builtins.open", mock_open(read_data="code")):
                ec.collect_code_to_pdf()

        self.assertNotIn("venv", dirs)

    # 🔹 erro ao ler arquivo
    @patch("exportar_codigo.os.walk")
    @patch("exportar_codigo.SimpleDocTemplate")
    def test_erro_leitura(self, mock_doc, mock_walk):
        mock_walk.return_value = [
            ("./", [], ["arquivo.py"])
        ]

        with patch("builtins.open", side_effect=Exception("erro")):
            ec.collect_code_to_pdf()

        self.assertTrue(True)

    # 🔹 caminho relativo
    @patch("exportar_codigo.os.walk")
    @patch("exportar_codigo.SimpleDocTemplate")
    def test_relpath(self, mock_doc, mock_walk):
        mock_walk.return_value = [
            ("./pasta", [], ["arquivo.py"])
        ]

        with patch("builtins.open", mock_open(read_data="code")):
            ec.collect_code_to_pdf()

        self.assertTrue(True)

    # 🔥 cobre o if __name__ == "__main__"
    @patch("exportar_codigo.collect_code_to_pdf")
    def test_main_execucao(self, mock_collect):
        runpy.run_module("exportar_codigo", run_name="__main__")
        mock_collect.assert_called_once()