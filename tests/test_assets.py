import pygame
import pytest

from classes.systems.assets import carregar_imagem, limpar_cache_imagens


def test_image_loader_reuses_cached_surface():
    limpar_cache_imagens()
    caminho = "assets/sprites/itens/chave.png"

    primeira = carregar_imagem(caminho, (39, 21))
    segunda = carregar_imagem(caminho, (39, 21))

    assert primeira is segunda
    assert primeira.get_size() == (39, 21)
    limpar_cache_imagens()


def test_missing_optional_image_uses_fallback_and_required_image_raises():
    limpar_cache_imagens()
    missing = "assets/sprites/nao-existe.png"

    imagem = carregar_imagem(missing, (16, 12))

    assert imagem.get_size() == (16, 12)
    assert imagem.get_at((8, 6)) == pygame.Color(255, 0, 255, 255)
    with pytest.raises((pygame.error, OSError)):
        carregar_imagem(missing, fallback=False)
    limpar_cache_imagens()


def test_relative_image_path_is_independent_of_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    image = carregar_imagem("assets/sprites/itens/chave.png", (39, 21))

    assert image.get_size() == (39, 21)
