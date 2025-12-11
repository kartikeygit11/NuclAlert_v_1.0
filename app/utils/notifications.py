"""Desktop notification utilities."""

from plyer import notification
from app.config import NOTIFICATION_TIMEOUTS


def send_notification(level, plants):
    """
    Send desktop notification based on radiation level.
    
    Args:
        level: Notification level ('dangerous', 'moderate', 'safe')
        plants: List of plant names triggering the notification
    """
    if not plants:
        return
    
    timeouts = NOTIFICATION_TIMEOUTS
    
    if level == 'dangerous':
        notification.notify(
            title="🚨 HIGH RADIATION ALERT!",
            message=f"Critical danger! You're within 50km of {len(plants)} dangerous plants: {', '.join(plants)}",
            timeout=timeouts["dangerous"],
            app_icon=None
        )
    elif level == 'moderate':
        notification.notify(
            title="⚠️ Moderate Radiation Warning",
            message=f"Caution! You're within 75km of {len(plants)} aging plants: {', '.join(plants)}",
            timeout=timeouts["moderate"]
        )
    elif level == 'safe':
        notification.notify(
            title="ℹ️ Radiation Monitoring",
            message=f"You're near {len(plants)} newer plants: {', '.join(plants)}",
            timeout=timeouts["safe"]
        )

