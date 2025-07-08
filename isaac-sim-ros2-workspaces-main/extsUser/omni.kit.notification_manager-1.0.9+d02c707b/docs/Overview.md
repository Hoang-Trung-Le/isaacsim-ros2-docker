```{csv-table}
**Extension**: {{ extension_version }},**Documentation Generated**: {sub-ref}`today`
```

# Overview

This extension posts kinds of notifications to right-bottom of viewport or main window (if viewport invisible).

Following creates a simple notification:

```
import omni.kit.notification_manager as nm
nm.post_notification("This is a simple notification.")
```

![](simple_info_notification.png)


For more examples, please consult the [usage](USAGE) page.

For settings, please consult the [settings](SETTINGS) page.
