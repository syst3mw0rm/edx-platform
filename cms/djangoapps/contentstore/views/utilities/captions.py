

"""
Views related to operations on course objects
"""
import json


from django.contrib.auth.decorators import login_required
from django_future.csrf import ensure_csrf_cookie
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from edxmako.shortcuts import render_to_response
from xmodule.modulestore.django import modulestore, loc_mapper
from models.settings.course_grading import CourseGradingModel

from ..access import has_course_access
from ..component import (
    OPEN_ENDED_COMPONENT_TYPES, NOTE_COMPONENT_TYPES,
    ADVANCED_COMPONENT_POLICY_KEY)

from xmodule.modulestore.locator import BlockUsageLocator

from xmodule.contentstore.content import StaticContent
from xmodule.contentstore.django import contentstore
from xmodule.exceptions import NotFoundError
import logging
import copy
from django.conf import settings
import requests
from ...transcripts_utils import (get_transcripts_from_youtube,
                                  GetTranscriptsFromYouTubeException,
                                  save_module,
                                  download_youtube_subs)


log = logging.getLogger(__name__)

__all__ = ['utility_captions_handler']


def _get_locator_and_course(package_id, branch, version_guid, block_id, user, depth=0):
    """
    Internal method used to calculate and return the locator and course module
    for the view functions in this file.
    """
    locator = BlockUsageLocator(package_id=package_id, branch=branch, version_guid=version_guid, block_id=block_id)
    if not has_course_access(user, locator):
        raise PermissionDenied()
    course_location = loc_mapper().translate_locator_to_location(locator)
    course_module = modulestore().get_item(course_location, depth=depth)
    return locator, course_module


# pylint: disable=unused-argument
@login_required
def utility_captions_handler(request, tag=None, package_id=None, branch=None, version_guid=None, block=None, utilities_index=None):
    """
    The restful handler for course specific requests.
    It provides the course tree with the necessary information for identifying and labeling the parts. The root
    will typically be a 'course' object but may not be especially as we support modules.

    GET
        html: return course listing page if not given a course id
        html: return html page overview for the given course if given a course id
        json: return json representing the course branch's index entry as well as dag w/ all of the children
        replaced w/ json docs where each doc has {'_id': , 'display_name': , 'children': }
    POST
        json: create a course, return resulting json
        descriptor (same as in GET course/...). Leaving off /branch/draft would imply create the course w/ default
        branches. Cannot change the structure contents ('_id', 'display_name', 'children') but can change the
        index entry.
    PUT
        json: update this course (index entry not xblock) such as repointing head, changing display name, org,
        package_id, prettyid. Return same json as above.
    DELETE
        json: delete this branch from this course (leaving off /branch/draft would imply delete the course)
    """
    if request.method == 'GET':  # assume html
        return course_index(request, package_id, branch, version_guid, block)
    else:
        if request.method == 'POST':
            for key in request.POST:
                if key != 'csrfmiddlewaretoken':
                    try:
                        item = modulestore().get_item(key)
                        download_youtube_subs({1.0: item.youtube_id_1_0}, item)
                        item.sub = item.youtube_id_1_0
                        save_module(item, request.user)
                    except GetTranscriptsFromYouTubeException as e:
                        print 'ughhh'
            return course_index(request, package_id, branch, version_guid, block)
        else:
            return HttpResponseNotFound()


@login_required
@ensure_csrf_cookie
def course_index(request, package_id, branch, version_guid, block):
    """
    Display an editable course overview.

    org, course, name: Attributes of the Location for the item to edit
    """
    locator, course = _get_locator_and_course(
        package_id, branch, version_guid, block, request.user, depth=3
    )
    sections = course.get_children()

    unit_dict = {}

    for section in sections:
        for subsection in section.get_children():
            for unit in subsection.get_children():
                for component in unit.get_children():
                    if component.location.category == 'video':
                        if unit_dict.get(section) is None:
                            unit_dict[section] = {}
                        if unit_dict[section].get(subsection) is None:
                            unit_dict[section][subsection] = {}
                        if unit_dict[section][subsection].get(unit) is None:
                            unit_dict[section][subsection][unit] = {}
                        val = get_transcript_status(component)
                        unit_dict[section][subsection][unit][component] = val['status'] == 'Success' and not val['youtube_diff']
                        break
        #         break
        #     break
        # break


    return render_to_response('captions.html',
        {
            'sections': unit_dict,
            'context_course': course,
            'new_unit_category': 'vertical',
            'course_graders': json.dumps(CourseGradingModel.fetch(locator).graders),
            'locator': locator,
        }
    )


