"""
SEHAYAK (सहायक) - Authentication and Role Management Module
Protects student privacy, supports 4 distinct roles:
 - Principal (School leadership)
 - Teacher (Assigned 100 students)
 - Student (Assessment & practice)
 - Parent (Child progress & teacher chat)
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from utils.db import get_user_by_username

def authenticate_user(username, password):
    """Verify credentials and return user dict if valid."""
    user = get_user_by_username(username.strip().lower())
    if not user:
        return None
    if check_password_hash(user["password_hash"], password.strip()):
        return user
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in as an educator.", "warning")
            return redirect(url_for("login"))
        role = session.get("user", {}).get("role")
        if role not in ["teacher", "principal"]:
            flash("Educator credentials are required to view student assessment analytics.", "danger")
            return redirect(url_for("student_portal"))
        return f(*args, **kwargs)
    return decorated_function

def principal_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in as Principal.", "warning")
            return redirect(url_for("login"))
        if session.get("user", {}).get("role") != "principal":
            flash("Institutional leadership credentials required.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def counselor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in as School Counselor.", "warning")
            return redirect(url_for("login", role="counselor"))
        role = session.get("user", {}).get("role")
        if role != "counselor":
            flash("School Counselor credentials are required for this workspace.", "danger")
            if role == "parent":
                return redirect(url_for("parent_view"))
            elif role in ["teacher", "principal"]:
                return redirect(url_for("dashboard"))
            return redirect(url_for("student_portal"))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Allow Teachers, Principal, or School Counselor to inspect student diagnostics."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in as staff or counselor.", "warning")
            return redirect(url_for("login"))
        role = session.get("user", {}).get("role")
        if role not in ["teacher", "principal", "counselor"]:
            flash("Educator or Counselor credentials are required to view student diagnostics.", "danger")
            return redirect(url_for("student_portal"))
        return f(*args, **kwargs)
    return decorated_function
