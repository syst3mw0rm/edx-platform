"""
Custom field types for mongoengine
"""
import mongoengine
from xmodule.modulestore.locations import SlashSeparatedCourseKey, Location
from types import NoneType
from xmodule.modulestore.keys import CourseKey


class CourseKeyField(mongoengine.StringField):
    """
    Serializes and deserializes CourseKey's to mongo dbs which use mongoengine
    """
    def __init__(self, **kwargs):
        # it'd be useful to add init args such as support_deprecated, force_deprecated
        super(CourseKeyField, self).__init__(**kwargs)

    def to_mongo(self, course_key):
        """
        For now saves the course key in the deprecated form
        """
        assert isinstance(course_key, (NoneType, SlashSeparatedCourseKey))
        return super(CourseKeyField, self).to_mongo(course_key.to_deprecated_string())

    def to_python(self, course_key):
        """
        Deserialize to a CourseKey instance
        """
        course_key = super(CourseKeyField, self).to_python(course_key)
        assert isinstance(course_key, (NoneType, basestring, SlashSeparatedCourseKey))
        return SlashSeparatedCourseKey.from_deprecated_string(course_key)

    def validate(self, value):
        assert isinstance(value, (NoneType, basestring, SlashSeparatedCourseKey))
        if isinstance(value, CourseKey):
            return super(CourseKeyField, self).validate(value.to_deprecated_string())
        else:
            return super(CourseKeyField, self).validate(value)

    def prepare_query_value(self, op, value):
        return self.to_mongo(value)


class UsageKeyField(mongoengine.StringField):
    """
    Represent a UsageKey as a single string in Mongo
    """
    def to_mongo(self, location):
        """
        For now saves the usage key in the deprecated location i4x/c4x form
        """
        assert isinstance(location, (NoneType, SlashSeparatedCourseKey))
        return super(UsageKeyField, self).to_mongo(location.to_deprecated_string())

    def to_python(self, location):
        """
        Deserialize to a UsageKey instance: for now it's a location missing the run
        """
        assert isinstance(location, (NoneType, basestring, Location))
        if not location:
            return None
        if isinstance(location, basestring):
            location = super(UsageKeyField, self).to_python(location)
            return Location.from_deprecated_string(location)
        else:
            return location

    def validate(self, value):
        assert isinstance(value, (NoneType, basestring, Location))
        if isinstance(value, Location):
            return super(UsageKeyField, self).validate(value.to_deprecated_string())
        else:
            return super(UsageKeyField, self).validate(value)

    def prepare_query_value(self, op, value):
        return self.to_mongo(value)
