from flask import Blueprint, flash, redirect, session, url_for

from models import User

referral_bp = Blueprint('referral', __name__)


@referral_bp.route('/ref/<referral_code>')
def accept_referral(referral_code: str):
    code = (referral_code or '').strip()
    if not code:
        flash('Invalid referral link.', 'warning')
        return redirect(url_for('auth.register'))

    referrer = User.query.filter_by(referral_code=code).first()
    if not referrer:
        session.pop('referral_code', None)
        flash('Referral code not found.', 'warning')
        return redirect(url_for('auth.register'))

    session['referral_code'] = code
    flash('Referral code applied. Complete signup to claim your bonus.', 'success')
    return redirect(url_for('auth.register', ref=code))
