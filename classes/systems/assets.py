import pygame


def carregar_imagem(caminho, tamanho=None, cor_fallback=(255, 0, 255)):
    """
    Carrega uma imagem com alpha. Se o arquivo não existir ou for inválido, devolve um
    retângulo colorido de fallback (o jogo nunca quebra por falta de asset).
    """
    try:
        img = pygame.image.load(caminho).convert_alpha()
    except (pygame.error, FileNotFoundError):
        print(f"[assets] não foi possível carregar '{caminho}' - usando fallback")
        img = pygame.Surface(tamanho or (32, 32), pygame.SRCALPHA)
        img.fill((*cor_fallback, 255))
        pygame.draw.rect(img, (0, 0, 0), img.get_rect(), 2)
        return img
    if tamanho and img.get_size() != tuple(tamanho):
        img = pygame.transform.scale(img, tamanho)
    return img
