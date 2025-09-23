from django.db import models
from django.conf import settings

# --- Modelos de Tabelas Existentes ---

class Sicadfull(models.Model):
    # ... (cole aqui todos os campos do modelo Sicadfull que você forneceu) ...
    servidor = models.CharField(max_length=50, blank=True, null=True)
    nro_bop = models.CharField(max_length=500, blank=True, null=True)
    nro_bop_aditado = models.CharField(max_length=500, blank=True, null=True)
    nro_tombo = models.CharField(max_length=500, blank=True, null=True)
    tipo_tombo = models.CharField(max_length=500, blank=True, null=True)
    unidade_origem = models.CharField(max_length=500, blank=True, null=True)
    unidade_responsavel = models.CharField(max_length=500, blank=True, null=True)
    data_registro = models.DateField(blank=True, null=True)
    hora_registro = models.TimeField(blank=True, null=True)
    data_fato = models.DateField(blank=True, null=True) 
    data_modificacao = models.DateField(blank=True, null=True) 
    dia_semana = models.CharField(max_length=500, blank=True, null=True)
    hora_fato = models.TimeField(blank=True, null=True)
    fx_4_hor = models.CharField(max_length=500, blank=True, null=True)
    fx_12_hr = models.CharField(max_length=500, blank=True, null=True)
    relatorio = models.CharField(max_length=500, blank=True, null=True)
    ident_autoria = models.CharField(max_length=500, blank=True, null=True)
    qtd_autor = models.IntegerField(blank=True, null=True)
    classe_motivo = models.CharField(max_length=500, blank=True, null=True)
    mes_registro = models.CharField(max_length=500, blank=True, null=True)
    mes_fato = models.CharField(max_length=500, blank=True, null=True)
    ano_registro = models.IntegerField(blank=True, null=True)
    ano_fato = models.IntegerField(blank=True, null=True)
    registros = models.CharField(max_length=500, blank=True, null=True)
    consolidado = models.CharField(max_length=500, blank=True, null=True)
    fato_real = models.CharField(max_length=500, blank=True, null=True)
    especificacao_crime = models.CharField(max_length=500, blank=True, null=True)
    meio_emp_deac = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=500, blank=True, null=True)
    longitude = models.CharField(max_length=500, blank=True, null=True)
    causa_presumivel = models.CharField(max_length=500, blank=True, null=True)
    especializacao_fato = models.CharField(max_length=500, blank=True, null=True)
    grupo_ocorrencia = models.CharField(max_length=500, blank=True, null=True)
    sub_grupo = models.CharField(max_length=500, blank=True, null=True)
    meio_empregado_sisp = models.CharField(max_length=500, blank=True, null=True)
    distrito = models.CharField(max_length=500, blank=True, null=True)
    municipios = models.CharField(max_length=500, blank=True, null=True)
    regionais = models.CharField(max_length=500, blank=True, null=True)
    bairros = models.CharField(max_length=500, blank=True, null=True)
    reg_integracao = models.CharField(max_length=500, blank=True, null=True)
    risp = models.CharField(max_length=500, blank=True, null=True)
    aisp = models.CharField(max_length=500, blank=True, null=True)
    rua_fato = models.CharField(max_length=500, blank=True, null=True)
    empresa = models.CharField(max_length=500, blank=True, null=True)
    linha = models.CharField(max_length=500, blank=True, null=True)
    tipo_transporte = models.CharField(max_length=500, blank=True, null=True)
    complemento = models.TextField(blank=True, null=True)
    local_ocorrencia = models.TextField(blank=True, null=True)
    identificacao_fato = models.TextField(blank=True, null=True)
    relator = models.TextField(blank=True, null=True)
    relato = models.TextField(blank=True, null=True)
    atuacao = models.CharField(max_length=500, blank=True, null=True)
    vit_nome = models.TextField(blank=True, null=True)
    vit_alcunha = models.CharField(max_length=500, blank=True, null=True)
    vit_dt_nasc = models.DateField(blank=True, null=True)
    vit_idade = models.IntegerField(blank=True, null=True)
    vit_fx_etaria = models.CharField(max_length=500, blank=True, null=True)
    vit_nro_doc = models.CharField(max_length=500, blank=True, null=True)
    vit_tipo_doc = models.CharField(max_length=500, blank=True, null=True)
    vit_pai = models.CharField(max_length=500, blank=True, null=True)
    vit_mae = models.CharField(max_length=500, blank=True, null=True)
    vit_tipo = models.CharField(max_length=500, blank=True, null=True)
    vit_sexo = models.CharField(max_length=100, blank=True, null=True)
    vit_cor_pele = models.CharField(max_length=500, blank=True, null=True)
    vit_grau_inst = models.CharField(max_length=500, blank=True, null=True)
    vit_profissao = models.CharField(max_length=500, blank=True, null=True)
    vit_situacao_emprego = models.CharField(max_length=500, blank=True, null=True)
    vit_estado_civil = models.CharField(max_length=500, blank=True, null=True)
    aut_nome = models.CharField(max_length=500, blank=True, null=True)
    aut_alcunha = models.CharField(max_length=500, blank=True, null=True)
    aut_data_nasc = models.DateField(blank=True, null=True)
    aut_idade = models.IntegerField(blank=True, null=True)
    aut_fx_etaria = models.CharField(max_length=500, blank=True, null=True)
    aut_nro_doc = models.CharField(max_length=500, blank=True, null=True)
    aut_tipo_doc = models.CharField(max_length=500, blank=True, null=True)
    aut_pai = models.CharField(max_length=500, blank=True, null=True)
    aut_mae = models.CharField(max_length=500, blank=True, null=True)
    aut_tipo = models.CharField(max_length=500, blank=True, null=True)
    aut_sexo = models.CharField(max_length=500, blank=True, null=True)
    grau_de_relacionamento = models.CharField(max_length=500, blank=True, null=True)
    aut_cor_pele = models.CharField(max_length=500, blank=True, null=True)
    aut_grau_inst = models.CharField(max_length=500, blank=True, null=True)
    aut_profissao = models.CharField(max_length=500, blank=True, null=True)
    aut_sit_emprego = models.CharField(max_length=500, blank=True, null=True)
    aut_est_civil = models.CharField(max_length=500, blank=True, null=True)
    meio_locomocao = models.CharField(max_length=500, blank=True, null=True)
    cor_veiculo = models.CharField(max_length=500, blank=True, null=True)
    marca_veic_fuga = models.CharField(max_length=500, blank=True, null=True)
    modelo_do_veic_fuga = models.CharField(max_length=500, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    id = models.AutoField(primary_key=True, db_column='pk')
    id_servidor_sicad = models.IntegerField(blank=True, null=True)
    qtd = models.IntegerField(blank=True, null=True)
    usuario_modificacao = models.CharField(max_length=50, blank=True, null=True)
    exclusao = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sicadfull'
        verbose_name = 'Registro SICAD'
        verbose_name_plural = 'Registros SICAD'

class Localidades(models.Model):
    risp = models.CharField(max_length=500, blank=True, null=True)
    municipios = models.CharField(max_length=500, blank=True, null=True)
    bairros = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localidades'
        verbose_name = 'Localidade'
        verbose_name_plural = 'Localidades'
        
class Consolidados(models.Model):
    consolidado = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consolidados'
        verbose_name = 'Crime Consolidado'
        verbose_name_plural = 'Crimes Consolidados'

# --- Novos Modelos para a Aplicação Phoenix ---

class SearchHistory(models.Model):
    """Armazena o histórico de pesquisas de um usuário."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='search_history'
    )
    search_type = models.CharField(max_length=100, verbose_name="Tipo de Pesquisa")
    search_query = models.JSONField(verbose_name="Parâmetros da Pesquisa")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data da Pesquisa")

    class Meta:
        verbose_name = 'Histórico de Pesquisa'
        verbose_name_plural = 'Históricos de Pesquisa'
        ordering = ['-timestamp']

class SavedItem(models.Model):
    """Armazena boletins ou procedimentos salvos por um usuário."""
    SAVED_TYPES = (
        ('BOP', 'Boletim de Ocorrência'),
        ('PROC', 'Procedimento'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='saved_items'
    )
    item_type = models.CharField(max_length=4, choices=SAVED_TYPES, verbose_name="Tipo de Item")
    item_id = models.CharField(max_length=100, verbose_name="Identificador do Item")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição Rápida")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data de Salvamento")

    class Meta:
        verbose_name = 'Item Salvo'
        verbose_name_plural = 'Itens Salvos'
        unique_together = ('user', 'item_type', 'item_id')
        ordering = ['-timestamp']