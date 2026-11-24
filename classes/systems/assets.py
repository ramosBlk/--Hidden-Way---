from functools import lru_cache
from pathlib import Path

import pygame

RAIZ_PROJETO = Path(__file__).resolve().parents[2]


def carregar_imagem(caminho, tamanho=None, cor_fallback=(255, 0, 255), *, alpha=True, fallback=True):
    """
    Carrega uma imagem com cache. Caminhos relativos são resolvidos a partir da raiz do projeto.
    Com fallback=False, erros de arquivo são propagados para recursos obrigatórios.
    A superfície é compartilhada; copie-a antes de aplicar alterações.
    """
    caminho = Path(caminho)
    if not caminho.is_absolute():
        caminho = RAIZ_PROJETO / caminho
    tamanho = tuple(tamanho) if tamanho else None
    cor_fallback = tuple(cor_fallback)
    return _carregar_imagem(
        str(caminho.resolve()), tamanho, cor_fallback, alpha, fallback
    )


@lru_cache(maxsize=256)
def _carregar_imagem(caminho, tamanho, cor_fallback, alpha, fallback):
    try:
        img = pygame.image.load(caminho)
    except (pygame.error, OSError):
        if not fallback:
            raise
        print(f"[assets] não foi possível carregar '{caminho}' - usando fallback")
        img = pygame.Surface(tamanho or (32, 32), pygame.SRCALPHA)
        img.fill((*cor_fallback, 255))
        pygame.draw.rect(img, (0, 0, 0), img.get_rect(), 2)
        return img
    img = img.convert_alpha() if alpha else img.convert()
    if tamanho and img.get_size() != tuple(tamanho):
        img = pygame.transform.scale(img, tamanho)
    return img


def limpar_cache_imagens():
    _carregar_imagem.cache_clear()
