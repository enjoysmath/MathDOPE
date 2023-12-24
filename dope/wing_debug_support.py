# Debugging support so Wing Pro can report exceptions before they are shown
# in the browser.  Fails quietly unless Wing's debugger is active.
import os
import sys

try:
    import django.views.debug

    def wing_debug_hook(*args, **kwargs):
        if __debug__ and 'WINGDB_ACTIVE' in os.environ:
            exc_type, exc_value, traceback = sys.exc_info()
            sys.excepthook(exc_type, exc_value, traceback)
        return old_technical_500_response(*args, **kwargs)

    old_technical_500_response = django.views.debug.technical_500_response
    django.views.debug.technical_500_response = wing_debug_hook

except Exception:
    print("Failed to install debugging support for Wing Pro")
    if "WINGDB_ACTIVE" in os.environ:
        raise

