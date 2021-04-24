from datetime import datetime, timedelta


def _calculate(diff: timedelta):
    seconds = diff.seconds
    days = seconds // (60 * 60 * 24)
    remaining_seconds = seconds - days * 60 * 60 * 24
    hours = remaining_seconds // (60 * 60)
    remaining_seconds = seconds - hours * 60 * 60
    minutes = remaining_seconds // 60
    return [days, hours, minutes]


def time_diff_to_str(diff: timedelta) -> str:
    units = ["d", "h", "min"]
    values = _calculate(diff)
    return " ".join([f"{v}{u}" for v, u in zip(values, units) if v != 0])


def time_diff(started_at: datetime, stopped_at: datetime) -> str:
    if started_at > stopped_at:
        raise Exception("the started_at is newer then stopped_at")

    diff = stopped_at - started_at
    return time_diff_to_str(diff)
