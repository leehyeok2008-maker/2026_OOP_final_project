import math
import pygame
from pygame import Vector2
from entities import Entity, StaticEntity, DynamicEntity
from physics import Collider, RectCollider, RigidBody2D
from collections.abc import Iterable


class ColliderManager:
    '''
    self._entries: Entity와 대응하는 Collider의 딕셔너리
    register를 통해 _entries 업데이트
    check_all을 통해 on_collision 실행
    '''
    def __init__(self):
        self._entries: dict[Entity, Collider] = {}

    #region 등록 및 해제
    def register(self, entity: Entity, collider: Collider):
        self._entries[entity] = collider

    def register_all(self, entries : dict[Entity, Collider] | Iterable[tuple[Entity, Collider]]):
        self._entries.update(entries)

    def unregister(self, entity: Entity):
        self._entries.pop(entity, None)

    def clear(self):
        self._entries.clear()
    #endregion

    #region 충돌 감지
    def check_all(self):
        entries = list(self._entries.items())
        dynamics = []
        statics = []

        for ea, ca in entries:
            if isinstance(ea, DynamicEntity): dynamics.append((ea, ca))
            else: statics.append((ea, ca))

        for ea, ca in dynamics:
            for eb, cb in entries:
                if (ea.transform.position - eb.transform.position).length_squared() > (ca.max_distance + cb.max_distance) ** 2:
                    continue
                collision_info = self.do_intersect(ca, cb)
                if (collision_info is not None):
                    self.handle_collision_response(ea, eb, collision_info)
                    ea.on_collision(eb)
                    eb.on_collision(ea)

    def check_one(self, entity: Entity) -> list[Entity]:
        if entity not in self._entries:
            return []
        ca = self._entries[entity]
        return [
            other for other, cb in self._entries.items()
            if other is not entity and self.do_intersect(ca, cb)
        ]

    def are_colliding(self, entity_a: Entity, entity_b: Entity) -> bool:
        ca = self._entries.get(entity_a)
        cb = self._entries.get(entity_b)
        if ca is None or cb is None:
            return False
        return self.do_intersect(ca, cb) is not None
    #endregion
    
    #region 충돌 판정
    def do_intersect(self, a: Collider, b: Collider) -> dict | None:
        if isinstance(a, RectCollider) and isinstance(b, RectCollider):
            return self._rect_rect(a, b)
        else:
            return None

    def _rect_rect(self, a: RectCollider, b: RectCollider) -> dict | None:
        
        displacement = b.position - a.position

        axes = []
        for vec in [a.width_vector, a.height_vector, b.width_vector, b.height_vector]:
            if vec.length_squared() > 0:
                axes.append(Vector2.normalize(vec))

        min_overlap = float('inf')
        mtv_axis = Vector2(0, 0)

        for axis in axes:
            r_a = abs(a.width_vector.dot(axis)) + abs(a.height_vector.dot(axis))
            r_b = abs(b.width_vector.dot(axis)) + abs(b.height_vector.dot(axis))
            
            projection_sum = r_a + r_b
            distance = abs(displacement.dot(axis))
            if distance > projection_sum:
                return None
            
            overlap = projection_sum - distance

            if overlap < min_overlap:
                min_overlap = overlap
                mtv_axis = axis

        # a에서 b로 가는 방향
        if displacement.dot(mtv_axis) < 0:
            mtv_axis = -mtv_axis

        contact_points = []

        pts_a = [
            a.position + a.width_vector + a.height_vector,
            a.position + a.width_vector - a.height_vector,
            a.position - a.width_vector + a.height_vector,
            a.position - a.width_vector - a.height_vector
        ]
        pts_b = [
            b.position + b.width_vector + b.height_vector,
            b.position + b.width_vector - b.height_vector,
            b.position - b.width_vector + b.height_vector,
            b.position - b.width_vector - b.height_vector
        ]

        # 내부 판정 보조 함수
        def is_point_inside_rect(p, rect):
            local_p = p - rect.position
            ax = rect.width_vector.normalize() if rect.width_vector.length_squared() > 0 else Vector2(1, 0)
            ay = rect.height_vector.normalize() if rect.height_vector.length_squared() > 0 else Vector2(0, 1)
            return (abs(local_p.dot(ax)) <= rect.width_vector.length() + 0.01 and 
                    abs(local_p.dot(ay)) <= rect.height_vector.length() + 0.01)

        for p in pts_a:
            if is_point_inside_rect(p, b): contact_points.append(p)
        for p in pts_b:
            if is_point_inside_rect(p, a): contact_points.append(p)

        # 평균 작용점 산출 및 예외 처리
        if len(contact_points) > 0:
            final_contact = sum(contact_points, Vector2(0, 0)) / len(contact_points)
        else:
            final_contact = (a.position + b.position) * 0.5

        return {
            "overlap" : min_overlap,
            "normal" : mtv_axis,
            "vector" : mtv_axis * min_overlap,
            "contact": final_contact
        }
    #endregion

    #region 충돌 반응
    def handle_collision_response(self, ea : Entity, eb : Entity, collision_info : dict):
        if not ea.is_solid or not eb.is_solid:
            return

        is_ea_dynamic = isinstance(ea, DynamicEntity)
        is_eb_dynamic = isinstance(eb, DynamicEntity)

        # 정적 물체의 collision
        if not is_ea_dynamic and not is_eb_dynamic:
            return

        # 동적 물체와 정적 물체의 collision
        elif is_ea_dynamic and not is_eb_dynamic:
            ea.transform.position -= collision_info["vector"]

        # 정적 물체와 동적 물체의 collision
        elif not is_ea_dynamic and is_eb_dynamic:
            eb.transform.position += collision_info["vector"]

        # 동적 물체와 동적 물체의 collision
        elif is_ea_dynamic and is_eb_dynamic:
            ea.transform.position -= collision_info["vector"] * 0.5
            eb.transform.position += collision_info["vector"] * 0.5

        contact = collision_info["contact"]
        normal = collision_info["normal"]

        r_a = contact - ea.transform.position
        r_b = contact - eb.transform.position

        vel_a = ea.rigidbody.velocity + RigidBody2D.cross(ea.rigidbody.angular_velocity, r_a) if is_ea_dynamic else Vector2(0, 0)
        vel_b = eb.rigidbody.velocity + RigidBody2D.cross(eb.rigidbody.angular_velocity, r_b) if is_eb_dynamic else Vector2(0, 0)
        
        relative_velocity = vel_b - vel_a
        vel_along_normal = relative_velocity.dot(normal)

        if vel_along_normal > 0:
            return

        e = 0.3

        inv_mass_a = (1.0 / ea.rigidbody.mass) if (is_ea_dynamic and ea.rigidbody.mass > 0) else 0.0
        inv_mass_b = (1.0 / eb.rigidbody.mass) if (is_eb_dynamic and eb.rigidbody.mass > 0) else 0.0

        inv_inertia_a = (1.0 / ea.rigidbody.moment) if (is_ea_dynamic and ea.rigidbody.moment > 0) else 0.0
        inv_inertia_b = (1.0 / eb.rigidbody.moment) if (is_eb_dynamic and eb.rigidbody.moment > 0) else 0.0

        r_a_cross_n = RigidBody2D.cross(r_a, normal)
        r_b_cross_n = RigidBody2D.cross(r_b, normal)

        denominator = inv_mass_a + inv_mass_b
        denominator += (r_a_cross_n ** 2) * inv_inertia_a
        denominator += (r_b_cross_n ** 2) * inv_inertia_b

        if denominator == 0:
            return
        
        impulse_scalar = -(1.0 + e) * vel_along_normal / denominator
        impulse_vector = impulse_scalar * normal

        if is_ea_dynamic:
            ea.rigidbody.apply_impulse(-impulse_vector, point=contact, is_local=False)

        if is_eb_dynamic:
            eb.rigidbody.apply_impulse(impulse_vector, point=contact, is_local=False)
    #endregion