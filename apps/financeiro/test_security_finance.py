from django.test import TestCase
from apps.financeiro.models import Fatura
from apps.usuarios.models.perfis import Aluno
from apps.academico.models import Turma
from django.contrib.auth import get_user_model
from django.db import connection
from django.utils import timezone

User = get_user_model()

class FinanceSecurityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='finuser', password='Password123!')
        self.turma = Turma.objects.create(nome="Turma Fin", ano=2026, turno="tarde")
        self.aluno = Aluno.objects.create(
            user=self.user,
            nome_completo="Aluno Fin",
            cpf="529.982.247-25",
            turma=self.turma
        )
        self.fatura = Fatura.objects.create(
            aluno=self.aluno,
            descricao="Mensalidade Abril",
            valor=500.00,
            data_vencimento=timezone.now().date(),
            link_pagamento="https://pagamento.seguro.com/token123"
        )

    def test_fatura_encryption(self):
        """Valida criptografia do link de pagamento."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT link_pagamento FROM financeiro_fatura WHERE id = %s", [self.fatura.id])
            row = cursor.fetchone()
            self.assertNotEqual(row[0], "https://pagamento.seguro.com/token123")
        
        fatura_db = Fatura.objects.get(id=self.fatura.id)
        self.assertEqual(fatura_db.link_pagamento, "https://pagamento.seguro.com/token123")

    def test_fatura_audit(self):
        """Valida trilha de auditoria na fatura."""
        self.fatura.status = 'PAGO'
        self.fatura.save()
        
        self.assertEqual(self.fatura.history.count(), 2) # Criação + Alteração
        self.assertEqual(self.fatura.history.first().status, 'PAGO')
