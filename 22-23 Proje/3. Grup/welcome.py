from time_details import get_hours, get_date
from output_module import output
from database import update_last_seen, get_last_seen
import assistant_details as ad
from help_task import help_greet
from datetime import date

def greet(status):
    previous_date = get_last_seen()
    today_date = get_date()
    update_last_seen(today_date)
    bot = ad.name
    m = "Sorabileceğin birkaç şey.."
    msg = ". Your " + bot + " Assistant burada. Sana birçok konuda yardım edebilirim. " + m

    if previous_date == today_date:
        output("Tekrar hoş geldin.. " + status + msg)
    else:
        hour = int(get_hours())
        if 4 <= hour < 12:
            output("Günaydın, " + status + msg)
        elif 12 <= hour < 16:
            output("İyi günler, " + status + msg)
        else:
            output("İyi geceler, " + status + msg)

    help_greet()




	

