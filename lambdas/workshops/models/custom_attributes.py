from pynamodb.attributes import (MapAttribute, UnicodeAttribute)


class ScheduleMap(MapAttribute):
    date = UnicodeAttribute()
    init_time = UnicodeAttribute()
    end_time = UnicodeAttribute()