def get_transcript_status(item):
    transcripts_presence = {
        'html5_local': [],
        'html5_equal': False,
        'is_youtube_mode': False,
        'youtube_local': False,
        'youtube_server': False,
        'youtube_diff': True,
        'current_item_subs': None,
        'status': 'Error',
    }

    videos = {'youtube': item.youtube_id_1_0}
    html5 = {}
    for url in item.html5_sources:
        name = url.split('/')[-1].split('.mp4')[0]
        html5[name] = 'html5'
    videos['html5'] = html5

    transcripts_presence['status'] = 'Success'

    filename = 'subs_{0}.srt.sjson'.format(item.sub)
    content_location = StaticContent.compute_location(
        item.location.org, item.location.course, filename
    )
    try:
        local_transcripts = contentstore().find(content_location).data
        transcripts_presence['current_item_subs'] = item.sub
    except NotFoundError:
        pass

    # Check for youtube transcripts presence
    youtube_id = videos.get('youtube', None)
    if youtube_id:
        transcripts_presence['is_youtube_mode'] = True

        # youtube local
        filename = 'subs_{0}.srt.sjson'.format(youtube_id)
        content_location = StaticContent.compute_location(
            item.location.org, item.location.course, filename
        )
        try:
            local_transcripts = contentstore().find(content_location).data
            transcripts_presence['youtube_local'] = True
        except NotFoundError:
            log.debug("Can't find transcripts in storage for youtube id: %s", youtube_id)

        # youtube server
        youtube_api = copy.deepcopy(settings.YOUTUBE_API)
        youtube_api['params']['v'] = youtube_id
        youtube_response = requests.get(youtube_api['url'], params=youtube_api['params'])

        if youtube_response.status_code == 200 and youtube_response.text:
            transcripts_presence['youtube_server'] = True
        #check youtube local and server transcripts for equality
        if transcripts_presence['youtube_server'] and transcripts_presence['youtube_local']:
            try:
                youtube_server_subs = get_transcripts_from_youtube(youtube_id)
                if json.loads(local_transcripts) == youtube_server_subs:  # check transcripts for equality
                    transcripts_presence['youtube_diff'] = False
            except GetTranscriptsFromYouTubeException:
                pass

    # Check for html5 local transcripts presence
    html5_subs = []
    for html5_id in videos['html5']:
        filename = 'subs_{0}.srt.sjson'.format(html5_id)
        content_location = StaticContent.compute_location(
            item.location.org, item.location.course, filename
        )
        try:
            html5_subs.append(contentstore().find(content_location).data)
            transcripts_presence['html5_local'].append(html5_id)
        except NotFoundError:
            log.debug("Can't find transcripts in storage for non-youtube video_id: %s", html5_id)
        if len(html5_subs) == 2:  # check html5 transcripts for equality
            transcripts_presence['html5_equal'] = json.loads(html5_subs[0]) == json.loads(html5_subs[1])

    command, subs_to_use = _transcripts_logic(transcripts_presence, videos)
    transcripts_presence.update({
        'command': command,
        'subs': subs_to_use,
    })
    return transcripts_presence


def _transcripts_logic(transcripts_presence, videos):
    """
    By `transcripts_presence` content, figure what show to user:

    returns: `command` and `subs`.

    `command`: string,  action to front-end what to do and what show to user.
    `subs`: string, new value of item.sub field, that should be set in module.

    `command` is one of::

        replace: replace local youtube subtitles with server one's
        found: subtitles are found
        import: import subtitles from youtube server
        choose: choose one from two html5 subtitles
        not found: subtitles are not found
    """
    command = None

    # new value of item.sub field, that should be set in module.
    subs = ''

    # youtube transcripts are of high priority than html5 by design
    if (
            transcripts_presence['youtube_diff'] and
            transcripts_presence['youtube_local'] and
            transcripts_presence['youtube_server']):  # youtube server and local exist
        command = 'replace'
        subs = videos['youtube']
    elif transcripts_presence['youtube_local']:  # only youtube local exist
        command = 'found'
        subs = videos['youtube']
    elif transcripts_presence['youtube_server']:  # only youtube server exist
        command = 'import'
    else:  # html5 part
        if transcripts_presence['html5_local']:  # can be 1 or 2 html5 videos
            if len(transcripts_presence['html5_local']) == 1 or transcripts_presence['html5_equal']:
                command = 'found'
                subs = transcripts_presence['html5_local'][0]
            else:
                command = 'choose'
                subs = transcripts_presence['html5_local'][0]
        else:  # html5 source have no subtitles
            # check if item sub has subtitles
            if transcripts_presence['current_item_subs'] and not transcripts_presence['is_youtube_mode']:
                log.debug("Command is use existing %s subs", transcripts_presence['current_item_subs'])
                command = 'use_existing'
            else:
                command = 'not_found'
    log.debug(
        "Resulted command: %s, current transcripts: %s, youtube mode: %s",
        command,
        transcripts_presence['current_item_subs'],
        transcripts_presence['is_youtube_mode']
    )
    return command, subs
