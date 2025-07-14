# statgen/backend/core/models.py
from django.db import models
# Futuramente, importaremos o User para o campo 'owner'
from django.contrib.auth.models import User 

class Experiment(models.Model):
    DESIGN_CHOICES = [
        ('DIC', 'Delineamento Inteiramente Casualizado'),
        ('DBC', 'Delineamento em Blocos Casualizados'),
        ('QL', 'Quadrado Latino'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nome do Experimento")
    design_type = models.CharField(max_length=3, choices=DESIGN_CHOICES, verbose_name="Tipo de Delineamento")
    
    # JSONField é perfeito para guardar dados semi-estruturados como os parâmetros de entrada.
    parameters = models.JSONField(verbose_name="Parâmetros de Entrada")
    
    # Também usaremos um JSONField para guardar o resultado completo do sorteio.
    layout = models.JSONField(verbose_name="Layout do Sorteio")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    # --- CAMPO A SER ADICIONADO NO FUTURO ---
    # Quando tivermos usuários, esta linha conectará o experimento ao seu dono.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="experiments", null=True, blank=True)

    def __str__(self):
        return f"{self.owner.username} ({self.get_design_type_display()})"

    class Meta:
        ordering = ['-created_at'] # Ordena os experimentos do mais novo para o mais antigo.
