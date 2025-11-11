from src.buddy import models


def center(rect: models.objects.Rectangle) -> models.objects.Position:
    return models.objects.Position(
        int(rect.position.x + rect.size.width / 2), int(rect.position.y + rect.size.height / 2))


def normalize(position: models.objects.Position, reference: models.objects.Size) -> models.objects.Position:
    return models.objects.Position(
        position.x / reference.width,
        position.y / reference.height
    )
