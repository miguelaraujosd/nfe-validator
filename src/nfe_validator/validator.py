"""Motor de validação da Nota Fiscal.

Cada função referencia a regra de negócio (RNxx) da SPEC.md que implementa.
"""
from datetime import date, datetime, timedelta
from typing import List

from .models import ErroValidacao, NotaFiscal, ResultadoValidacao

TOLERANCIA_CENTAVOS = 0.01
LIMITE_VALOR_ALTO = 100_000.00
ANOS_MAXIMO_RETROATIVO = 5


def _somente_digitos(valor: str) -> str:
    return "".join(c for c in valor if c.isdigit())


def _digito_verificador_cpf(cpf: str) -> bool:
    if len(set(cpf)) == 1:
        return False

    def calc_digito(cpf_parcial: str) -> int:
        peso = len(cpf_parcial) + 1
        soma = sum(int(d) * (peso - i) for i, d in enumerate(cpf_parcial))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    d1 = calc_digito(cpf[:9])
    d2 = calc_digito(cpf[:9] + str(d1))
    return cpf[-2:] == f"{d1}{d2}"


def _digito_verificador_cnpj(cnpj: str) -> bool:
    if len(set(cnpj)) == 1:
        return False

    def calc_digito(cnpj_parcial: str, pesos: List[int]) -> int:
        soma = sum(int(d) * p for d, p in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = calc_digito(cnpj[:12], pesos1)
    d2 = calc_digito(cnpj[:12] + str(d1), pesos2)
    return cnpj[-2:] == f"{d1}{d2}"


def validar_documento(documento: str) -> bool:
    """RN05 — Valida CPF (11 dígitos) ou CNPJ (14 dígitos)."""
    digitos = _somente_digitos(documento)
    if len(digitos) == 11:
        return _digito_verificador_cpf(digitos)
    if len(digitos) == 14:
        return _digito_verificador_cnpj(digitos)
    return False


def calcular_totais(nota: NotaFiscal) -> tuple[float, float]:
    """RN01 e RN02 — retorna (valor_calculado, icms_total)."""
    valor_calculado = 0.0
    icms_total = 0.0
    for item in nota.itens:
        subtotal = item.quantidade * item.valor_unitario
        valor_calculado += subtotal
        icms_total += subtotal * item.aliquota_icms
    return round(valor_calculado, 2), round(icms_total, 2)


def validar_campos_obrigatorios(nota: NotaFiscal) -> List[ErroValidacao]:
    erros: List[ErroValidacao] = []

    if not nota.numero:
        erros.append(ErroValidacao("numero", "campo_obrigatorio", "Número da nota é obrigatório."))
    if not nota.serie:
        erros.append(ErroValidacao("serie", "campo_obrigatorio", "Série é obrigatória."))
    if not nota.emitente or not nota.emitente.razao_social:
        erros.append(ErroValidacao("emitente.razao_social", "campo_obrigatorio", "Razão social do emitente é obrigatória."))
    if not nota.destinatario or not nota.destinatario.nome:
        erros.append(ErroValidacao("destinatario.nome", "campo_obrigatorio", "Nome do destinatário é obrigatório."))
    if not nota.itens:
        erros.append(ErroValidacao("itens", "campo_obrigatorio", "A nota deve conter ao menos um item."))

    for i, item in enumerate(nota.itens or []):
        if not item.descricao:
            erros.append(ErroValidacao(f"itens[{i}].descricao", "campo_obrigatorio", "Descrição do item é obrigatória."))
        if item.quantidade is None or item.quantidade <= 0:
            erros.append(ErroValidacao(f"itens[{i}].quantidade", "campo_invalido", "Quantidade deve ser maior que zero."))
        if item.valor_unitario is None or item.valor_unitario <= 0:
            erros.append(ErroValidacao(f"itens[{i}].valor_unitario", "campo_invalido", "Valor unitário deve ser maior que zero."))
        if item.aliquota_icms is None or not (0 <= item.aliquota_icms <= 1):
            erros.append(ErroValidacao(f"itens[{i}].aliquota_icms", "campo_invalido", "Alíquota de ICMS deve estar entre 0 e 1."))

    return erros


def validar_regras_negocio(nota: NotaFiscal, valor_calculado: float) -> List[ErroValidacao]:
    erros: List[ErroValidacao] = []

    # RN01
    diferenca = round(abs(nota.valor_total_declarado - valor_calculado), 2)
    if diferenca > TOLERANCIA_CENTAVOS:
        erros.append(ErroValidacao(
            "valor_total_declarado", "RN01",
            f"Valor declarado ({nota.valor_total_declarado:.2f}) difere do "
            f"valor calculado ({valor_calculado:.2f})."
        ))

    # RN03
    if nota.valor_total_declarado > LIMITE_VALOR_ALTO and not nota.autorizacao_especial:
        erros.append(ErroValidacao(
            "autorizacao_especial", "RN03",
            "Notas acima de R$ 100.000,00 exigem autorizacao_especial=true."
        ))

    # RN04
    try:
        data_emissao = datetime.strptime(nota.data_emissao, "%Y-%m-%d").date()
        hoje = date.today()
        if data_emissao > hoje:
            erros.append(ErroValidacao("data_emissao", "RN04", "Data de emissão não pode ser futura."))
        elif data_emissao < hoje - timedelta(days=365 * ANOS_MAXIMO_RETROATIVO):
            erros.append(ErroValidacao("data_emissao", "RN04", "Data de emissão está vencida (mais de 5 anos)."))
    except (ValueError, TypeError):
        erros.append(ErroValidacao("data_emissao", "campo_invalido", "Data de emissão em formato inválido (esperado YYYY-MM-DD)."))

    # RN05
    if nota.destinatario and nota.destinatario.documento:
        if not validar_documento(nota.destinatario.documento):
            erros.append(ErroValidacao("destinatario.documento", "RN05", "CPF/CNPJ do destinatário é inválido."))

    return erros


def validar_nota_fiscal(nota: NotaFiscal) -> ResultadoValidacao:
    """Orquestra todas as validações e retorna o resultado consolidado."""
    erros = validar_campos_obrigatorios(nota)

    valor_calculado, icms_total = calcular_totais(nota)

    if nota.numero and nota.itens:
        erros += validar_regras_negocio(nota, valor_calculado)

    return ResultadoValidacao(
        valido=len(erros) == 0,
        erros=erros,
        valor_calculado=valor_calculado,
        icms_total=icms_total,
    )
