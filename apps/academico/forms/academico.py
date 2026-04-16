"""
Formulários do domínio acadêmico (turma, disciplina, atividades).

O que é: validações de negócio na camada de formulário antes de persistir
em ``models.academico``.
"""

from django import forms
from apps.comum.forms.base_formularios import BaseModelForm
from ..models.academico import Turma, Disciplina, AtividadeProfessor, MaterialDidatico
from apps.usuarios.models.perfis import Professor

class TurmaForm(BaseModelForm):
    """FormulÃ¡rio para Turma."""
    class Meta:
        model = Turma
        fields = ["nome", "turno", "ano"]
        
    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        ano = cleaned_data.get("ano")
        
        # ValidaÃ§Ã£o de duplicidade
        qs = Turma.objects.filter(nome=nome, ano=ano)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise forms.ValidationError("JÃ¡ existe uma turma com este nome para o ano informado.")
            
        return cleaned_data

class DisciplinaForm(BaseModelForm):
    """FormulÃ¡rio para Disciplina."""
    class Meta:
        model = Disciplina
        fields = ["nome", "professor", "turma"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: filtrar professores se necessÃ¡rio
        self.fields["professor"].queryset = Professor.objects.select_related("user").all()

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        turma = cleaned_data.get("turma")
        
        if nome and turma:
            qs = Disciplina.objects.filter(nome=nome, turma=turma)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f"A disciplina '{nome}' jÃ¡ estÃ¡ cadastrada para esta turma.")
        
        return cleaned_data

class AtividadeProfessorForm(BaseModelForm):
    """FormulÃ¡rio para o professor lanÃ§ar atividades ou avaliaÃ§Ãµes."""
    class Meta:
        model = AtividadeProfessor
        fields = ["titulo", "tipo", "data", "prazo_final", "descricao"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "prazo_final": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get("data")
        prazo_final = cleaned_data.get("prazo_final")
        tipo = cleaned_data.get("tipo")
        from apps.calendario.models.calendario import EventoCalendario
        
        if tipo != "PROVA" and not prazo_final:
            self.add_error("prazo_final", "Para atividades e trabalhos, é obrigatório definir um prazo final de entrega.")

        if data and tipo == "PROVA":
            evento = EventoCalendario.objects.filter(data=data, tipo="PROVA").first()
            if not evento:
                self.add_error("data", "Provas só podem ser cadastradas em datas marcadas como 'Semana de Prova' no Calendário Escolar Oficial.")
        return cleaned_data

class MaterialDidaticoForm(BaseModelForm):
    """Formulário para o professor disponibilizar materiais de aula."""
    class Meta:
        model = MaterialDidatico
        fields = ["titulo", "tipo", "url", "arquivo", "livro", "descricao"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.biblioteca.models.biblioteca import Livro
        self.fields["livro"].queryset = Livro.objects.all().order_by("titulo")

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        url = cleaned_data.get("url")
        arquivo = cleaned_data.get("arquivo")
        livro = cleaned_data.get("livro")

        if tipo == 'LINK' and not url:
            self.add_error("url", "Informe o link para o material.")
        elif tipo == 'ARQUIVO' and not arquivo:
            self.add_error("arquivo", "Faça o upload do arquivo.")
        elif tipo == 'LIVRO' and not livro:
            self.add_error("livro", "Selecione um livro da biblioteca.")

        return cleaned_data
