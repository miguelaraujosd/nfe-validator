"""Suíte de testes do validador de Notas Fiscais.

Cada teste referencia o item correspondente da seção 6 (Casos de Borda) da
SPEC.md.
"""
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nfe_validator.models import Destinatario, Emitente, ItemNota, NotaFiscal
from nfe_validator.validator import validar_documento, validar_nota_fiscal

CPF_VALIDO = "52998224725"
CNPJ_VALIDO = "11222333000181"


def nota_base(**overrides) -> NotaFiscal:
    """Fábrica de uma nota válida, para os testes sobrescreverem só o necessário."""
    padrao = dict(
        numero="000123",
        serie="1",
        data_emissao=date.today().isoformat(),
        emitente=Emitente(cnpj=CNPJ_VALIDO, razao_social="Empresa Exemplo LTDA"),
        destinatario=Destinatario(documento=CPF_VALIDO, nome="Cliente Exemplo"),
        itens=[ItemNota(descricao="Produto A", quantidade=2, valor_unitario=50.00, aliquota_icms=0.18)],
        valor_total_declarado=100.00,
        autorizacao_especial=False,
    )
    padrao.update(overrides)
    return NotaFiscal(**padrao)


# ---------------------------------------------------------------------------
# Caso principal: nota totalmente válida
# ---------------------------------------------------------------------------

def test_nota_valida_passa_sem_erros():
    resultado = validar_nota_fiscal(nota_base())
    assert resultado.valido is True
    assert resultado.erros == []
    assert resultado.valor_calculado == 100.00
    assert resultado.icms_total == 18.00


# ---------------------------------------------------------------------------
# Edge case 1 — nota sem itens
# ---------------------------------------------------------------------------

def test_edge_1_nota_sem_itens_invalida():
    resultado = validar_nota_fiscal(nota_base(itens=[]))
    assert resultado.valido is False
    assert any(e.campo == "itens" for e in resultado.erros)


# ---------------------------------------------------------------------------
# Edge case 2 — quantidade/valor unitário inválidos
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("quantidade,valor_unitario", [(-1, 50.0), (0, 50.0), (2, 0), (2, -10)])
def test_edge_2_item_com_quantidade_ou_valor_invalido(quantidade, valor_unitario):
    item = ItemNota(descricao="X", quantidade=quantidade, valor_unitario=valor_unitario, aliquota_icms=0.1)
    resultado = validar_nota_fiscal(nota_base(itens=[item]))
    assert resultado.valido is False


# ---------------------------------------------------------------------------
# Edge case 3 — alíquota de ICMS fora do intervalo
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("aliquota", [1.5, -0.1])
def test_edge_3_aliquota_icms_fora_do_intervalo(aliquota):
    item = ItemNota(descricao="X", quantidade=1, valor_unitario=10, aliquota_icms=aliquota)
    resultado = validar_nota_fiscal(nota_base(itens=[item]))
    assert resultado.valido is False
    assert any(e.regra == "campo_invalido" for e in resultado.erros)


# ---------------------------------------------------------------------------
# Edge case 4 — tolerância de arredondamento no valor total (RN01)
# ---------------------------------------------------------------------------

def test_edge_4_diferenca_de_um_centavo_passa():
    resultado = validar_nota_fiscal(nota_base(valor_total_declarado=100.01))
    assert resultado.valido is True


def test_edge_4_diferenca_de_dois_centavos_falha():
    resultado = validar_nota_fiscal(nota_base(valor_total_declarado=100.02))
    assert resultado.valido is False
    assert any(e.regra == "RN01" for e in resultado.erros)


# ---------------------------------------------------------------------------
# Edge case 5 — CPF/CNPJ com todos os dígitos iguais
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("documento", ["11111111111", "11111111000111"])
def test_edge_5_documento_com_digitos_repetidos_invalido(documento):
    assert validar_documento(documento) is False


def test_documento_valido_cpf_e_cnpj():
    assert validar_documento(CPF_VALIDO) is True
    assert validar_documento(CNPJ_VALIDO) is True


# ---------------------------------------------------------------------------
# Edge case 6 e 7 — datas de emissão inválidas (RN04)
# ---------------------------------------------------------------------------

def test_edge_6_data_emissao_futura_invalida():
    data_futura = (date.today() + timedelta(days=10)).isoformat()
    resultado = validar_nota_fiscal(nota_base(data_emissao=data_futura))
    assert resultado.valido is False
    assert any(e.regra == "RN04" for e in resultado.erros)


def test_edge_7_data_emissao_vencida_invalida():
    data_antiga = (date.today() - timedelta(days=365 * 6)).isoformat()
    resultado = validar_nota_fiscal(nota_base(data_emissao=data_antiga))
    assert resultado.valido is False
    assert any(e.regra == "RN04" for e in resultado.erros)


# ---------------------------------------------------------------------------
# Edge case 8 e 9 — limite de valor alto (RN03)
# ---------------------------------------------------------------------------

def test_edge_8_valor_exatamente_no_limite_nao_exige_autorizacao():
    item = ItemNota(descricao="X", quantidade=1000, valor_unitario=100.0, aliquota_icms=0.1)
    resultado = validar_nota_fiscal(nota_base(itens=[item], valor_total_declarado=100000.00))
    assert not any(e.regra == "RN03" for e in resultado.erros)


def test_edge_9_valor_acima_do_limite_sem_autorizacao_falha():
    item = ItemNota(descricao="X", quantidade=1000, valor_unitario=100.01, aliquota_icms=0.1)
    resultado = validar_nota_fiscal(nota_base(itens=[item], valor_total_declarado=100010.00, autorizacao_especial=False))
    assert resultado.valido is False
    assert any(e.regra == "RN03" for e in resultado.erros)


def test_edge_9_valor_acima_do_limite_com_autorizacao_passa_rn03():
    item = ItemNota(descricao="X", quantidade=1000, valor_unitario=100.01, aliquota_icms=0.1)
    resultado = validar_nota_fiscal(nota_base(itens=[item], valor_total_declarado=100010.00, autorizacao_especial=True))
    assert not any(e.regra == "RN03" for e in resultado.erros)


# ---------------------------------------------------------------------------
# Edge case 10 — campos obrigatórios ausentes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("campo,valor", [("numero", ""), ("serie", "")])
def test_edge_10_campo_obrigatorio_ausente(campo, valor):
    resultado = validar_nota_fiscal(nota_base(**{campo: valor}))
    assert resultado.valido is False
    assert any(e.campo == campo for e in resultado.erros)


def test_edge_10_razao_social_emitente_ausente():
    resultado = validar_nota_fiscal(nota_base(emitente=Emitente(cnpj=CNPJ_VALIDO, razao_social="")))
    assert resultado.valido is False


def test_edge_10_nome_destinatario_ausente():
    resultado = validar_nota_fiscal(nota_base(destinatario=Destinatario(documento=CPF_VALIDO, nome="")))
    assert resultado.valido is False
