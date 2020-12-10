from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from .models import Time
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, events, color):											# formats a day as a td, filter events by day
	# by leebc ----------------
		events_per_year_1 = events.filter(start_time__year__lte = self.year)
		events_per_year = events_per_year_1.filter(end_time__year__gte = self.year)

		events_per_month_1 = events_per_year.filter(start_time__month__lte = self.month)
		events_per_month = events_per_month_1.filter(end_time__month__gte = self.month)

		events_per_day_1 = events_per_month.filter(start_time__day__lte = day)
		events_per_day = events_per_day_1.filter(end_time__day__gte = day)
	# by leebc ----------------
		d = ''
		count = 0
		for event in events_per_day:
			count += 1
			if count > 3:
				dx = ""
			else:
				dx = event.get_html_url2
			d += f'<div>{dx}</div>'
			#d += f'<div>{event.get_html_url}</div>'								#d += '<div>\u2007\u2007<\u2022\u2022\u2022></div>'
		if day != 0:
			yearmonthday = (self.year - 2000) * 10000 + self.month * 100 + day
			url = reverse('timegram:schedule2', kwargs={'kk': yearmonthday})
			#url = reverse('timegram:schedule2', kwargs={'kk': day})

			day_display = day
			if day==date.today().day:
				if color=='red':
					return f"<td> <a class='red_xdate' href={url} kk=day>{day_display}</a>  {d}</td>"
				else:
					return f"<td> <a class='xdate' href={url} kk=day>{day_display}</a>  {d}</td>"
			else:
				if color=='red':
					return f"<td> <a class='red_date' href={url} kk=day>{day_display}</a>  {d}</td>"
				else:
					return f"<td> <a class='date' href={url} kk=day>{day_display}</a>  {d}</td>"
		return '<td></td>'

	def formatweek(self, theweek, events):										# formats a week as a tr
		week = ''
		count = 0
		for d, weekday in theweek:
			count += 1
			if count==6 or count==7:
				color = 'red'
			else:
				color = 'blue'
			week += self.formatday(d, events, color)
		return f'<tr> {week}</tr>'

	def formatmonth(self, group_id, author_id, withyear=True):								# formats a month as a table, filter events by year and month
#---leebc---

#group_id = request.user.groups.values_list('id', flat=True).first()  # for group_name, replace 'id' with 'name'
#pagefiles = Task.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))


		event_data = Time.objects.filter(Q(group_id=group_id) & Q(author_id=author_id))
		#events = Time.objects.filter(start_time__year=self.year, start_time__month=self.month)		#original
		events = event_data.filter(start_time__year=self.year, start_time__month=self.month)
#---leebc---
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		xx = self.formatmonthname(self.year, self.month, withyear=withyear)
		cal += f'{change_month(xx)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		# -----------
		cal += f'</table>\n'
		cal += '<p></p>'
		#------------
		return cal

def change_month(name):
	if 'Jan' in name:
		number = name.replace('January', '1월')
	if 'Feb' in name:
		number = name.replace('February', '2월')
	if 'Mar' in name:
		number = name.replace('March', '3월')
	if 'Apr' in name:
		number = name.replace('April', '4월')
	if 'May' in name:
		number = name.replace('May', '5월')
	if 'Jun' in name:
		number = name.replace('June', '6월')
	if 'July' in name:
		number = name.replace('July', '7월')
	if 'Aug' in name:
		number = name.replace('August', '8월')
	if 'Sep' in name:
		number = name.replace('September', '9월')
	if 'Oct' in name:
		number = name.replace('October', '10월')
	if 'Nov' in name:
		number = name.replace('November', '11월')
	if 'Dec' in name:
		number = name.replace('December', '12월')
	return number

############################################################################################################
############################################################################################################

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
		#cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		xx = self.formatmonthname(self.year, self.month, withyear=withyear)
		cal += f'{change_month(xx)}\n'
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

	def formatday(self, day, events, color):											# formats a day as a td, filter events by day
	# by leebc ----------------
		events_per_year_1 = events.filter(start_time__year__lte = self.year)
		events_per_year = events_per_year_1.filter(end_time__year__gte = self.year)

		events_per_month_1 = events_per_year.filter(start_time__month__lte = self.month)
		events_per_month = events_per_month_1.filter(end_time__month__gte = self.month)

		events_per_day_1 = events_per_month.filter(start_time__day__lte = day)
		events_per_day = events_per_day_1.filter(end_time__day__gte = day)
	# by leebc ----------------
		d = ''
		count = 0
		for event in events_per_day:
			count += 1
			if count > 3:
				dx = ""
			else:
				dx = event.get_html_url2
			d += f'<div>{dx}</div>'
		if day != 0:
			yearmonthday = (self.year - 2000) * 10000 + self.month * 100 + day
			url = reverse('timegram:schedule2', kwargs={'kk': yearmonthday})

			day_display = day
			if day==date.today().day:
				if color=='red':
					return f"<td> <a class='red_xdate' href={url} kk=day>{day_display}</a>  {d}</td>"
				else:
					return f"<td> <a class='xdate' href={url} kk=day>{day_display}</a>  {d}</td>"
			else:
				if color=='red':
					return f"<td> <a class='red_date' href={url} kk=day>{day_display}</a>  {d}</td>"
				else:
					return f"<td> <a class='date' href={url} kk=day>{day_display}</a>  {d}</td>"
		return '<td></td>'

	def formatweek(self, theweek, events):										# formats a week as a tr
		week = ''
		count = 0
		for d, weekday in theweek:
			count += 1
			if count==6 or count==7:
				color = 'red'
			else:
				color = 'blue'
			week += self.formatday(d, events, color)
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