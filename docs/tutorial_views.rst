T2: .py View Files
===================================

.. contents::
    :depth: 2

Let's add some "work" to the process by adding the current server time to the index page. Create a new file ``homepage/views/index.py`` and copy this code into it:

.. code:: python

    from django.conf import settings
    from django_mako_plus import view_function
    from datetime import datetime
    from .. import dmp_render, dmp_render_to_string

    @view_function
    def process_request(request):
        context = {
            'now': datetime.now(),
        }
        return dmp_render(request, 'index.html', context)

Reload your server and browser page, and you should see the exact same page. It might look the same, but something very important happened in the routing. Rather than going straight to the ``index.html`` page, processing went to your new ``index.py`` file. At the end of the ``process_request`` function above, we manually render the ``index.html`` file. In other words, we're now doing extra "work" before the rendering. This is the place to do database connections, modify objects, prepare and handle forms, etc. It keeps complex code out of your html pages.

Let me pause for a minute and talk about log messages. If you enabled the logger in the installation, you should see the following in your console:

::

    DEBUG::DMP variables set by urls.py: ['dmp_router_app', 'dmp_router_page', 'urlparams']; variables set by defaults: ['dmp_router_function'].
    INFO::DMP processing: app=homepage, page=index, module=homepage.views.index, func=process_request, urlparams=['']
    INFO::DMP calling view function homepage.views.index.process_request
    DEBUG::DMP rendering template /Users/conan/Documents/data/teaching/2017/IS 411-413/fomoproject/homepage/templates/index.html

These debug statements are incredibly helpful in figuring out why pages aren't routing right. If your page didn't load right, you'll probably see why in these statements. In my log above, the first line lists what named parameters were matched in ``urls.py``.

The second line shows the how these named (or defaulted) parameters translated into the app, page, module, and function.

The third line shows the controller found the ``index.py`` view, and it called the ``process_request`` function successfully. This is important -- the ``process_request`` function is the "default" view function. This web-accessible function must be decorated with ``@view_function``.

    This decoration with ``@view_function`` is done for security. If the framework were to allow browsers specify any old function, end users could invoke any function of any module on your system! By requiring the decorator, the framework limits end users to one specifically-named function.

You can have multiple decorators on your function, such as a permissions check and ``view_function``. The order isn't important unless the other decorators don't wrap the function correctly.  If ``@view_function`` is listed first, you won't have to worry.

.. code:: python

    @view_function
    @permission_required('can_vote')
    def process_request(request):
        ...

|

    Later in the tutorial, we'll describe another way to call other functions within your view Even though ``process_request`` is the default function, you can actually have multiple web-accessible functions within a single .py file.

As stated earlier, we explicitly call the Mako renderer at the end of the ``process_request`` function. The context (the third parameter of the call) is a dictionary containing variables to be passed to the template.

Let's use the ``now`` variable in our index.html template:

.. code:: html

    <%inherit file="base.htm" />

    <%block name="content">
        <div class="content">
          <h3>Congratulations -- you've successfully created a new django-mako-plus app!</h3>
          <h4>Next Up: Go through the django-mako-plus tutorial and add Javascript, CSS, and urlparams to this page.</h4>
          <p class="server-time">The current server time is ${ now }.</p>
          <p class="browser-time">The current browser time is...</p>
        </div>
    </%block>

The ``${ varname }`` code is Mako syntax and is described more fully on the Mako web site. Right now, it's most important that you see how to send data from the view to the template. If you already know Django templates, it should be familiar.

Reload your web page and ensure the new view is working correctly. You should see the server time printed on the screen. Each time you reload the page, the time changes.


The Render Functions
-------------------------

    This section explains the two render functions included with DMP. If you just want to get things working, skip over this section. You can always come back later for an explanation of how things are put together.

In the example above, we used the ``dmp_render`` function to render our template. It's the DMP equivalent of Django's ``render`` shortcut function. The primary difference between the two functions (other than, obviously, the names) is DMP's function must be **connected to an app**. Django searches for templates in a flat list of directories -- while your apps might have templates in them, Django just searches through them in order. DMP's structure is logically app-based: each of your apps contains a ``templates`` directory, and DMP always searches the *current* app directly. With DMP, there are no worries about template name clashes or finding issues.

Because DMP is app-aware, it creates more than one render function -- one per app. You'll have one version of ``dmp_render`` in your homepage app, another version of ``dmp_render`` in your catalog app, and so forth through your apps. The function is named the same in each module for consistency.

**Practically, you don't need to worry about any of this.** DMP is smart enough to know which render is connected to which app. You just need to import the function correctly in each of your views, like this:

.. code:: python

    # this works in any app/views/*.py file:
    from .. import dmp_render, dmp_render_to_string

