# Third Party Library
# Standard Library
import os
from datetime import datetime

from loguru import logger

# Local Module
from scheduler.notification.mail_prod import MailReport


def generate_report(anomalies) -> MailReport:
    contents = ""
    title = "[UDC Server] DR Result"
    logger.info('[SETTLEMENT CALCULATION] Generate report')
    if len(anomalies) > 0:
        contents = generate_contents(anomalies)

    return MailReport(
        subject=title,
        subtype='html',
        content=contents,
    )


def generate_contents(anomalies) -> str:

    content = "<html><body>"
    for anomaly in anomalies:
        content += f"""
            <div>
                <ol>
                    <li>Checking Time: {datetime.now().strftime("%b %d %Y %H:%M:%S")}</li>
                    <li>Anomalous Meters: {anomaly['meter']}</li>
                    <li>Probable Cause: {anomaly['type']} kW</li>
                    <li>Recommended Solution: {anomaly['solution']} kW</li>
                    <li><img src="{os.environ.get('NGROK')}"></li>
                </ol>
            </div>
        """
    content += "</html></body>"

    # content = f"""
    # <html>
    #     <body>
    #         <div>
    #             <ol>
    #                 <li>Checking Time: {datetime.now().strftime("%b %d %Y %H:%M:%S")}</li>
    #                 <li>Anomalous Meters: {anomalies[0]['meter']}</li>
    #                 <li>Probable Cause: {anomalies[0]['type']} kW</li>
    #                 <li>Recommended Solution: {anomalies[0]['solution']} kW</li>
    #             </ol>
    #         </div>
    #     </body>
    # </html>
    # """

    return content
