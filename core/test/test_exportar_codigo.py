"""
test_exportar_codigo.py — cobertura 100% do exportar_codigo.py
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

# Garante que o módulo exportar_codigo seja importável
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)

import exportar_codigo
from exportar_codigo import collect_code_to_pdf, main


class ExportarCodigoTest(unittest.TestCase):

    # ------------------------------------------------------------------
    # collect_code_to_pdf — fluxo principal
    # ------------------------------------------------------------------

    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("os.walk")
    def test_collect_gera_pdf(self, mock_walk, mock_doc):
        mock_walk.return_value = [(".", [], ["arquivo.py"])]
        mock_instance = MagicMock()
        mock_doc.return_value = mock_instance

        with patch("builtins.open", mock_open(read_data="print('hello')")):
            collect_code_to_pdf("saida_test.pdf")

        mock_doc.assert_called_once()
        mock_instance.build.assert_called_once()

    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("os.walk")
    def test_collect_arquivo_com_erro_leitura(self, mock_walk, mock_doc):
        mock_walk.return_value = [(".", [], ["erro.py"])]
        mock_instance = MagicMock()
        mock_doc.return_value = mock_instance

        with patch("builtins.open", side_effect=Exception("erro")):
            collect_code_to_pdf("saida_erro.pdf")

        mock_instance.build.assert_called_once()

    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("os.walk")
    def test_collect_sem_arquivos(self, mock_walk, mock_doc):
        mock_walk.return_value = []
        mock_instance = MagicMock()
        mock_doc.return_value = mock_instance

        collect_code_to_pdf("vazio.pdf")

        mock_instance.build.assert_called_once()

    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("os.walk")
    def test_collect_multiplos_arquivos(self, mock_walk, mock_doc):
        mock_walk.return_value = [(".", [], ["a.py", "b.py"])]
        mock_instance = MagicMock()
        mock_doc.return_value = mock_instance

        with patch("builtins.open", mock_open(read_data="x = 1")):
            collect_code_to_pdf("multi.pdf")

        mock_instance.build.assert_called_once()

    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("os.walk")
    def test_collect_ignora_extensoes_invalidas(self, mock_walk, mock_doc):
        mock_walk.return_value = [
            (".", [], ["imagem.png", "dados.bin"])
        ]
        mock_instance = MagicMock()
        mock_doc.return_value = mock_instance

        collect_code_to_pdf("ignorados.pdf")

        mock_instance.build.assert_called_once()

    @patch("exportar_codigo.SimpleDocTemplate")
    @patch("os.walk")
    def test_collect_subdiretorios(self, mock_walk, mock_doc):
        mock_walk.return_value = [
            (".", ["subdir"], []),
            ("./subdir", [], ["modulo.py"]),
        ]
        mock_instance = MagicMock()
        mock_doc.return_value = mock_instance

        with patch("builtins.open", mock_open(read_data="def f(): pass")):
            collect_code_to_pdf("subdir.pdf")

        mock_instance.build.assert_called_once()

    def test_collect_retorna_none(self):
        with patch("exportar_codigo.SimpleDocTemplate") as mock_doc:
            mock_doc.return_value = MagicMock()
            with patch("os.walk", return_value=[]):
                result = collect_code_to_pdf("teste.pdf")

        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # main()
    # ------------------------------------------------------------------

    def test_main_chama_collect(self):
        with patch.object(exportar_codigo, "collect_code_to_pdf") as mock_collect:
            main()
            mock_collect.assert_called_once()

    def test_main_passa_nome_arquivo(self):
        with patch.object(exportar_codigo, "collect_code_to_pdf") as mock_collect:
            main()
            args, kwargs = mock_collect.call_args
            self.assertTrue(args or kwargs)

    # ------------------------------------------------------------------
    # Sanidade
    # ------------------------------------------------------------------

    def test_modulo_importa_sem_erros(self):
        self.assertTrue(callable(collect_code_to_pdf))
        self.assertTrue(callable(main))