If relative imports (the double dot) make you want to take a shower, absolute imports are fine too.  Just be sure you use the appropriate app name, depending on the location of your template.  A common copy-and-paste mistake is duplicating a view.py file across apps and forgetting to change the app name.

.. code:: python

    # this also works in any app/views/*.py file:
    from homepage import dmp_render, dmp_render_to_string

By using one of the above import lines, you'll always get a template renderer that is app-aware and that processes template inheritance, includes, CSS, and JS files correctly.

    Some Python programmers have strong feelings about relative vs. absolute imports. Use whichever you prefer. Personally, I favor the first one (relative importing) because it requires me to think less when I copy view files.

DMP provides a second function, ``dmp_render_to_string``. This is nearly the same as ``dmp_render``, but ``dmp_render_to_string`` returns a string rather than an ``HttpResponse`` object. If you need a custom response, or if you simply need the rendered string, ``dmp_render_to_string`` is the ticket. Most of the time, ``dmp_render`` is the appropriate method because Django expects the full response object (not just the content string) returned from your views.

Scroll to `Mime Types and Status Codes`_ to see an example of the ``dmp_render_to_string`` function.

If you need to process templates across apps within a single view.py file (likely a rare case), use absolute imports and give an alias to the functions as you import them:

.. code:: python

    from homepage import dmp_render as homepage_render
    from catalog import dmp_render as catalog_render

Suppose you need to put your templates in a directory named something other than ``/appname/templates/``. Or perhaps you have a non-traditional app path. The two above methods are really just convenience methods to make rendering easier. If you need a custom template instance, switch to the paddle shifters:

.. code:: python

    from django.conf import settings
    from django_mako_plus import view_function
    from django_mako_plus.template import get_template_loader
    from datetime import datetime

    @view_function
    def process_request(request):
        context = {
            'now': datetime.now(),
        }

        # this syntax is only needed if you need to customize the way template rendering works
        tlookup = get_template_loader('/app/path/', subdir="my_templates")
        template = tlookup.get_template('index.html')
        return template.render_to_response(request=request, context=context)

The above code references an app in a non-standard location and a template subdirectory with a non-standard name.  `A shorter version of this <Convenience Functions_>`_ also exists.


Mime Types and Status Codes
---------------------------

The ``dmp_render()`` function determines the mime type from the template extension and returns a *200* status code. What if you need to return JSON, CSV, or a 404 not found? Just wrap the ``dmp_render_to_string`` function in a standard Django ``HttpResponse`` object. A few examples:

.. code:: python

    from django.http import HttpResponse

    # return CSV
    return HttpResponse(dmp_render_to_string(request, 'my_csv.html', {}), mimetype='text/csv')

    # return a custom error page
    return HttpResponse(dmp_render_to_string(request, 'custom_error_page.html', {}), status=404)


Convenience Functions
-------------------------

You might be wondering: Can I use a dynamically-found app? What if I need a template object? Can I render a file directly?

Use the DMP convenience functions to be more dynamic, to interact directly with template objects, or to render a file of your choosing.

*Render a file from any app's template directory:*

.. code:: python

    from django_mako_plus import render_template
    mystr = render_template(request, 'homepage', 'index.html', context)

*Render a file from a custom directory within an app:*

.. code:: python

    from django_mako_plus import render_template
    mystr = render_template(request, 'homepage', 'custom.html', context, subdir="customsubdir")

*Render a file at any location, even outside of your project:*

.. code:: python

    from django_mako_plus import render_template_for_path
    mystr = render_template_for_path(request, '/var/some/dir/template.html', context)

*Get a template object for a template in an app:*

.. code:: python

    from django_mako_plus import get_template
    template = get_template('homepage', 'index.html')

*Get a template object at any location, even outside your project:*

.. code:: python

    from django_mako_plus import get_template_for_path
    template = get_template_for_path('/var/some/dir/template.html')

*Get a lower-level Mako template object (without the Django template wrapper):*

.. code:: python

    from django_mako_plus import get_template_for_path
    template = get_template_for_path('/var/some/dir/template.html')
    mako_template = template.mako_template

See the `Mako documentation <http://www.makotemplates.org/>`__ for more information on working directly with Mako template objects. Mako has many features that go well beyond the DMP interface.

    The convenience functions are perfectly fine if they suit your needs, but the ``dmp_render`` function described at the beginning of the tutorial is likely the best choice for most users because it doesn't hard code the app name. The convenience functions are not Django-API compliant.

Django API Calls
--------------------------------

As a template engine, DMP conforms to the Django standard.  If you need/want to use the standard Django template functions, use the following:

.. code:: python

    from django.shortcuts import render
    return render(request, 'homepage/index.html', context)

or to be more explicit with Django:

.. code:: python

    from django.shortcuts import render
    return render(request, 'homepage/index.html', context, using='django_mako_plus')
