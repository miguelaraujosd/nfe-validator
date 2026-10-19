"""CLI simples: python -m nfe_validator.cli caminho/para/nota.json"""
import json
import sys

from .models import Destinatario, Emitente, ItemNota, NotaFiscal
from .validator import validar_nota_fiscal


def carregar_nota(caminho: str) -> NotaFiscal:
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)

    emitente = Emitente(**dados["emitente"])
    destinatario = Destinatario(**dados["destinatario"])
    itens = [ItemNota(**item) for item in dados.get("itens", [])]

    return NotaFiscal(
        numero=dados.get("numero", ""),
        serie=dados.get("serie", ""),
        data_emissao=dados.get("data_emissao", ""),
        emitente=emitente,
        destinatario=destinatario,
        itens=itens,
        valor_total_declarado=dados.get("valor_total_declarado", 0.0),
        autorizacao_especial=dados.get("autorizacao_especial", False),
    )


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python -m nfe_validator.cli <arquivo.json>")
        sys.exit(1)

    nota = carregar_nota(sys.argv[1])
    resultado = validar_nota_fiscal(nota)
    print(json.dumps(resultado.to_dict(), indent=2, ensure_ascii=False))
    sys.exit(0 if resultado.valido else 1)


if __name__ == "__main__":
    main()
