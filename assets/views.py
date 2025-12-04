from django.shortcuts import render, redirect, get_object_or_404
from .models import Asset, Reservation
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    total_assets = Asset.objects.count()
    available_assets = Asset.objects.filter(status="available").count()
    unavailable_assets = Asset.objects.exclude(status="available").count()

    recent_assets = Asset.objects.order_by('-created_at')[:5]

    return render(request, "dashboard.html", {
        "total_assets": total_assets,
        "available_assets": available_assets,
        "unavailable_assets": unavailable_assets,
        "recent_assets": recent_assets,
    })

def asset_list(request):
    assets = Asset.objects.all().order_by('name')
    return render(request, "assets/asset_list.html", {"assets": assets})

def add_asset(request):
    if request.method == "POST":
        name = request.POST.get("name")
        serial = request.POST.get("serial_number")
        category = request.POST.get("category")
        location = request.POST.get("location")
        image = request.FILES.get("image")

        # check duplicate serial
        if Asset.objects.filter(serial_number=serial).exists():
            messages.error(request, "Asset with this serial number already exists.")
            return redirect("add_asset")

        asset = Asset.objects.create(
            name=name,
            serial_number=serial,
            category=category or "",
            location=location or "",
            image=image
        )

        messages.success(request, "Asset created.")
        return redirect("asset_list")

    return render(request, "assets/add_asset.html")


def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    return render(request, "assets/asset_detail.html", {"asset": asset})

def edit_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        asset.name = request.POST.get("name") or asset.name
        asset.serial_number = request.POST.get("serial_number") or asset.serial_number
        asset.category = request.POST.get("category") or asset.category
        asset.location = request.POST.get("location") or asset.location
        asset.status = request.POST.get("status") or asset.status

        # optional: update image
        new_image = request.FILES.get("image")
        if new_image:
            asset.image = new_image

        try:
            asset.save()
            messages.success(request, "Asset updated.")
        except Exception as e:
            messages.error(request, f"Error updating asset: {e}")

        return redirect("asset_detail", pk=asset.pk)

    return render(request, "assets/edit_asset.html", {"asset": asset})


def delete_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        asset.delete()
        messages.success(request, "Asset deleted.")
        return redirect("asset_list")
    return render(request, "assets/delete_confirm.html", {"asset": asset})


# Reservations
def reservation_list(request):
    # only link to the asset; reservation stores a simple text user_name
    reservations = Reservation.objects.select_related("asset").order_by("-check_in")
    return render(request, "assets/reservation_list.html", {"reservations": reservations})


def add_reservation(request):
    assets = Asset.objects.filter(status="available").order_by('name')

    if request.method == "POST":
        asset_id = request.POST.get("asset")
        username = request.POST.get("user_name")
        checkin_str = request.POST.get("checkin_date")
        days = int(request.POST.get("days", "1"))

        asset = get_object_or_404(Asset, id=asset_id)

        # parse check-in date/time
        try:
            if 'T' in checkin_str:
                checkin = datetime.fromisoformat(checkin_str)
            else:
                checkin = datetime.fromisoformat(checkin_str + "T00:00:00")
        except Exception:
            messages.error(request, "Invalid date format.")
            return redirect("add_reservation")

        checkout = checkin + timedelta(days=days)

        # create reservation (store the plain text username)
        Reservation.objects.create(
            asset=asset,
            user_name=username,
            check_in=checkin,
            check_out=checkout,
            days=days,
            status="booked",
        )

        # update asset status
        asset.status = "unavailable"
        asset.save()

        messages.success(request, "Reservation created.")
        return redirect("reservation_list")

    return render(request, "assets/add_reservation.html", {"assets": assets})

def checkout_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    reservation.status = "checked_out"
    reservation.save()

    # update asset
    reservation.asset.status = "checked_out"
    reservation.asset.save()

    messages.success(request, "Checked out.")
    return redirect("reservation_list")
