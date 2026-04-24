from django.test import TestCase
from apps.usuarios.models.perfis import Aluno
from apps.academico.models import Turma
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

class SecurityAuditTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Password123!')
        # Precisa de uma turma para o aluno
        self.turma = Turma.objects.create(nome="Turma Teste", ano=2026, turno="manha")
        self.aluno = Aluno.objects.create(
            user=self.user,
            nome_completo="João Teste",
            cpf="467.509.166-00",
            telefone="11999999999",
            logradouro="Rua Teste",
            turma=self.turma
        )

    def test_encryption_at_rest(self):
        """
        Valida se os dados estão criptografados no banco de dados.
        """
        with connection.cursor() as cursor:
            cursor.execute("SELECT telefone, logradouro FROM core_aluno WHERE id = %s", [self.aluno.id])
            row = cursor.fetchone()
            
            # O valor no banco deve ser um blob/string criptografada, não o texto original
            self.assertNotEqual(row[0], "11999999999")
            self.assertNotEqual(row[1], "Rua Teste")
            
        # No Django, o acesso deve ser transparente
        aluno_db = Aluno.objects.get(id=self.aluno.id)
        self.assertEqual(aluno_db.telefone, "11999999999")
        self.assertEqual(aluno_db.logradouro, "Rua Teste")

    def test_audit_trail_aluno(self):
        """
        Valida se as alterações no Aluno criam registros de histórico.
        """
        old_count = self.aluno.history.count()
        
        self.aluno.nome_completo = "João Alterado"
        self.aluno.save()
        
        self.assertEqual(self.aluno.history.count(), old_count + 1)
        latest_history = self.aluno.history.first()
        self.assertEqual(latest_history.nome_completo, "João Alterado")
        self.assertEqual(latest_history.history_type, '~') # Alteração
