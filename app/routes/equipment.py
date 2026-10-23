
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import Equipment
from app.permissions import role_required

staff_equipment = Blueprint("staff_equipment", __name__)


# Displays the equipment management page and handles adding equipment.
@staff_equipment.route("/staff/equipment", methods=["GET", "POST"])
@role_required("Staff")
def manage_equipment():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Available").strip()

        if not name or not category:
            flash("Equipment name and category are required.", "danger")
        elif len(name) > 120 or len(category) > 80:
            flash("Equipment name or category is too long.", "danger")
        elif status not in {"Available", "Unavailable"}:
            flash("Please select a valid equipment status.", "danger")
        else:
            equipment = Equipment(
                name=name,
                category=category,
                description=description or None,
                status=status,
            )

            db.session.add(equipment)
            db.session.commit()

            flash("Equipment added successfully.", "success")
            return redirect(url_for("staff_equipment.manage_equipment"))

    equipment_items = Equipment.query.order_by(Equipment.name).all()

    return render_template(
        "staff/equipment.html",
        equipment_items=equipment_items,
    )


# Deletes equipment only when it has no booking history.
@staff_equipment.route(
    "/staff/equipment/<int:equipment_id>/delete",
    methods=["POST"],
)
@role_required("Staff")
def delete_equipment(equipment_id):
    equipment = db.session.get(Equipment, equipment_id)

    if equipment is None:
        flash("Equipment not found.", "danger")
    elif equipment.bookings:
        flash(
            "Equipment with booking history cannot be deleted.",
            "warning",
        )
    else:
        db.session.delete(equipment)
        db.session.commit()
        flash("Equipment deleted successfully.", "success")

    return redirect(url_for("staff_equipment.manage_equipment"))
