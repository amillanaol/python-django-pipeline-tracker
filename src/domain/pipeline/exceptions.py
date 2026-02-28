class InvalidPipelineTransitionError(Exception):
    def __init__(self, current_status: str, target_status: str) -> None:
        super().__init__(
            f"Cannot transition pipeline from '{current_status}' to '{target_status}'."
        )
        self.current_status = current_status
        self.target_status = target_status


class InvalidSeverityError(Exception):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid severity value: '{value}'.")
        self.value = value
