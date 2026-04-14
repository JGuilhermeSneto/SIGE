from django import forms
from apps.comum.forms.base_formularios import BaseModelForm
from ..models.academico import Turma, Disciplina, AtividadeProfessor
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
