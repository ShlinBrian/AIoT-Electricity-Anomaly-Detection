# Third Party Library
# Standard Library
from datetime import timedelta
from typing import List

from loguru import logger
from sqlalchemy.orm import Session

# Local Module
from scheduler.dr.utils import timezone
from scheduler.notification.mail_prod import MailReport
from tables.coupon.coupon_model import AcceptanceHistory, DrCouponEvent
from tables.system.system_model import LineUserLocation


def generate_report(
    session: Session,
    dr_coupon_event: DrCouponEvent,
    acceptance_histories: List[AcceptanceHistory],
) -> MailReport:
    contents = ""
    title = "[UDC Server] Coupon-based DR Result"
    logger.info('[EXECUTION RESULT ANNOUNCEMENT] Generate report')
    if dr_coupon_event:
        location_tz = timezone(session, dr_coupon_event.location)
        date = (dr_coupon_event.start_time + location_tz).strftime("%Y-%m-%d")
        contents = generate_contents(
            session, dr_coupon_event, acceptance_histories, location_tz
        )
        title = f'[{dr_coupon_event.location}] {date} Coupon-based DR Result'
    return MailReport(subject=title, subtype='html', content=contents)


def generate_contents(
    session: Session,
    dr_coupon_event: DrCouponEvent,
    acceptance_histories: List[AcceptanceHistory],
    location_tz: timedelta,
) -> str:
    users = (
        session.query(LineUserLocation)
        .filter(
            LineUserLocation.location == dr_coupon_event.location,
            LineUserLocation.in_use.is_(True),
        )
        .all()
    )
    family_count = len(users)
    participant_count = sum(
        [
            1
            for acceptance_history in acceptance_histories
            if acceptance_history.accept
        ]
    )
    start = (dr_coupon_event.start_time + location_tz).strftime(
        "%Y-%m-%d %H:%M"
    )
    end = (dr_coupon_event.end_time + location_tz).strftime("%Y-%m-%d %H:%M")
    savings = dr_coupon_event.execution_reduct_demand
    content = f"""
    <html>
        <body>
            <div>
                <ol>
                    <li>House: {dr_coupon_event.location}</li>
                    <li>Family size: {family_count}</li>
                    <li>The numbers of participants: {participant_count}</li>
                    <li>Savings Demand (kW): {savings}</li>
                    <li>Execution Start Time: {start}</li>
                    <li>Execution End Time: {end}</li>
    """
    if acceptance_histories:
        content += """
        <br><li>User Info:</li>
        """
        for acceptance_history in acceptance_histories:
            content += f"""
                UserID: {acceptance_history.line_id}<br>
                Type: {acceptance_history.type}<br>
                Coupon Value: {acceptance_history.coupon_value}<br>
                Allowance: {acceptance_history.allowance}<br>
                Accept: {acceptance_history.accept}<br>
                <br>
        """
    content += """
                </ol>
            </div>
        </body>
    </html>
    """
    return content
