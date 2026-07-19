from typing import Protocol


class RuntimeHooks(Protocol):
    def before_journey(self, journey_id: str, context: object) -> None: ...
    def after_journey(self, journey_id: str, context: object) -> None: ...
    def before_mission(self, mission_id: str, context: object) -> None: ...
    def after_mission(self, mission_id: str, context: object) -> None: ...
    def before_assessment(self, mission_id: str, context: object) -> None: ...
    def after_assessment(self, mission_id: str, context: object) -> None: ...


class NoopHooks:
    def before_journey(self, journey_id: str, context: object) -> None:
        pass

    def after_journey(self, journey_id: str, context: object) -> None:
        pass

    def before_mission(self, mission_id: str, context: object) -> None:
        pass

    def after_mission(self, mission_id: str, context: object) -> None:
        pass

    def before_assessment(self, mission_id: str, context: object) -> None:
        pass

    def after_assessment(self, mission_id: str, context: object) -> None:
        pass
