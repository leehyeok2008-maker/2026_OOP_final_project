import pygame
from pygame import Vector2
from entities.entity import Entity
from physics import Collider, RectCollider, CircleCollider


class ColliderManager:
    '''
    self._entries: Entity와 대응하는 Collider의 딕셔너리
    register를 통해 _entries 업데이트
    check_all을 통해 on_collision 실행
    '''
    def __init__(self):
        self._entries: dict[Entity, Collider] = {}

    # ── 등록 / 해제 ──────────────────────────────────────────

    def register(self, entity: Entity, collider: Collider):
        self._entries[entity] = collider

    def unregister(self, entity: Entity):
        self._entries.pop(entity, None)

    def clear(self):
        self._entries.clear()

    # ── 충돌 감지 ────────────────────────────────────────────

    def check_all(self):
        entries = list(self._entries.items())

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                ea, ca = entries[i]
                eb, cb = entries[j]
                if self._intersects(ca, cb):
                    ea.on_collision(eb)
                    eb.on_collision(ea)

    def check_one(self, entity: Entity) -> list[Entity]:
        if entity not in self._entries:
            return []
        ca = self._entries[entity]
        return [
            other for other, cb in self._entries.items()
            if other is not entity and self._intersects(ca, cb)
        ]

    def are_colliding(self, entity_a: Entity, entity_b: Entity) -> bool:
        ca = self._entries.get(entity_a)
        cb = self._entries.get(entity_b)
        if ca is None or cb is None:
            return False
        return self._intersects(ca, cb)

    # ── 충돌 판정 ─────────────────────────────────────────────

    def _intersects(self, a: Collider, b: Collider) -> bool:
        if isinstance(a, RectCollider) and isinstance(b, RectCollider):
            return self._rect_rect(a, b)
        if isinstance(a, RectCollider) and isinstance(b, CircleCollider):
            return self._rect_circle(a, b)
        if isinstance(a, CircleCollider) and isinstance(b, RectCollider):
            return self._rect_circle(b, a)
        if isinstance(a, CircleCollider) and isinstance(b, CircleCollider):
            return self._circle_circle(a, b)
        return False

    def _rect_rect(self, a: RectCollider, b: RectCollider) -> bool:
        dist = b.position -a.position

        vecs = [
            a.width_vector,
            a.height_vector,
            b.width_vector,
            b.height_vector,
        ]

        for vec in vecs:
            unit = vec.normalize()
            projection_sum = sum(abs(v.dot(unit)) for v in vecs)
            if abs(dist.dot(unit)) > projection_sum:
                return False

        return True

    def _rect_circle(self, rect: RectCollider, circle: CircleCollider) -> bool:
        diff = (circle.transform.position + circle.offset) \
             - (rect.transform.position + rect.offset)
        local_x = diff.dot(rect.width_vector.normalize())
        local_y = diff.dot(rect.height_vector.normalize())

        closest_x = max(-rect.width / 2, min(local_x, rect.width / 2))
        closest_y = max(-rect.height / 2, min(local_y, rect.height / 2))

        dist_sq = (local_x - closest_x) ** 2 + (local_y - closest_y) ** 2
        return dist_sq < circle.radius ** 2

    def _circle_circle(self, a: CircleCollider, b: CircleCollider) -> bool:
        pos_a = a.transform.position + a.offset
        pos_b = b.transform.position + b.offset
        return pos_a.distance_to(pos_b) < a.radius + b.radius

    # ── 디버그 렌더링 ─────────────────────────────────────────

    def render_debug(self, screen: pygame.Surface, px_per_meter: float):
        for collider in self._entries.values():
            if isinstance(collider, RectCollider):
                self._render_rect(screen, collider, px_per_meter)
            elif isinstance(collider, CircleCollider):
                self._render_circle(screen, collider, px_per_meter)

    def _render_rect(self, screen: pygame.Surface,
                     collider: RectCollider, ppm: float):
        c = collider.transform.position + collider.offset
        w = collider.width_vector
        h = collider.height_vector
        corners = [
            ((c + w + h).x * ppm, (c + w + h).y * ppm),
            ((c - w + h).x * ppm, (c - w + h).y * ppm),
            ((c - w - h).x * ppm, (c - w - h).y * ppm),
            ((c + w - h).x * ppm, (c + w - h).y * ppm),
        ]
        pygame.draw.polygon(screen, (0, 255, 0), corners, 1)

    def _render_circle(self, screen: pygame.Surface,
                       collider: CircleCollider, ppm: float):
        pos = collider.transform.position + collider.offset
        center = (int(pos.x * ppm), int(pos.y * ppm))
        radius = int(collider.radius * ppm)
        pygame.draw.circle(screen, (0, 255, 0), center, radius, 1)