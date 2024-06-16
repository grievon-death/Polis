"""
Todos os utilitários da plataforma.
"""
from typing import Set

class Tool:
    """
    Ferramentas úteis.
    """
    @staticmethod
    def validate_request_query(query: dict, requireds: Set[str]) -> bool:
        """
        Valida os parâmetros das consultas REST.
        """
        _query_keys = tuple(query.keys())

        if any([k not in requireds for k in _query_keys]):
            return False
        elif not any([k in requireds for k in _query_keys]):
            return False
        return True
