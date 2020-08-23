from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Time

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, group_id, withyear=True):													#lbc inserted 'group_id'
#---leebc---
		try:
			#group_id = request.user.groups.values_list('id', flat=True).first()					#lbc
			event_data = Time.objects.filter(group_id=group_id)
		except:
			event_data = Time.objects.filter(group_id=1)
		#events = Time.objects.filter(start_time__year=self.year, start_time__month=self.month)		#original
		events = event_data.filter(start_time__year=self.year, start_time__month=self.month)
#---leebc---
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal