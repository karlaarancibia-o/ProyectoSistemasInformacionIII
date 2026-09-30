from app.domain.entities.lote_dosis import LoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


class ListarLotesDosis:
    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self) -> list[LoteDosis]:
        return self.repo.listar()
