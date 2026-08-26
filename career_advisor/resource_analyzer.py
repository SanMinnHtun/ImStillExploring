"""Model 2 resource filtering and personalized roadmap formatting."""

from collections.abc import Iterable, Mapping
from typing import Any


_PHASES = (
    ("Phase 1: Foundations (Weeks 1-4)", ("foundation", "fundamental", "beginner", "intro", "basics")),
    ("Phase 2: Core Tools & Frameworks (Weeks 5-8)", ("core", "tool", "framework", "beginner", "intro")),
)


def _text_values(item: Mapping[str, Any], keys: tuple[str, ...]) -> str:
    values: list[str] = []
    for key in keys:
        value = item.get(key)
        if isinstance(value, str):
            values.append(value.lower())
        elif isinstance(value, Iterable) and not isinstance(value, (bytes, str, Mapping)):
            values.extend(str(entry).lower() for entry in value)
    return " ".join(values)


def _is_primary_field_item(item: Mapping[str, Any], primary_field: str) -> bool:
    searchable = _text_values(
        item,
        ("field", "category", "career_field", "track", "domain", "tags", "skills"),
    )
    if not searchable:
        return False

    field_terms = [term for term in primary_field.lower().replace("&", " ").split() if len(term) > 2]
    return any(term in searchable for term in field_terms)


def _is_advanced(item: Mapping[str, Any]) -> bool:
    level = _text_values(item, ("level", "skill_level", "difficulty", "experience_level"))
    return any(term in level for term in ("advanced", "expert", "senior"))


def _is_beginner(item: Mapping[str, Any]) -> bool:
    level = _text_values(item, ("level", "skill_level", "difficulty", "experience_level"))
    return not level or any(term in level for term in ("beginner", "intro", "foundation", "fundamental", "basic"))


def _is_project(item: Mapping[str, Any]) -> bool:
    kind = _text_values(item, ("type", "kind", "resource_type", "category"))
    return "project" in kind or "capstone" in kind


def _matches_phase(item: Mapping[str, Any], phase_terms: tuple[str, ...]) -> bool:
    phase = _text_values(item, ("phase",))
    if phase:
        return any(term in phase for term in phase_terms)
    return any(term in _text_values(item, ("type", "tags", "title")) for term in phase_terms)


def _item_line(item: Mapping[str, Any]) -> str:
    title = item.get("title")
    identifier = item.get("id")
    route = item.get("route")
    if not isinstance(title, str) or not title:
        raise ValueError("Each selected resource must provide a non-empty title")

    details = [title]
    if identifier is not None:
        details.append(f"ID: {identifier}")
    if isinstance(route, str) and route:
        details.append(f"Route: {route}")
    return "- " + " | ".join(details)


def analyze_resources(user_profile: Mapping[str, Any], available_app_resources: list[Mapping[str, Any]]) -> str:
    """Return a markdown learning path using only supplied internal resources."""
    primary_field = user_profile.get("primary_field")
    if not isinstance(primary_field, str) or not primary_field.strip():
        raise ValueError("user_profile.primary_field is required")

    matches = [
        item
        for item in available_app_resources
        if isinstance(item, Mapping)
        and _is_primary_field_item(item, primary_field)
        and not _is_advanced(item)
        and _is_beginner(item)
        and isinstance(item.get("title"), str)
        and item.get("title")
    ]

    foundation = [item for item in matches if not _is_project(item) and _matches_phase(item, _PHASES[0][1])]
    core = [item for item in matches if not _is_project(item) and item not in foundation and _matches_phase(item, _PHASES[1][1])]
    projects = [item for item in matches if _is_project(item)]

    # Keep the phases useful when the database omits phase labels: distribute remaining learning items in order.
    assigned = set(map(id, foundation + core + projects))
    remaining = [item for item in matches if id(item) not in assigned]
    split_at = (len(remaining) + 1) // 2
    foundation.extend(remaining[:split_at])
    core.extend(remaining[split_at:])

    capstone = projects[-1] if projects else None
    rationale = (
        f"Your diagnostic profile prioritizes {primary_field}, so this path selects matching internal resources. "
        "Beginner and foundational items come first, while advanced or unrelated resources are excluded."
    )
    lines = ["### Summary Rationale", rationale, "", "### Phase 1: Foundations (Weeks 1-4)"]
    lines.extend(_item_line(item) for item in foundation) if foundation else lines.append("- No matching internal foundation items available.")
    lines.extend(["", "### Phase 2: Core Tools & Frameworks (Weeks 5-8)"])
    lines.extend(_item_line(item) for item in core) if core else lines.append("- No matching internal core tool items available.")
    lines.extend(["", "### Phase 3: Applied Projects (Weeks 9-12)"])
    lines.append(_item_line(capstone) if capstone else "- No matching internal capstone project available.")
    return "\n".join(lines)
