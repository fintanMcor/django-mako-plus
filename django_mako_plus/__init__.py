#
#   Author:  Conan Albrecht <ca&byu,edu>
#   License: Apache Open Source License
#

# pointer to our app config
# Django looks for this exact variable name
default_app_config = 'django_mako_plus.Config'

# the version
from .version import __version__


# the app config
from .apps import Config


# the exceptions
from .exceptions import RedirectException
from .exceptions import PermanentRedirectException
from .exceptions import JavascriptRedirectException
from .exceptions import InternalRedirectException


# the http responses
from .http import HttpResponseJavascriptRedirect


# the convenience functions
#
# Instead of these functions, consider using dmp_render() and dmp_render_to_string(),
# which are monkey-patched onto every DMP-enabled app at load time.  See the documentation
# for information on why we do this.
#
from .convenience import render_template
from .convenience import render_template_for_path
from .convenience import get_template
from .convenience import get_template_for_path
from .convenience import get_template_loader
from .convenience import get_template_loader_for_path


# the utilities
from .util import get_dmp_instance
from .util import get_dmp_app_configs


# the router
from .router import route_request, view_function


# the urls
# I'm specifically not including urls.py here because I want it imported
# as late as possible (after all the apps are set up).  Django will import it
# when it processes the project's urls.py file.


# the template engine
from .engine import MakoTemplates


# the static files shortcuts
from .static_files import get_template_css
from .static_files import get_template_js
from .static_files import get_fake_template_css
from .static_files import get_fake_template_js
