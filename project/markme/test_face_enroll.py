#!/usr/bin/env python3
"""
test_face_enroll.py — Interactive CLI to test AI face enrollment + recognition.

Usage:
  python test_face_enroll.py

Requirements:
  - Backend server must be running on http://127.0.0.1:8000
  - You need a photo file (JPG/PNG) of the person to enroll
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000/api"

def post(url, data=None, token=None, files=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if files:
        # Multipart form data
        boundary = "----FormBoundary7MA4YWxkTrZu0gW"
        body = b""
        for key, value in (data or {}).items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode()
        for key, (filename, file_bytes, content_type) in files.items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"; filename=\"{filename}\"\r\nContent-Type: {content_type}\r\n\r\n".encode()
            body += file_bytes + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    else:
        body = json.dumps(data or {}).encode()
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def get(url, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def header(title):
    print(f"\n{'━'*50}")
    print(f"  {title}")
    print(f"{'━'*50}")

def main():
    print("\n🤖 Hajri Hub — Face Enrollment & Recognition Tester")
    print("   Backend: http://127.0.0.1:8000\n")

    # ── STEP 1: Login ─────────────────────────────────
    header("STEP 1: Login as Admin")
    email = input("  Admin email [admin@hajrihub.ai]: ").strip() or "admin@hajrihub.ai"
    password = input("  Password [admin1234]: ").strip() or "admin1234"

    resp = post(f"{BASE}/auth/login/", {"email": email, "password": password})
    if "access" not in resp:
        print(f"\n❌ Login failed: {resp}")
        sys.exit(1)
    token = resp["access"]
    print("  ✅ Logged in successfully!")

    # ── STEP 2: List students ──────────────────────────
    header("STEP 2: Students in Database")
    students_resp = get(f"{BASE}/accounts/students/?page_size=100", token)
    students = students_resp.get("results", []) if isinstance(students_resp, dict) else students_resp
    
    if not students:
        print("  ⚠️  No students found. Create one via admin panel first.")
        print(f"     http://127.0.0.1:8000/admin/accounts/student/add/")
        sys.exit(1)

    for i, s in enumerate(students, 1):
        enrolled = "✅ Face enrolled" if s.get("face_registered") else "❌ No face yet"
        print(f"  {i}. {s['user']['full_name']} | {s['user']['email']} | {enrolled}")
        print(f"     ID: {s['id']}")

    # ── STEP 3: Choose student ─────────────────────────
    header("STEP 3: Select Student to Enroll")
    while True:
        try:
            choice = int(input(f"  Enter number (1-{len(students)}): ")) - 1
            if 0 <= choice < len(students):
                break
        except ValueError:
            pass
        print("  Invalid choice.")
    
    student = students[choice]
    student_id = student["id"]
    print(f"  → Selected: {student['user']['full_name']}")

    # ── STEP 4: Provide photo ──────────────────────────
    header("STEP 4: Provide Photo for Face Enrollment")
    print("  Provide a clear frontal photo (JPG/PNG) of the student.")
    print("  Tips: Good lighting, face clearly visible, no sunglasses.\n")
    
    while True:
        photo_path = input("  Path to photo file: ").strip().strip("'\"")
        if os.path.isfile(photo_path):
            break
        print(f"  ❌ File not found: {photo_path}")

    print(f"  📸 Reading {os.path.basename(photo_path)}...")
    with open(photo_path, "rb") as f:
        photo_bytes = f.read()
    
    ext = os.path.splitext(photo_path)[1].lower()
    ctype = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"

    print("  🧠 Running face detection on server (may take 2–5 seconds)...")
    result = post(
        f"{BASE}/accounts/students/{student_id}/enroll-face/",
        token=token,
        files={"photo": (os.path.basename(photo_path), photo_bytes, ctype)}
    )

    if result.get("face_registered"):
        print(f"\n  ✅ FACE ENROLLED SUCCESSFULLY!")
        print(f"     Student: {student['user']['full_name']}")
        print(f"     The AI can now recognize this person from the scanner.")
    else:
        print(f"\n  ❌ Enrollment failed: {result.get('detail', result)}")
        sys.exit(1)

    # ── STEP 5: Test recognition ───────────────────────
    header("STEP 5: Test Face Recognition (Scan)")
    print("  Now test recognition with a photo (can be the same or different one).")
    test_again = input("  Use same photo for test? [Y/n]: ").strip().lower()
    
    if test_again != 'n':
        test_path = photo_path
    else:
        while True:
            test_path = input("  Path to test photo: ").strip().strip("'\"")
            if os.path.isfile(test_path):
                break
            print(f"  ❌ File not found: {test_path}")

    with open(test_path, "rb") as f:
        test_bytes = f.read()
    ext = os.path.splitext(test_path)[1].lower()
    ctype = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"

    print("  🔍 Running AI face scan...")
    scan_result = post(
        f"{BASE}/attendance/scan/",
        token=token,
        files={"image": (os.path.basename(test_path), test_bytes, ctype)}
    )

    print()
    if scan_result.get("matched"):
        print(f"  ✅ MATCH FOUND!")
        print(f"     Student:    {scan_result.get('student_name')}")
        print(f"     Confidence: {scan_result.get('confidence', 0)*100:.1f}%")
        if scan_result.get("already_marked"):
            print(f"     ℹ️  Attendance was already marked today.")
        else:
            print(f"     📝 Attendance marked as PRESENT!")
    else:
        print(f"  ❌ No match found.")
        print(f"     Message: {scan_result.get('message')}")
        if scan_result.get("confidence"):
            print(f"     Best confidence: {scan_result.get('confidence', 0)*100:.1f}% (below threshold)")
        print(f"\n  💡 Tips:")
        print(f"     - Make sure the photo has a clear face")
        print(f"     - Try lowering tolerance: add ?tolerance=0.6 to scan URL")
        print(f"     - Re-enroll with a better quality photo")

    # ── STEP 6: Dashboard check ────────────────────────
    header("STEP 6: Dashboard Stats")
    dashboard = get(f"{BASE}/attendance/dashboard/", token)
    print(f"  📊 Today's stats:")
    print(f"     Total students:  {dashboard.get('total_students')}")
    print(f"     Present today:   {dashboard.get('present_today')}")
    print(f"     Attendance rate: {dashboard.get('attendance_rate')}%")

    print(f"\n{'━'*50}")
    print(f"  🎉 Test complete! Admin panel: http://127.0.0.1:8000/admin/")
    print(f"{'━'*50}\n")


if __name__ == "__main__":
    main()
