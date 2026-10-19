"""Testes complementares (Entrega 3): ramos de erro, serialização e CLI.

Adicionados após a medição de cobertura para cobrir caminhos que a suíte
inicial não exercitava (ver docs/COVERAGE_REPORT.md).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nfe_validator import cli
from nfe_validator.models import Destinatario, Emitente, ItemNota, NotaFiscal
from nfe_validator.validator import validar_documento, validar_nota_fiscal

from test_validator import CNPJ_VALIDO, CPF_VALIDO, nota_base

EXEMPLOS = Path(__file__).parent.parent / "exemplos"


# --- RN05: ramos de documento inválido --------------------------------------

def test_rn05_cnpj_com_todos_digitos_iguais_invalido():
    assert validar_documento("11111111111111") is False


@pytest.mark.parametrize("documento", ["123", "", "123456789012345"])
def test_rn05_documento_com_tamanho_invalido(documento):
    assert validar_documento(documento) is False


def test_rn05_documento_com_digito_verificador_errado_na_nota():
    nota = nota_base(destinatario=Destinatario(documento="52998224726", nome="Cliente"))
    resultado = validar_nota_fiscal(nota)
    assert resultado.valido is False
    assert any(e.regra == "RN05" for e in resultado.erros)


def test_rn05_documento_formatado_com_pontuacao_e_aceito():
    assert validar_documento("529.982.247-25") is True
    assert validar_documento("11.222.333/0001-81") is True


# --- Campos obrigatórios e data ---------------------------------------------

def test_item_sem_descricao_invalido():
    item = ItemNota(descricao="", quantidade=1, valor_unitario=10, aliquota_icms=0.1)
    resultado = validar_nota_fiscal(nota_base(itens=[item], valor_total_declarado=10.0))
    assert resultado.valido is False
    assert any(e.campo == "itens[0].descricao" for e in resultado.erros)


@pytest.mark.parametrize("data", ["10/09/2026", "2026-13-40", "abc", ""])
def test_data_emissao_em_formato_invalido(data):
    resultado = validar_nota_fiscal(nota_base(data_emissao=data))
    assert resultado.valido is False
    assert any(e.campo == "data_emissao" for e in resultado.erros)


# --- Serialização do resultado ----------------------------------------------

def test_resultado_to_dict_segue_contrato_de_saida():
    resultado = validar_nota_fiscal(nota_base(valor_total_declarado=999.0))
    saida = resultado.to_dict()
    assert set(saida) == {"valido", "erros", "valor_calculado", "icms_total"}
    assert saida["valido"] is False
    assert saida["erros"][0] == {
        "campo": "valor_total_declarado",
        "regra": "RN01",
        "mensagem": saida["erros"][0]["mensagem"],
    }


# --- CLI --------------------------------------------------------------------

def test_cli_carregar_nota_le_arquivo_json():
    nota = cli.carregar_nota(str(EXEMPLOS / "nota_valida.json"))
    assert isinstance(nota, NotaFiscal)
    assert nota.numero == "000123"
    assert len(nota.itens) == 1


def test_cli_nota_valida_retorna_exit_0(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["cli", str(EXEMPLOS / "nota_valida.json")])
    with pytest.raises(SystemExit) as saida:
        cli.main()
    assert saida.value.code == 0
    assert json.loads(capsys.readouterr().out)["valido"] is True


@pytest.mark.parametrize("arquivo,regra", [
    ("nota_cpf_invalido.json", "RN05"),
    ("nota_valor_alto_sem_autorizacao.json", "RN03"),
    ("nota_sem_itens.json", "campo_obrigatorio"),
])
def test_cli_nota_invalida_retorna_exit_1_e_regra_violada(monkeypatch, capsys, arquivo, regra):
    monkeypatch.setattr(sys, "argv", ["cli", str(EXEMPLOS / arquivo)])
    with pytest.raises(SystemExit) as saida:
        cli.main()
    assert saida.value.code == 1
    resultado = json.loads(capsys.readouterr().out)
    assert resultado["valido"] is False
    assert any(e["regra"] == regra for e in resultado["erros"])


def test_cli_sem_argumento_mostra_uso_e_retorna_exit_1(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["cli"])
    with pytest.raises(SystemExit) as saida:
        cli.main()
    assert saida.value.code == 1
    assert "Uso:" in capsys.readouterr().out
