"""
test_exportar_codigo.py — cobertura 100% do exportar_codigo.py
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

# Garante que o módulo exportar_codigo seja importável
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import exportar_codigo
from exportar_codigo import collect_code_to_pdf, main


class ExportarCodigoTest(unittest.TestCase):

    # ------------------------------------------------------------------
    # collect_code_to_pdf — fluxo principal
    # ------------------------------------------------------------------

    def test_collect_gera_pdf(self):
        """Função principal deve criar o PDF sem erros"""
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [(".", [], ["arquivo.py"])]
                with patch("builtins.open", mock_open(read_data="print('hello')")):
                    collect_code_to_pdf("saida_test.pdf")
            mock_pdf.output.assert_called_once()

    def test_collect_arquivo_com_erro_leitura(self):
        """Arquivos que não podem ser lidos devem ser ignorados sem quebrar"""
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [(".", [], ["erro.py"])]
                with patch("builtins.open", side_effect=Exception("erro")):
                    collect_code_to_pdf("saida_erro.pdf")
            mock_pdf.output.assert_called_once()

    def test_collect_sem_arquivos_py(self):
        """Deve funcionar mesmo sem nenhum .py encontrado"""
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [(".", [], [])]
                collect_code_to_pdf("vazio.pdf")
            mock_pdf.output.assert_called_once()

    def test_collect_multiplos_arquivos(self):
        """Deve processar múltiplos arquivos .py"""
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [(".", [], ["a.py", "b.py", "c.py"])]
                with patch("builtins.open", mock_open(read_data="x = 1")):
                    collect_code_to_pdf("multi.pdf")
            mock_pdf.output.assert_called()

    def test_collect_ignora_nao_py(self):
        """Arquivos não-.py devem ser ignorados"""
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [
                    (".", [], ["imagem.png", "readme.md", "dados.json"])
                ]
                with patch("builtins.open", mock_open(read_data="x = 1")):
                    collect_code_to_pdf("ignorados.pdf")
            mock_pdf.add_page.assert_not_called()

    def test_collect_subdiretorios(self):
        """Deve processar arquivos em subdiretórios"""
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = [
                    (".", ["subdir"], []),
                    ("./subdir", [], ["modulo.py"]),
                ]
                with patch("builtins.open", mock_open(read_data="def f(): pass")):
                    collect_code_to_pdf("subdir.pdf")
            mock_pdf.output.assert_called_once()

    # ------------------------------------------------------------------
    # main() — chamada direta
    # ------------------------------------------------------------------

    def test_main_chama_collect_diretamente(self):
        with patch.object(exportar_codigo, "collect_code_to_pdf") as mock_collect:
            main()
            mock_collect.assert_called_once()

    def test_main_passa_nome_arquivo(self):
        with patch.object(exportar_codigo, "collect_code_to_pdf") as mock_collect:
            main()
            args, kwargs = mock_collect.call_args
            self.assertTrue(len(args) > 0 or len(kwargs) > 0)

    def test_main_execucao(self):
        with patch.object(exportar_codigo, "collect_code_to_pdf") as mock_collect:
            mock_collect.return_value = None
            main()
            mock_collect.assert_called_once()

    # ------------------------------------------------------------------
    # Integração leve
    # ------------------------------------------------------------------

    def test_modulo_importa_sem_erros(self):
        self.assertTrue(callable(collect_code_to_pdf))
        self.assertTrue(callable(main))

    def test_collect_retorna_none(self):
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_fpdf.return_value = MagicMock()
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = []
                result = collect_code_to_pdf("teste_retorno.pdf")
        self.assertIsNone(result)

    def test_collect_nome_arquivo_personalizado(self):
        with patch("exportar_codigo.FPDF") as mock_fpdf:
            mock_pdf = MagicMock()
            mock_fpdf.return_value = mock_pdf
            with patch("os.walk") as mock_walk:
                mock_walk.return_value = []
                collect_code_to_pdf("meu_codigo_2026.pdf")
            mock_pdf.output.assert_called_once_with("meu_codigo_2026.pdf")