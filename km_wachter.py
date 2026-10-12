# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernised 2025.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how far through the service interval the car is, as a percentage (0–100+)."""
    return km_since_service / interval * 100     a car with no last-service reading is handled
    PASS   The 15000 km / 80% rules are untouched
            interval=15000, threshold=80 (both must be untouched)
    PASS   The settings.cfg rules are untouched
            settings.cfg says interval=15000, threshold=80 (both must be untouched)
    PASS   The nightly repo


def needs_service(car: dict) -> bool:
    """Return True if this car is at or past the 80 % wear threshold."""
    # If there is no last-service reading, assume the car was just serviced
    # (km since service = 0), so it is never falsely flagged as overdue.
    last = car.get("last_service_km", car["odometer"])
    km_since = car["odometer"] - last
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Flag every car that needs a service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
