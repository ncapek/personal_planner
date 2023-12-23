test_response = {
  'weather_data': {
    'current_weather': {
      'temperature': '0.3°C',
      'description': 'snow',
      'sunrise': '2023-12-23 07:59:18 CET',
      'sunset': '2023-12-23 16:02:48 CET',
      'wind_speed': '6.17 m/s',
      'humidity': '96%'
    },
    'today_forecast': {
      'max_temp': '4.33°C',
      'min_temp': '0.3°C',
      'conditions': 'rain and snow'
    },
    'alerts': [
      {
        'title': 'Flood Alert',
        'description': 'Flood warning - 2nd level of flood stage is expected at some river reaches. Water may start to overbank in the countryside.',
        'start': '2023-12-23 00:00:00 CET',
        'end': '2023-12-24 19:59:59 CET'
      },
      {
        'title': 'Very Strong Wind',
        'description': 'Very strong northwest wind with gusts 65 to 90 kmph.',
        'start': '2023-12-22 13:42:32 CET',
        'end': '2023-12-23 07:59:59 CET'
      },
      {
        'title': 'Strong Wind',
        'description': 'Strong northwest wind with gusts to 70 kmph.',
        'start': '2023-12-23 22:00:00 CET',
        'end': '2023-12-24 23:59:59 CET'
      }
    ]
  },
  'fitness_data':
    {
      'steps_count': 1533,
      'active_minutes': 20,
      'calories_expended': 251,
      'heart_minutes': 9
    },
  'planner_data': [
    {
      'name': 'test',
      'description': None,
      'duration': 30,
      'due_date': '2023-12-22T22:59:59.999Z',
      'type': 'Work'
    },
    {
      'name': 'test',
      'description': None,
      'duration': 30,
      'due_date': '2023-12-21T07:45:00.000Z',
      'type': ''
    },
  ]
}