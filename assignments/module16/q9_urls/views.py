from django.shortcuts import render


DOCTORS = [
    {
        "id": 1,
        "name": "Dr. Priya Sharma",
        "specialty": "Cardiologist",
        "experience": "12 Years",
        "rating": 4.9,
        "location": "Ahmedabad, Gujarat",
        "image_placeholder": "PS",
        "color": "#4285F4",
        "available": True,
        "bio": "Dr. Priya Sharma is a board-certified cardiologist with over 12 years of experience "
               "in interventional cardiology. She specializes in complex coronary interventions, "
               "heart failure management, and preventive cardiology.",
        "education": [
            "MBBS – B.J. Medical College, Ahmedabad",
            "MD (Medicine) – AIIMS, New Delhi",
            "DM (Cardiology) – PGIMER, Chandigarh",
        ],
        "consultations": 3200,
        "languages": ["English", "Hindi", "Gujarati"],
    },
    {
        "id": 2,
        "name": "Dr. Arjun Mehta",
        "specialty": "Neurologist",
        "experience": "9 Years",
        "rating": 4.7,
        "location": "Surat, Gujarat",
        "image_placeholder": "AM",
        "color": "#1877F2",
        "available": True,
        "bio": "Dr. Arjun Mehta is a renowned neurologist focusing on stroke management, epilepsy, "
               "and movement disorders. He has published over 20 research papers in international journals.",
        "education": [
            "MBBS – Government Medical College, Surat",
            "MD (Medicine) – KEM Hospital, Mumbai",
            "DM (Neurology) – NIMHANS, Bangalore",
        ],
        "consultations": 2100,
        "languages": ["English", "Hindi", "Gujarati"],
    },
    {
        "id": 3,
        "name": "Dr. Sneha Patel",
        "specialty": "Dermatologist",
        "experience": "7 Years",
        "rating": 4.8,
        "location": "Vadodara, Gujarat",
        "image_placeholder": "SP",
        "color": "#FBBC05",
        "available": False,
        "bio": "Dr. Sneha Patel specialises in cosmetic and clinical dermatology, with expertise in "
               "acne management, hair loss treatment, and laser-based skin therapies.",
        "education": [
            "MBBS – M.S. University, Baroda",
            "MD (Dermatology) – Lokmanya Tilak Municipal Medical College, Mumbai",
        ],
        "consultations": 1800,
        "languages": ["English", "Hindi", "Gujarati"],
    },
]


def home(request):

    query = request.GET.get("q", "").strip()
    specialty_filter = request.GET.get("specialty", "").strip()

    doctors = DOCTORS

    if query:
        doctors = [
            d for d in doctors
            if query.lower() in d["name"].lower()
            or query.lower() in d["specialty"].lower()
            or query.lower() in d["location"].lower()
        ]

    if specialty_filter:
        doctors = [d for d in doctors if d["specialty"] == specialty_filter]

    specialties = sorted({d["specialty"] for d in DOCTORS})

    context = {
        "doctors": doctors,
        "query": query,
        "specialties": specialties,
        "selected_specialty": specialty_filter,
        "total_doctors": len(DOCTORS),
    }
    return render(request, "doctor_finder/home.html", context)


def profile(request, doctor_id):

    doctor = next((d for d in DOCTORS if d["id"] == doctor_id), None)
    if doctor is None:
        from django.http import Http404
        raise Http404("Doctor not found")


    similar = [d for d in DOCTORS if d["id"] != doctor_id]

    context = {
        "doctor": doctor,
        "similar": similar,
    }
    return render(request, "doctor_finder/profile.html", context)


def contact(request):

    submitted = False
    doctors_list = [(d["id"], d["name"]) for d in DOCTORS]

    if request.method == "POST":
        submitted = True

    context = {
        "submitted": submitted,
        "doctors_list": doctors_list,
    }
    return render(request, "doctor_finder/contact.html", context)