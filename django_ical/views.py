#:coding=utf-8:

from datetime import datetime

from django.contrib.syndication.views import Feed

# ICAL用の Django Syndication フレームワークに拡張するフィールド
FEED_EXTRA_FIELDS = (
    'method',
    'product_id',
    'timezone',
)
ICAL_EXTRA_FIELDS = (
    'timestamp',        # dtstamp
    'created',          # created
    'updated',          # last-modified
    'start_datetime',   # dtstart
    'end_datetime',     # dtend
    'transparency',     # transp
    'location',         # location
)

class ICalFeed(Feed):
    """
    ====================
    icalendar 用のFeed
    ====================

    既存フィールド
    ---------------------
    title => X-WR-CALNAME
    description => X-WR-CALDESC

    item_guid => UID
    item_title => SUMMARY
    item_description => DESCRIPTION
    item_link => URL
     
    拡張フィールド
    -------------------------
    method => METHOD
    timezone => X-WR-TIMEZONE

    item_class => CLASS
    item_timestamp => DTSTAMP
    item_created => CREATED
    item_updated => LAST-MODIFIED
    item_start_datetime => DTSTART
    item_end_datetime => DTEND
    item_transparency => TRANSP
    """
    def _get_dynamic_attr(self, attname, obj, default=None):
        """
        django.contrib.syndication.views.Feed からコピー
        """
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            # Check func_code.co_argcount rather than try/excepting the
            # function and catching the TypeError, because something inside
            # the function may raise the TypeError. This technique is more
            # accurate.
            if hasattr(attr, 'func_code'):
                argcount = attr.func_code.co_argcount
            else:
                argcount = attr.__call__.func_code.co_argcount
            if argcount == 2: # one argument is 'self'
                return attr(obj)
            else:
                return attr()
        return attr

    def method(self, obj):
        return 'PUBLISH'

    def feed_extra_kwargs(self, obj):
        kwargs = {}
        for field in FEED_EXTRA_FIELDS:
            val = self._get_dynamic_attr(field, obj)
            if val:
                kwargs[field] = val
        return kwargs

    def item_timestamp(self, obj):
        return datetime.now()

    def item_extra_kwargs(self, obj):
        kwargs = {}
        for field in ICAL_EXTRA_FIELDS:
            val = self._get_dynamic_attr('item_' + field, obj)
            if val:
                kwargs[field] = val
        return kwargs
