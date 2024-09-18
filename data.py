from datetime import datetime, timedelta

# Function to generate time slots
def generate_slots(start_time, end_time, interval_minutes=30):
    slots = []
    current_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    
    while current_time <= end_time:
        slots.append(current_time.strftime("%Y-%m-%d %H:%M"))
        current_time += timedelta(minutes=interval_minutes)
    
    return slots

def generate_half_day_slots(start_time, end_time, interval_minutes=30):
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    half_day_end_time = start_time.replace(hour=12, minute=0)
    return generate_slots(start_time.strftime("%Y-%m-%d %H:%M"), half_day_end_time.strftime("%Y-%m-%d %H:%M"), interval_minutes)

hospitals = [
    {"id": 1, "name": "Hospital A", "lat": 28.5355, "lon": 77.3910},
    {"id": 2, "name": "Hospital B", "lat": 28.7041, "lon": 77.1025},
    {"id": 3, "name": "Hospital B", "lat": 28.9213, "lon": 78.1025},
]

doctors = {
    1: [
        {"id": 1, "name": "Dr. Aarav Patel", "specialty": "Cardiology"},
        {"id": 2, "name": "Dr. Priya Sharma", "specialty": "Neurology"},
        {"id": 3, "name": "Dr. Kabir Gupta", "specialty": "Orthopedics"},
        {"id": 4, "name": "Dr. Neha Singh", "specialty": "Pediatrics"},
        {"id": 5, "name": "Dr. Rajesh Reddy", "specialty": "Dermatology"},
        {"id": 6, "name": "Dr. Aisha Khan", "specialty": "General Medicine"},
        {"id": 7, "name": "Dr. Siddharth Nair", "specialty": "Internal Medicine"},
        {"id": 8, "name": "Dr. Meera Joshi", "specialty": "Gastroenterology"},
        {"id": 9, "name": "Dr. Arjun Verma", "specialty": "Pulmonology"},
        {"id": 10, "name": "Dr. Isha Desai", "specialty": "Endocrinology"}
    ],
    2: [
        {"id": 11, "name": "Dr. Ankit Kumar", "specialty": "Rheumatology"},
        {"id": 12, "name": "Dr. Aarti Mehta", "specialty": "Hematology"},
        {"id": 13, "name": "Dr. Rohan Patel", "specialty": "Nephrology"},
        {"id": 14, "name": "Dr. Simran Chawla", "specialty": "Allergy & Immunology"},
        {"id": 15, "name": "Dr. Vikram Rathi", "specialty": "Urology"},
        {"id": 16, "name": "Dr. Sanya Gupta", "specialty": "Surgery"},
        {"id": 17, "name": "Dr. Ravi Bhat", "specialty": "Ophthalmology"},
        {"id": 18, "name": "Dr. Pooja Bhardwaj", "specialty": "Ear, Nose & Throat"},
        {"id": 19, "name": "Dr. Karan Joshi", "specialty": "Pain Management"},
        {"id": 20, "name": "Dr. Tanya Kapoor", "specialty": "Physical Medicine & Rehabilitation"}
    ],
    3: [
        {"id": 21, "name": "Dr. Aarav Singh", "specialty": "Oncology"},
        {"id": 22, "name": "Dr. Riya Nair", "specialty": "Palliative Care"},
        {"id": 23, "name": "Dr. Aman Yadav", "specialty": "Neurosurgery"},
        {"id": 24, "name": "Dr. Meenal Agarwal", "specialty": "Vascular Surgery"},
        {"id": 25, "name": "Dr. Kunal Sharma", "specialty": "Rehabilitation"},
        {"id": 26, "name": "Dr. Sneha Deshmukh", "specialty": "Obstetrics & Gynecology"},
        {"id": 27, "name": "Dr. Anil Patel", "specialty": "Plastic Surgery"},
        {"id": 28, "name": "Dr. Kavita Jain", "specialty": "Thoracic Surgery"},
        {"id": 29, "name": "Dr. Rajiv Mehta", "specialty": "Geriatrics"},
        {"id": 30, "name": "Dr. Nidhi Kapoor", "specialty": "Emergency Medicine"}
    ]
}

# Generate slots for doctors dynamically
def generate_all_slots():
    all_slots = {}
    
    for hospital_id in doctors.keys():
        for doctor in doctors[hospital_id]:
            doctor_id = doctor["id"]
            # Set start and end time for appointments
            start_date = datetime(2024, 9, 18)
            end_date = datetime(2024, 9, 30)
            
            # Generate slots for each day
            doctor_slots = {}
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                if current_date.weekday() == 6:  # Sunday
                    slots_for_date = generate_half_day_slots(
                        f"{date_str} 09:00",
                        f"{date_str} 12:00"
                    )
                else:
                    slots_for_date = generate_slots(
                        f"{date_str} 09:00",
                        f"{date_str} 17:00"
                    )
                
                # Store slots by date
                doctor_slots[date_str] = slots_for_date
                current_date += timedelta(days=1)
            
            all_slots[doctor_id] = doctor_slots
    
    return all_slots
