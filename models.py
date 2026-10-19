"""Estruturas de dados da Nota Fiscal (ver SPEC.md, seção 3)."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Emitente:
    cnpj: str
    razao_social: str


@dataclass
class Destinatario:
    documento: str
    nome: str


@dataclass
class ItemNota:
    descricao: str
    quantidade: float
    valor_unitario: float
    aliquota_icms: float


@dataclass
class NotaFiscal:
    numero: str
    serie: str
    data_emissao: str
    emitente: Emitente
    destinatario: Destinatario
    itens: List[ItemNota] = field(default_factory=list)
    valor_total_declarado: float = 0.0
    autorizacao_especial: Optional[bool] = False


@dataclass
class ErroValidacao:
    campo: str
    regra: str
    mensagem: str


@dataclass
class ResultadoValidacao:
    valido: bool
    erros: List[ErroValidacao] = field(default_factory=list)
    valor_calculado: Optional[float] = None
    icms_total: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "valido": self.valido,
            "erros": [
                {"campo": e.campo, "regra": e.regra, "mensagem": e.mensagem}
                for e in self.erros
            ],
            "valor_calculado": self.valor_calculado,
            "icms_total": self.icms_total,
        }
