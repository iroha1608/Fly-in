import re
import math


from Zone import Zone
from Gragh import Gragh


class Parser:
    """
    """
    def __init__(self) -> None:
        self.gragh = Gragh()

    def parse_metadata(self, metadata_str: str) -> dict[str, str]:
        metadata = {}
        if not metadata_str:
            return metadata

        content_match = re.search(r'\[(.*?)\]', metadata_str)
        if content_match:
            pairs = content_mach.group(1).split()
            fot pair in pairs:
                if "=" in pair:
                    key, value = pair.split('=', 1)
                    metadata[key] = value
        return metadata

    def parse_file(self, filepath: str) -> Gragh:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.split("#")[0].strip()
                if not line:
                    continue

                if line.startswith("nb_drones"):
                    self.gragh.nb_drones = int(line.split(":")[1].strip())
                    continue

                if line.startswith(("start_hub:", "end_hub:", "hub:")):
                    parts = line.split(":", 1)[1].strip().split("[", 1)
                    base_info = parts[0].split()
                    name = base_info[0]
                    x, y = int(base_info[1]), int(base_info[2])

                    meta = self.parse_metadata(f"[{parts[1]}]" if len(parts) > 1 else "")

                    is_start = line.startswith("start_hub:")
                    max_drones = math.inf if is_start else float(meta.get("max_drones", 1.0))

                    zone = Zone(
                        name=name,
                        x=x,
                        y=y,
                        zone_type=meta.get("zone", "normal"),
                        color=meta.get("color"),
                        max_drones=max_drones
                    )

                    self.gragh.add_zone(zone)
                    if is_start:
                        self.gragh.start_zone = zone
                    elif line.startswith("end_hub"):
                        self.gragh.end_zone = zone

                elif line.startswith("connection:"):
                    parts = line.split(":", 1)[1].strip().split("[", 1)
                    name1, name2 = parts[0].strip().split("-")

                    meta = self.parse_metadata(f"[{parts[1]}]" if len(parts) > 1 else "")
                    capacity = int(meta.get("max_link_capacity", 1))

                    self.gragh.add_connection(name1, name2, capacity)

            return self.gragh
