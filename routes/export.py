from flask import Blueprint, Response, flash, redirect, url_for
from io import StringIO
import csv
from models import Campaign, Sponsor
from flask_security import auth_token_required, roles_accepted
from flask_login import current_user

export_bp = Blueprint('export', __name__)

@export_bp.route('/export-campaigns-csv', methods=['GET'])
@auth_token_required
@roles_accepted('sponsor')
def export_campaigns_csv():

    user = current_user
    sponsor = Sponsor.query.filter_by(user_id=user.id).first()
    
    if not sponsor:
        flash("Sponsor not found. Cannot export campaigns.", 'danger')
        return redirect(url_for('sponsor_dashboard'))

    si = StringIO()
    writer = csv.writer(si)
    
    writer.writerow(['Campaign Name', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])

    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()

    for campaign in campaigns:
        writer.writerow([
            campaign.name,
            campaign.description,
            campaign.start_date.strftime('%Y-%m-%d'),
            campaign.end_date.strftime('%Y-%m-%d'),
            campaign.budget,
            campaign.visibility,
            campaign.goals
        ])

    output = si.getvalue()
    si.close()

    response = Response(output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=campaigns_export.csv'
    
    flash("Campaign export completed successfully!", 'success')
    
    return response
