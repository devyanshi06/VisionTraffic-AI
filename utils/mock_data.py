import random

def get_dashboard_data():

    return {
        "vehicle_count": random.randint(120, 220),

        "traffic_status": random.choice([
            "Low",
            "Moderate",
            "High"
        ]),

        "average_speed": random.randint(30, 70),

        "alerts": random.randint(0, 5)
    }