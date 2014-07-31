import cgi
import logging

import ckan.lib.helpers as helpers
import ckan.lib.base as base
import ckanext.oauth2.repozewho as oauth2_repozewho

from ckan.common import request, response

log = logging.getLogger(__name__)


class OAuth2Controller(base.BaseController):

    def callback(self):
        '''
        If the callback is called properly, this function won't be executed.
        This function is only executed when an error arises login the user in
        the OAuth2 Server (i.e.: a user doesn't allow the application to access
        their data, the application is not running over HTTPs,...)
        '''
        log.debug('Callback Controller')
        # Move to the came_from page coded in the state of the OAuth request
        response.status_int = 302   # FOUND
        redirect_url = oauth2_repozewho.get_came_from(request.params.get('state'))
        redirect_url = '/' if redirect_url == oauth2_repozewho.INITIAL_PAGE else redirect_url
        response.location = redirect_url
        helpers.flash_error(cgi.escape(request.GET.get('error_description',
                            'It was impossible to log in you using the OAuth2 Service')))
