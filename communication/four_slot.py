from dataclasses import dataclass, field
from typing import Any

@dataclass
class FourSlot:
    latest: int = 0
    reading: int = 0

    # which index (0 or 1) is current for each pair
    slot: list[int] = field(default_factory=lambda: [0, 0])

    # actual storage: 2 pairs x 2 slots each
    data: list[list[Any]] = field(
        default_factory=lambda: [[None, None], [None, None]]
    )

    def write(self, value: Any) -> None:
        pair = not self.latest     
        index = not self.slot[pair]

        self.data[pair][index] = value
        self.slot[pair] = index
        self.latest = pair

    def read(self) -> Any:
        pair = self.latest
        self.reading = pair
        index = self.slot[pair]

        return self.data[pair][index]
