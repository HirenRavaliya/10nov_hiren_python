from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import Http404

# ── Doctor data with real Gujarat coordinates ─────────────────────────────────
# This app is self-contained — it carries its own data, independent of any
# other app in the project.
DOCTORS = [
    {
        "id": 1,
        "name": "Dr. Priya Sharma",
        "specialty": "Cardiologist",
        "experience": "12 Years",
        "rating": 4.9,
        "city": "Ahmedabad",
        "address": "Sterling Hospital, Gurukul Rd, Memnagar, Ahmedabad – 380052",
        "lat": 23.0480,
        "lng": 72.5300,
        "initials": "PS",
        "available": True,
        "timings": "Mon–Sat, 10 AM – 5 PM",
        "phone": "+91 79 2630 1234",
        "bio": (
            "Dr. Priya Sharma is a board-certified cardiologist with over 12 years of experience "
            "in interventional cardiology, heart failure management, and preventive care."
        ),
        "consultations": 3200,
    },
    {
        "id": 2,
        "name": "Dr. Arjun Mehta",
        "specialty": "Neurologist",
        "experience": "9 Years",
        "rating": 4.7,
        "city": "Surat",
        "address": "Kiran Hospital, Majura Gate, Surat – 395001",
        "lat": 21.2012,
        "lng": 72.8343,
        "initials": "AM",
        "available": True,
        "timings": "Mon–Fri, 9 AM – 4 PM",
        "phone": "+91 261 246 5678",
        "bio": (
            "Dr. Arjun Mehta is a renowned neurologist focusing on stroke management, epilepsy, "
            "and movement disorders with 20+ published research papers."
        ),
        "consultations": 2100,
    },
    {
        "id": 3,
        "name": "Dr. Sneha Patel",
        "specialty": "Dermatologist",
        "experience": "7 Years",
        "rating": 4.8,
        "city": "Vadodara",
        "address": "Bhailal Amin General Hospital, Jetalpur Rd, Vadodara – 390007",
        "lat": 22.2850,
        "lng": 73.1987,
        "initials": "SP",
        "available": False,
        "timings": "Tue–Sun, 11 AM – 6 PM",
        "phone": "+91 265 243 9012",
        "bio": (
            "Dr. Sneha Patel specialises in cosmetic and clinical dermatology, with expertise in "
            "acne management, hair loss treatment, and laser-based skin therapies."
        ),
        "consultations": 1800,
    },
    {
        "id": 4,
        "name": "Dr. Rahul Joshi",
        "specialty": "Orthopaedist",
        "experience": "14 Years",
        "rating": 4.6,
        "city": "Rajkot",
        "address": "Pedak Road Hospital, Pedak Rd, Rajkot – 360002",
        "lat": 22.2980,
        "lng": 70.7984,
        "initials": "RJ",
        "available": True,
        "timings": "Mon–Sat, 9 AM – 3 PM",
        "phone": "+91 281 222 3456",
        "bio": (
            "Dr. Rahul Joshi is a senior orthopaedic surgeon specialising in joint replacements, "
            "sports injuries, and spinal disorders with 2,000+ successful surgeries."
        ),
        "consultations": 4100,
    },
    {
        "id": 5,
        "name": "Dr. Kavita Shah",
        "specialty": "Paediatrician",
        "experience": "11 Years",
        "rating": 4.9,
        "city": "Gandhinagar",
        "address": "Civil Hospital, Sector 12, Gandhinagar – 382016",
        "lat": 23.2195,
        "lng": 72.6473,
        "initials": "KS",
        "available": True,
        "timings": "Mon–Sat, 10 AM – 6 PM",
        "phone": "+91 79 2324 7890",
        "bio": (
            "Dr. Kavita Shah is a compassionate paediatrician with 11 years of experience in "
            "neonatal care, childhood vaccinations, and developmental paediatrics."
        ),
        "consultations": 5200,
    },
    {
        "id": 6,
        "name": "Dr. Vikram Desai",
        "specialty": "Ophthalmologist",
        "experience": "16 Years",
        "rating": 4.8,
        "city": "Bhavnagar",
        "address": "Sir T. Hospital, Jail Rd, Bhavnagar – 364001",
        "lat": 21.7583,
        "lng": 72.1461,
        "initials": "VD",
        "available": False,
        "timings": "Mon–Fri, 8 AM – 2 PM",
        "phone": "+91 278 242 0001",
        "bio": (
            "Dr. Vikram Desai is a leading ophthalmologist specialising in cataract surgeries, "
            "retinal disorders, and LASIK procedures across South Gujarat."
        ),
        "consultations": 6100,
    },
]


def _get_api_key():
    return getattr(settings, "GOOGLE_MAPS_API_KEY", "")


def map_home(request):
    """
    Main page — full-screen interactive Google Map with all doctor markers,
    a filterable sidebar, and info windows.
    URL: /map/
    """
    specialties = sorted({d["specialty"] for d in DOCTORS})
    context = {
        "doctors": DOCTORS,
        "specialties": specialties,
        "maps_api_key": _get_api_key(),
        "total": len(DOCTORS),
    }
    return render(request, "doctor_map/map_home.html", context)


def doctor_detail(request, doctor_id):
    """
    Detail page for a single doctor — shows profile info plus a
    focused mini-map centred on their clinic location.
    URL: /map/doctor/<int:doctor_id>/
    """
    doctor = next((d for d in DOCTORS if d["id"] == doctor_id), None)
    if doctor is None:
        raise Http404("Doctor not found")

    others = [d for d in DOCTORS if d["id"] != doctor_id]
    context = {
        "doctor": doctor,
        "others": others,
        "maps_api_key": _get_api_key(),
    }
    return render(request, "doctor_map/doctor_detail.html", context)


def about(request):
    """
    About page — explains what this app does and how the
    Google Maps API is used. Demonstrates a third URL route.
    URL: /map/about/
    """
    context = {
        "total_doctors": len(DOCTORS),
        "cities": sorted({d["city"] for d in DOCTORS}),
        "specialties": sorted({d["specialty"] for d in DOCTORS}),
    }
    return render(request, "doctor_map/about.html", context)
