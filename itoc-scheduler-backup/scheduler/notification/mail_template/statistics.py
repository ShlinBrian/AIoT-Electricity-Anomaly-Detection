# Standard Library
from datetime import datetime
from typing import List

# Third Party Library
import pytz
from pytz.tzinfo import DstTzInfo

# Local Module
from scheduler.notification.mail_prod import MailReport
from scheduler.statistic_reporter.model import MeterStatistics
from scheduler.statistic_reporter.utils import build_statistics_json
from scheduler.utils.utils import convert_time_zone, func_logger, time2str


@func_logger
def generate_report(
    statistics: List[MeterStatistics],
    start_time: datetime,
    end_time: datetime,
    notify_tz: DstTzInfo,
    field: str,
) -> MailReport:
    contents = ""
    attachment_path = ""
    if statistics:
        start_time = convert_time_zone(start_time, pytz.utc, notify_tz)
        end_time = convert_time_zone(end_time, pytz.utc, notify_tz)
        contents = generate_contents(statistics, start_time, end_time, field)
        attachment_path = build_statistics_json(
            statistics, start_time, end_time
        )

    return MailReport(
        f'[{field}] Meter Statistic Report',
        'html',
        contents,
        [attachment_path],
    )


def generate_contents(
    statistics: List[MeterStatistics],
    start_time: datetime,
    end_time: datetime,
    field: str,
) -> str:

    description = f"""
    <div>The following is the statistics of {field} meter :</div>
    <br/>
    <div>Start Time: <b>{time2str(start_time)}</b></div>
    <div>End Time  :  <b>{time2str(end_time)}</b> </div>
    <div>Column Description :</div>
    <ul>
        <li>Expected: Expected Received Data Count</li>
        <li>Actual: Actual UDC Database Received Data Count</li>
        <li>After Remetering: Data Count after Remetering (<b>Smart meter</b> available  only)</li>
        <li>Collection Rate (%): (Actual/Expected) * 100%</li>
        <li>Remetering Collection Rate (%): (After Remetering/Expected) * 100%</li>
    </ul>

    <table border="1">
        <thead>
            <tr>
                <th colspan="3">Metering Data Frequency</th>
            </tr>
        </thead>
        <tbody>
        <tr>
                <th> Type</th>
                <th> Frequency</th>
                <th> count(s)/time</th>
        </tr>
        <tr>
                <td>Smart Meter</td>
                <td>1 min</td>
                <td>1 </td>
        </tr>
        <tr>
                <td>Water Meter</td>
                <td>30 mins</td>
                <td>30</td>
        </tr>
        <tr>
                <td>Gas Meter</td>
                <td>24 hours</td>
                <td>24</td>
        </tr>
        </tbody>
    </table>
    """

    stat_table = """
        <table border="1">
            <tr>
                <td>Meter ID</td>
                <td>Type</td>
                <td>Expected</td>
                <td>Actual</td>
                <td>Missing</td>
                <td>Collection<br/>Rate(%)</td>
                <td>After Remetering</td>
                <td>Collection<br/>Rate(%)<br/>(after remetering)</td>
            </tr>
    """

    for stat in statistics:
        stat_table += f"""
            <tr>
                <td>{stat.meter_id}</td>
                <td>{stat.meter_type}</td>
                <td>{str(stat.expected)}</td>
                <td>{str(stat.actual)}</td>
                <td>{str(stat.missing)}</td>
                <td>{str(stat.rate)}</td>
                <td>{str(stat.after_remetering)}</td>
                <td>{str(stat.after_rate)}</td>
            </tr>
        """

    stat_table += "</table>"
    ending = """
        <br/>
        <div>Please see the attachment for the details of meter statistics</div>
    """

    contents = f"""
        <html>
            <body>
                {description}
                {stat_table}
                {ending}
            </body>
        </html>
    """

    return contents
