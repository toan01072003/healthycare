# chatbot/views.py
from django.shortcuts import render, redirect
from .forms import ChatForm
from .logic.predictor import predict_disease
from django.http import JsonResponse
import joblib

symptom_encoder = joblib.load("chatbot/logic/symptom_encoder.pkl")
all_symptoms = symptom_encoder.classes_

def suggest_symptoms(request):
    query = request.GET.get("q", "").lower()
    matches = [s for s in all_symptoms if query in s.lower()]
    return JsonResponse({"suggestions": matches[:10]})  # Giới hạn 10 gợi ý


# Lưu hội thoại trong session (tạm thời, đơn giản)
def chatbot_view(request):
    chat_history = request.session.get("chat_history", [])

    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            predictions = predict_disease(message.split(","))  # xử lý triệu chứng dạng list

            # tạo phản hồi
            reply = "Tôi dự đoán bạn có thể mắc:\n" + "\n".join(
                [f"{i+1}. {p['disease']} ({p['confidence']}%)" for i, p in enumerate(predictions)]
            )

            chat_history.append(("Bạn", message))
            chat_history.append(("AI", reply))
            request.session["chat_history"] = chat_history
            return redirect("chatbot-text")
    else:
        form = ChatForm()

    return render(request, "chatbot/chat_text.html", {
        "form": form,
        "chat_history": chat_history
    })



from django.shortcuts import render, redirect
from .forms import ChatForm
from appointment.models import Appointment
from user_profile.models import UserProfile
from django.utils import timezone
import dateparser

def appointment_chatbot_view(request):
    state = request.session.get("appointment_state", {"step": 0})
    message = None
    response = ""

    if request.method == "POST":
        form = ChatForm(request.POST)
        message = form.data.get("message", "").strip()
        date_input = request.POST.get("date_input")
        doctor_input = request.POST.get("doctor_input")

        # Xử lý xác nhận
        if state.get("step") == "confirm":
            if message.lower() in ["yes", "y"]:
                doctor = UserProfile.objects.get(user_id=state["doctor_id"])
                dt = dateparser.parse(state["date_time"])
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())

                Appointment.objects.create(
                    patient=request.user,
                    doctor=doctor.user,
                    date_time=dt,
                    reason="Confirmed via chatbot",
                    status="pending"
                )
                response = f"✅ Your appointment with Dr. {doctor.full_name} at {dt.strftime('%H:%M on %d/%m/%Y')} has been confirmed."
                state = {"step": 0}
            else:
                response = "❌ Appointment canceled. Please enter a new request or select again."
                state = {"step": 0}

        elif message:
            dt = dateparser.parse(message, settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': timezone.now()})
            matched_doctor = None

            for doc in UserProfile.objects.filter(user__role="doctor"):
                if doc.full_name.lower() in message.lower():
                    matched_doctor = doc
                    break

            if dt and matched_doctor:
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())

                if dt < timezone.now():
                    response = "⚠️ The selected time is in the past. Please choose a future time."
                elif dt.hour < 8 or dt.hour > 17:
                    response = "🕗 Appointments are allowed from 08:00 to 17:00 only."
                elif Appointment.objects.filter(doctor=matched_doctor.user, date_time=dt).exists():
                    # show available slots
                    selected_date = dt.date()
                    available_slots = []
                    for hour in range(8, 18):
                        slot_time = timezone.make_aware(
                            timezone.datetime.combine(selected_date, timezone.datetime.min.time()).replace(hour=hour)
                        )
                        if not Appointment.objects.filter(doctor=matched_doctor.user, date_time=slot_time).exists():
                            available_slots.append(slot_time.strftime("%H:%M"))

                    response = (
                        f"❌ Dr. {matched_doctor.full_name} is not available at {dt.strftime('%H:%M %d/%m/%Y')}.\n"
                        f"🕒 Available time slots on {selected_date.strftime('%d/%m/%Y')}: "
                        + ", ".join(available_slots) +
                        "\n👉 Please type a new time from the available slots."
                    )
                    state["step"] = 0
                else:
                    state = {
                        "step": "confirm",
                        "doctor_id": matched_doctor.user.id,
                        "doctor_name": matched_doctor.full_name,
                        "date_time": dt.isoformat()
                    }
                    response = f"🔔 Do you confirm booking with Dr. {matched_doctor.full_name} at {dt.strftime('%H:%M on %d/%m/%Y')}? (yes/no)"
            else:
                state["step"] = 1
                response = "📅 Please enter the date and doctor for your appointment."

        else:
            response = "❓ Please type your request or use the selection options."

        # Gửi kết quả ra giao diện
        doctors = UserProfile.objects.filter(user__role="doctor")
        request.session["appointment_state"] = state
        return render(request, "appointment/chat_appointment.html", {
            "form": ChatForm(initial={"message": ""}),
            "bot_message": response,
            "step": state["step"],
            "doctors": doctors
        })

    # GET request
    doctors = UserProfile.objects.filter(user__role="doctor")
    request.session["appointment_state"] = {"step": 0}
    return render(request, "appointment/chat_appointment.html", {
        "form": ChatForm(),
        "bot_message": "Hi! You can type something like 'Book with Dr. Minh at 10 AM tomorrow' or use the selectors below.",
        "step": 0,
        "doctors": doctors
    })


# chatbot/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(["GET"])
def doctor_list_view(request):
    doctors = User.objects.filter(role="doctor", status="approved")
    return Response([
        {"id": doctor.id, "name": doctor.email} for doctor in doctors
    ])







