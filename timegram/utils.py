from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Time
from django.urls import reverse

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, events):											# formats a day as a td, filter events by day
	# by leebc ----------------
		events_per_year_1 = events.filter(start_time__year__lte = self.year)
		events_per_year = events_per_year_1.filter(end_time__year__gte = self.year)

		events_per_month_1 = events_per_year.filter(start_time__month__lte = self.month)
		events_per_month = events_per_month_1.filter(end_time__month__gte = self.month)

		events_per_day_1 = events_per_month.filter(start_time__day__lte = day)
		events_per_day = events_per_day_1.filter(end_time__day__gte = day)
	# by leebc ----------------
		d = ''
		for event in events_per_day:
			d += f'<div>{event.get_html_url}</div>'								#d += f'<li> {event.get_html_url} </li>'
		if day != 0:
			url = reverse('timegram:schedule2', kwargs={'kk': day})
			return f"<td> <a class='date' href={url} kk=day>{day}</a>  {d}</td>"
		return '<td></td>'

	def formatweek(self, theweek, events):										# formats a week as a tr
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, group_id, withyear=True):								# formats a month as a table, filter events by year and month
#---leebc---
		try:
			#group_id = request.user.groups.values_list('id', flat=True).first()					#lbc inserted 'group_id'
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
		# -----------
		cal += f'</table>\n'
		cal += '<p></p>'
		#------------
		return cal

#############################################################################################################
#############################################################################################################

class Scalendar(HTMLCalendar):
	def __init__(self, year=None, month=None, day=None):
		self.year = year
		self.month = month
		self.day = day
		super(Scalendar, self).__init__()

	def formatmonth(self, group_id, day, withyear=True):
		# ---leebc---
		try:
			# group_id = request.user.groups.values_list('id', flat=True).first()					#
			event_data = Time.objects.filter(group_id=group_id)
		except:
			event_data = Time.objects.filter(group_id=1)
		# events = Time.objects.filter(start_time__year=self.year, start_time__month=self.month)		#original
		events = event_data.filter(start_time__year=self.year, start_time__month=self.month)
		# ---leebc---
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		# -----------
		cal += f'</table>\n'
		cal += '<p></p>'
		#------------
		#cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		#cal += f'{self.formatweekheader()}\n'
		#for week in self.monthdays2calendar(self.year, self.month):
		cal += f'{self.formatweek2(week, day, events)}\n'
		# -----------
		return cal

	def formatday(self, day, events):											# formats a day as a td, filter events by day
	# by leebc ----------------
		events_per_year_1 = events.filter(start_time__year__lte = self.year)
		events_per_year = events_per_year_1.filter(end_time__year__gte = self.year)

		events_per_month_1 = events_per_year.filter(start_time__month__lte = self.month)
		events_per_month = events_per_month_1.filter(end_time__month__gte = self.month)

		events_per_day_1 = events_per_month.filter(start_time__day__lte = day)
		events_per_day = events_per_day_1.filter(end_time__day__gte = day)
	# by leebc ----------------
		d = ''
		for event in events_per_day:
			d += f'<div>{event.get_html_url}</div>'								#d += f'<li> {event.get_html_url} </li>'
		if day != 0:
			url = reverse('timegram:schedule2', kwargs={'kk':day})
			return f"<td> <a class='date' href={url} kk=day>{day}</a>  {d}</td>"		#return f"<td> <span class='date'>{day}</span> <ul>{d}</ul> </td>"
		return '<td></td>'

	def formatweek(self, theweek, events):										# formats a week as a tr
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatday2(self, day, events):  # formats a day as a td, filter events by day
		# by leebc ----------------
		events_per_year_1 = events.filter(start_time__year__lte=self.year)
		events_per_year = events_per_year_1.filter(end_time__year__gte=self.year)

		events_per_month_1 = events_per_year.filter(start_time__month__lte=self.month)
		events_per_month = events_per_month_1.filter(end_time__month__gte=self.month)

		events_per_day_1 = events_per_month.filter(start_time__day__lte=day)
		events_per_day = events_per_day_1.filter(end_time__day__gte=day)
		# by leebc ----------------
		d = ''
		for event in events_per_day:
			d += f'<div><li>{event.get_html_url}</li></div>'  # d += f'<li> {event.get_html_url} </li>'
		if day != 0:
			return f"<td> <class='date'> <{self.month}월 {day}일>  {d}</td>"  # return f"<td> <span class='date'>{day}</span> <ul>{d}</ul> </td>"
		return '<td></td>'

	def formatweek2(self, theweek, day, events):  # formats a week as a tr
		week = ''
		#for d, weekday in theweek:
		week += self.formatday2(day, events)
		return f'<tr> {week} </tr>'