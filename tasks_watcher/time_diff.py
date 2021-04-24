from datetime import datetime, timedelta


def time_diff_to_str(diff: timedelta) -> str:
    if diff < timedelta(minutes=1):
        return "a moment"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f"{minutes}min"
    elif diff < timedelta(days=1):
        seconds = diff.seconds
        hours = seconds // (60 * 60)
        remaining_seconds = seconds - hours * 60 * 60
        minutes = remaining_seconds // 60
        return f"{hours}h {minutes}min"
    elif diff < timedelta(days=1):
        seconds = diff.seconds
        days = seconds // (60 * 60 * 24)
        remaining_seconds = seconds - days * 60 * 60 * 24
        hours = remaining_seconds // (60 * 60)
        remaining_seconds = seconds - hours * 60 * 60
        minutes = remaining_seconds // 60
        return f"{days}d {hours}h {minutes}min"

    raise Exception("too big diff wtf bro")


def time_diff(started_at: datetime, stopped_at: datetime) -> str:
    if started_at > stopped_at:
        raise Exception("the started_at is newer then stopped_at")

    diff = stopped_at - started_at
    return time_diff_to_str(diff)
