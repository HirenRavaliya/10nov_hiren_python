# Q21 — Payment Integration (Stripe): Doctor Appointment Booking

## What It Does
Allows users to book and pay for doctor appointments via **Stripe Checkout**. Supports INR payments with dynamic consultation fees per doctor.

## Endpoints
| URL | Description |
|-----|-------------|
| `/q21/` | Booking home — doctor list + appointment history |
| `/q21/book/` | POST to create appointment + redirect to Stripe |
| `/q21/success/<id>/` | Payment success page |
| `/q21/cancel/` | Payment cancelled page |

## Setup
1. Register at https://stripe.com
2. Get **Test** API keys from Dashboard → Developers → API keys
3. Add to `.env`:
```
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
```

## Without Stripe Config
Runs in **demo mode** — bookings are saved as "paid" without actual payment.

## Test Cards (Stripe test mode)
| Card | Result |
|------|--------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 0002 | Declined |

## Files
| File | Purpose |
|------|---------|
| `models.py` | Appointment model with `status` + `stripe_session_id` |
| `views.py` | Booking + Stripe Checkout session creation |
| `templates/q21/booking.html` | Doctor selection + booking form |
| `templates/q21/success.html` | Payment success confirmation |
