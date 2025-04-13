# indicators/volume.py

def is_volume_spike(current_volume: float, recent_volumes: list[float], multiplier: float = 3.0) -> bool:
    if not recent_volumes:
        return False

    avg_volume = sum(recent_volumes) / len(recent_volumes)
    return current_volume > avg_volume * multiplier